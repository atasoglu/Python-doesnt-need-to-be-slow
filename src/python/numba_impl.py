import argparse
import time
import numpy as np
from numba import njit, prange

@njit(parallel=True)
def compute_forces_numba(pos, mass, dt, soft_epsilon):
    n = pos.shape[0]
    # We can output directly to velocity or a separate acc array
    # Let's compute acceleration directly to match structure
    acc = np.zeros((n, 3))
    
    for i in prange(n):
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
            dist =  project_sqrt_impl(dist_sq) # helper or math.sqrt
            
            f = mass[j] / (dist_sq * dist)
            
            fx += f * dx
            fy += f * dy
            fz += f * dz
            
        acc[i, 0] = fx
        acc[i, 1] = fy
        acc[i, 2] = fz
        
    return acc

@njit
def project_sqrt_impl(val):
    return val**0.5

@njit(parallel=True)
def run_steps(pos, vel, mass, n_steps, dt, soft_epsilon):
    for _ in range(n_steps):
        # We need to inline loops or call njit function. 
        # Calling another njit function might have overhead if not inlined well, 
        # but for N-body O(N^2) the inner loop dominates.
        
        # NOTE: For maximum speed in Numba, it is often better to put everything in one big function 
        # or minimal calls. But let's try the function call approach first.
        
        n = pos.shape[0]
        # Re-implementing force loop here for clarity and potential performance (avoiding function call overhead in loop)
        
        # Parallel loop over particles
        for i in prange(n):
            fx = 0.0
            fy = 0.0
            fz = 0.0
            x1 = pos[i, 0]
            y1 = pos[i, 1]
            z1 = pos[i, 2]
            
            for j in range(n):
                # We can skip i==j or just rely on softening.
                # If i==j, dist=soft_eps, force=0 usually
                # But let's strictly skip
                if i == j:
                   continue

                dx = pos[j, 0] - x1
                dy = pos[j, 1] - y1
                dz = pos[j, 2] - z1
                
                dist_sq = dx*dx + dy*dy + dz*dz + soft_epsilon
                dist = dist_sq**0.5
                
                # force scalar
                f = mass[j, 0] / (dist_sq * dist)
                
                fx += f * dx
                fy += f * dy
                fz += f * dz
            
            vel[i, 0] += fx * dt
            vel[i, 1] += fy * dt
            vel[i, 2] += fz * dt
            
        # Update positions
        for i in prange(n):
            pos[i, 0] += vel[i, 0] * dt
            pos[i, 1] += vel[i, 1] * dt
            pos[i, 2] += vel[i, 2] * dt

def run_simulation(n_bodies, n_steps, dt=0.01, soft_epsilon=1e-9):
    np.random.seed(42)
    pos = np.random.uniform(-100, 100, (n_bodies, 3))
    vel = np.random.uniform(-1, 1, (n_bodies, 3))
    mass = np.random.uniform(1, 10, (n_bodies, 1))
    
    # Warmup compilation
    run_steps(pos, vel, mass, 1, dt, soft_epsilon)
    
    start_time = time.time()
    run_steps(pos, vel, mass, n_steps, dt, soft_epsilon)
    end_time = time.time()
    
    return end_time - start_time

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Numba N-body benchmark")
    parser.add_argument("--n", type=int, default=100, help="Number of bodies")
    parser.add_argument("--steps", type=int, default=100, help="Number of steps")
    args = parser.parse_args()

    print(f"Running Numba N-body with N={args.n}, Steps={args.steps}")
    duration = run_simulation(args.n, args.steps)
    print(f"Time: {duration:.4f} seconds")
    print(f"RESULT: {duration}")
