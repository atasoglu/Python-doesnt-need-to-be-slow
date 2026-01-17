import argparse
import time
import numpy as np
import math
from numba import cuda

@cuda.jit
def compute_forces_kernel(pos, vel, mass, dt, soft_epsilon):
    i = cuda.grid(1)
    n = pos.shape[0]
    
    if i < n:
        fx = 0.0
        fy = 0.0
        fz = 0.0
        
        x1 = pos[i, 0]
        y1 = pos[i, 1]
        z1 = pos[i, 2]
        
        for j in range(n):
            if i == j:
                continue
            
            dx = pos[j, 0] - x1
            dy = pos[j, 1] - y1
            dz = pos[j, 2] - z1
            
            dist_sq = dx*dx + dy*dy + dz*dz + soft_epsilon
            dist = math.sqrt(dist_sq)
            f = mass[j, 0] / (dist_sq * dist)
            
            fx += f * dx
            fy += f * dy
            fz += f * dz
        
        vel[i, 0] += fx * dt
        vel[i, 1] += fy * dt
        vel[i, 2] += fz * dt

@cuda.jit
def update_positions_kernel(pos, vel, dt):
    i = cuda.grid(1)
    n = pos.shape[0]
    
    if i < n:
        pos[i, 0] += vel[i, 0] * dt
        pos[i, 1] += vel[i, 1] * dt
        pos[i, 2] += vel[i, 2] * dt

def run_simulation(n_bodies, n_steps, dt=0.01, soft_epsilon=1e-9):
    # Initialize implementation using standard numpy
    np.random.seed(42)
    pos = np.random.uniform(-100, 100, (n_bodies, 3)).astype(np.float32)
    vel = np.random.uniform(-1, 1, (n_bodies, 3)).astype(np.float32)
    mass = np.random.uniform(1, 10, (n_bodies, 1)).astype(np.float32)
    
    # Check for CUDA
    if not cuda.is_available():
        raise RuntimeError("CUDA is not available on this system.")

    # Transfer to device
    d_pos = cuda.to_device(pos)
    d_vel = cuda.to_device(vel)
    d_mass = cuda.to_device(mass)
    
    threadsperblock = 256
    blockspergrid = (n_bodies + (threadsperblock - 1)) // threadsperblock
    
    # Warmup compilation
    compute_forces_kernel[blockspergrid, threadsperblock](d_pos, d_vel, d_mass, dt, soft_epsilon)
    update_positions_kernel[blockspergrid, threadsperblock](d_pos, d_vel, dt)
    cuda.synchronize()
    
    start_time = time.time()
    
    for _ in range(n_steps):
        compute_forces_kernel[blockspergrid, threadsperblock](d_pos, d_vel, d_mass, dt, soft_epsilon)
        update_positions_kernel[blockspergrid, threadsperblock](d_pos, d_vel, dt)
    
    cuda.synchronize()
    end_time = time.time()
    
    # Optional: copy back if needed for verification
    # pos = d_pos.copy_to_host()
    
    return end_time - start_time

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Numba CUDA N-body benchmark")
    parser.add_argument("--n", type=int, default=100, help="Number of bodies")
    parser.add_argument("--steps", type=int, default=100, help="Number of steps")
    args = parser.parse_args()

    try:
        if not cuda.is_available():
           print("CUDA not detected. Exiting.")
           exit(1)

        print(f"Running Numba CUDA N-body with N={args.n}, Steps={args.steps}")
        duration = run_simulation(args.n, args.steps)
        print(f"Time: {duration:.4f} seconds")
        print(f"RESULT: {duration}")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
