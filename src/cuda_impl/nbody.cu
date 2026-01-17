#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <cuda_runtime.h>
#include <string.h>

void print_gpu_info() {
    int device_count;
    cudaGetDeviceCount(&device_count);
    
    cudaDeviceProp prop;
    cudaGetDeviceProperties(&prop, 0);
    
    printf("GPU: %s\n", prop.name);
    // Note: CUDA Cores per SM varies by architecture. 128 is typical for recent archs (Ampere, Ada).
    printf("CUDA Cores: %d\n", prop.multiProcessorCount * 128);
    printf("Memory: %.1f GB\n", prop.totalGlobalMem / 1e9);
    printf("Compute Capability: %d.%d\n", prop.major, prop.minor);
}

void allocate_gpu_memory(size_t required) {
    size_t free_mem, total_mem;
    cudaMemGetInfo(&free_mem, &total_mem);
    
    printf("GPU Memory: %.1f/%.1f GB used\n", 
           (total_mem - free_mem) / 1e9, total_mem / 1e9);
    
    if (required > free_mem) {
        printf("ERROR: Insufficient GPU memory\n");
        exit(1);
    }
}

__global__ void compute_forces_kernel(
    float3* pos, float3* vel, float* mass, 
    int n, float dt
) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= n) return;
    
    // Force computation per thread
    float3 p1 = pos[i];
    float3 acc = make_float3(0.0f, 0.0f, 0.0f);
    float soft_epsilon = 1e-9f;

    for (int j = 0; j < n; j++) {
        if (i == j) continue;

        float3 p2 = pos[j];
        float dx = p2.x - p1.x;
        float dy = p2.y - p1.y;
        float dz = p2.z - p1.z;

        float dist_sq = dx*dx + dy*dy + dz*dz + soft_epsilon;
        float dist = sqrtf(dist_sq);
        float f = mass[j] / (dist_sq * dist);

        acc.x += f * dx;
        acc.y += f * dy;
        acc.z += f * dz;
    }

    vel[i].x += acc.x * dt;
    vel[i].y += acc.y * dt;
    vel[i].z += acc.z * dt;
}

__global__ void update_positions_kernel(float3* pos, float3* vel, int n, float dt) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= n) return;

    pos[i].x += vel[i].x * dt;
    pos[i].y += vel[i].y * dt;
    pos[i].z += vel[i].z * dt;
}

void run_cpu_fallback() {
    printf("Falling back to CPU implementation is not fully integrated yet.\n");
    exit(1);
}

int main(int argc, char* argv[]) {
    int n = 100;
    int steps = 100;
    
    // Parse args
    for(int i=1; i<argc; i++) {
        if(strcmp(argv[i], "--n") == 0 && i+1 < argc) n = atoi(argv[i+1]);
        if(strcmp(argv[i], "--steps") == 0 && i+1 < argc) steps = atoi(argv[i+1]);
    }

    int device_count;
    cudaError_t err = cudaGetDeviceCount(&device_count);
    
    if (err != cudaSuccess || device_count == 0) {
        printf("No CUDA devices found. Falling back to CPU.\n");
        run_cpu_fallback();
        return 0;
    }
    
    print_gpu_info();
    printf("Running CUDA N-body with N=%d, Steps=%d\n", n, steps);

    // Calculate memory requirements
    size_t size_float3 = n * sizeof(float3);
    size_t size_float = n * sizeof(float);
    size_t total_required = size_float3 * 2 + size_float;
    
    // Check GPU memory
    allocate_gpu_memory(total_required);

    // Allocate Host memory
    float3* h_pos = (float3*)malloc(size_float3);
    float3* h_vel = (float3*)malloc(size_float3);
    float* h_mass = (float*)malloc(size_float);

    // Initialize (match C version logic but float)
    srand(42);
    for (int i = 0; i < n; i++) {
        h_pos[i].x = ((float)rand() / RAND_MAX) * 200.0f - 100.0f;
        h_pos[i].y = ((float)rand() / RAND_MAX) * 200.0f - 100.0f;
        h_pos[i].z = ((float)rand() / RAND_MAX) * 200.0f - 100.0f;
        h_vel[i].x = ((float)rand() / RAND_MAX) * 2.0f - 1.0f;
        h_vel[i].y = ((float)rand() / RAND_MAX) * 2.0f - 1.0f;
        h_vel[i].z = ((float)rand() / RAND_MAX) * 2.0f - 1.0f;
        h_mass[i] = ((float)rand() / RAND_MAX) * 9.0f + 1.0f;
    }

    // Allocate Device memory
    float3 *d_pos, *d_vel;
    float *d_mass;
    cudaMalloc(&d_pos, size_float3);
    cudaMalloc(&d_vel, size_float3);
    cudaMalloc(&d_mass, size_float);

    // Copy Host -> Device
    cudaMemcpy(d_pos, h_pos, size_float3, cudaMemcpyHostToDevice);
    cudaMemcpy(d_vel, h_vel, size_float3, cudaMemcpyHostToDevice);
    cudaMemcpy(d_mass, h_mass, size_float, cudaMemcpyHostToDevice);

    float dt = 0.01f;
    int blockSize = 256;
    int numBlocks = (n + blockSize - 1) / blockSize;

    // Timer
    cudaEvent_t start, stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);

    cudaEventRecord(start);

    for (int s = 0; s < steps; s++) {
        compute_forces_kernel<<<numBlocks, blockSize>>>(d_pos, d_vel, d_mass, n, dt);
        update_positions_kernel<<<numBlocks, blockSize>>>(d_pos, d_vel, n, dt);
    }
    
    cudaEventRecord(stop);
    cudaEventSynchronize(stop);
    
    float milliseconds = 0;
    cudaEventElapsedTime(&milliseconds, start, stop);
    float seconds = milliseconds / 1000.0f;
    
    printf("Time: %.4f seconds\n", seconds);
    printf("RESULT: %.4f\n", seconds);

    // Cleanup
    free(h_pos); free(h_vel); free(h_mass);
    cudaFree(d_pos); cudaFree(d_vel); cudaFree(d_mass);
    cudaEventDestroy(start); cudaEventDestroy(stop);
    
    return 0;
}
