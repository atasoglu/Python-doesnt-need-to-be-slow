#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

typedef struct {
    double x, y, z;
    double vx, vy, vz;
    double mass;
} Planet;

void compute_forces(Planet* planets, int n, double dt) {
    double soft_epsilon = 1e-9;
    
    for (int i = 0; i < n; i++) {
        double fx = 0.0, fy = 0.0, fz = 0.0;
        double p1x = planets[i].x;
        double p1y = planets[i].y;
        double p1z = planets[i].z; // Fix: z was missing reference to planets[i]
        
        for (int j = 0; j < n; j++) {
            if (i == j) continue;
            
            double dx = planets[j].x - p1x;
            double dy = planets[j].y - p1y;
            double dz = planets[j].z - p1z;
            
            double dist_sq = dx*dx + dy*dy + dz*dz + soft_epsilon;
            double dist = sqrt(dist_sq);
            double f = planets[j].mass / (dist_sq * dist);
            
            fx += f * dx;
            fy += f * dy;
            fz += f * dz;
        }
        
        planets[i].vx += fx * dt;
        planets[i].vy += fy * dt;
        planets[i].vz += fz * dt;
    }
}

void update_positions(Planet* planets, int n, double dt) {
    for (int i = 0; i < n; i++) {
        planets[i].x += planets[i].vx * dt;
        planets[i].y += planets[i].vy * dt;
        planets[i].z += planets[i].vz * dt;
    }
}

int main(int argc, char* argv[]) {
    int n = 100;
    int steps = 100;
    
    // Parse args: ./nbody <n> <steps>
    if (argc > 1) n = atoi(argv[1]);
    if (argc > 2) steps = atoi(argv[2]);
    
    // Check for flags from python runner: --n N --steps S
    for(int i=1; i<argc; i++) {
        if(strcmp(argv[i], "--n") == 0 && i+1 < argc) n = atoi(argv[i+1]);
        if(strcmp(argv[i], "--steps") == 0 && i+1 < argc) steps = atoi(argv[i+1]);
    }
    
    printf("Running C N-body with N=%d, Steps=%d\n", n, steps);
    
    Planet* planets = (Planet*)malloc(n * sizeof(Planet));
    
    // Initialize
    srand(42);
    for (int i = 0; i < n; i++) {
        planets[i].x = ((double)rand() / RAND_MAX) * 200.0 - 100.0;
        planets[i].y = ((double)rand() / RAND_MAX) * 200.0 - 100.0;
        planets[i].z = ((double)rand() / RAND_MAX) * 200.0 - 100.0;
        planets[i].vx = ((double)rand() / RAND_MAX) * 2.0 - 1.0;
        planets[i].vy = ((double)rand() / RAND_MAX) * 2.0 - 1.0;
        planets[i].vz = ((double)rand() / RAND_MAX) * 2.0 - 1.0;
        planets[i].mass = ((double)rand() / RAND_MAX) * 9.0 + 1.0;
    }
    
    clock_t start = clock();
    
    double dt = 0.01;
    for (int s = 0; s < steps; s++) {
        compute_forces(planets, n, dt);
        update_positions(planets, n, dt);
    }
    
    clock_t end = clock();
    double time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;
    
    printf("Time: %.4f seconds\n", time_taken);
    printf("RESULT: %.4f\n", time_taken);
    
    free(planets);
    return 0;
}
