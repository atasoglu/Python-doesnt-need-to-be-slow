import argparse
import time
import math
import random
import multiprocessing

# We need a worker function that can be pickled
# The strategy: Split the outer loop (i) among processes.
# Workers need:
# - subset of 'i' indices to process
# - copy of all planet data (read-only for position/mass)
# - return: partial velocity updates or new positions?

# Simpler logic for MP:
# - Master holds state.
# - Each step:
#   - Share positions/masses with workers (via shared memory or copy)
#   - Workers compute forces for chunk of particles
#   - Master collects forces/accelerations
#   - Master updates positions
# This has high overhead per step due to IPC.
# Better: Workers do N steps independently? No, they interact.
# So "Synchronous" step-by-step is needed.
# For N=200, overhead dominates. For N=5000, maybe better.

class PlanetData:
    def __init__(self, x, y, z, vx, vy, vz, mass):
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.mass = mass

def compute_chunk_force(start_idx, end_idx, all_planets, dt, soft_epsilon=1e-9):
    # This runs in a worker process
    # all_planets is list of simple objects or dicts
    # Return list of (vx_inc, vy_inc, vz_inc) for the chunk
    
    n = len(all_planets)
    updates = []
    
    for i in range(start_idx, end_idx):
        p1 = all_planets[i]
        fx = 0.0
        fy = 0.0
        fz = 0.0
        
        # Optimization: Local variables for p1
        p1x, p1y, p1z = p1.x, p1.y, p1.z
        
        for j in range(n):
            if i == j:
                continue
            
            p2 = all_planets[j]
            dx = p2.x - p1x
            dy = p2.y - p1y
            dz = p2.z - p1z
            
            dist_sq = dx*dx + dy*dy + dz*dz + soft_epsilon
            dist = math.sqrt(dist_sq)
            f = p2.mass / (dist_sq * dist)
            
            fx += f * dx
            fy += f * dy
            fz += f * dz
        
        updates.append((fx * dt, fy * dt, fz * dt))
        
    return updates

def run_simulation(n_bodies, n_steps, dt=0.01, n_processes=None):
    if n_processes is None:
        n_processes = multiprocessing.cpu_count()
        
    # Initialize random planets
    random.seed(42)
    planets = []
    for _ in range(n_bodies):
        planets.append(PlanetData(
            x=random.uniform(-100, 100),
            y=random.uniform(-100, 100),
            z=random.uniform(-100, 100),
            vx=random.uniform(-1, 1),
            vy=random.uniform(-1, 1),
            vz=random.uniform(-1, 1),
            mass=random.uniform(1, 10)
        ))

    # Prepare chunks
    chunk_size = (n_bodies + n_processes - 1) // n_processes
    ranges = []
    for i in range(n_processes):
        start = i * chunk_size
        end = min((i + 1) * chunk_size, n_bodies)
        if start < end:
            ranges.append((start, end))
            
    start_time = time.time()
    
    with multiprocessing.Pool(processes=n_processes) as pool:
        for _ in range(n_steps):
            # Parallel Force Calculation
            # We must pass 'planets' to all. This pickling is slow.
            # Using shared memory is better but complex for vanilla "multiprocessing" benchmark.
            # We stick to standard Pool.map for simplicity of implementation, acknowledging overhead.
            
            # Create tasks
            tasks = [(r[0], r[1], planets, dt) for r in ranges]
            
            # Map
            results = pool.starmap(compute_chunk_force, tasks)
            
            # Collect and update
            # results is list of lists of (vx_d, vy_d, vz_d)
            flat_updates = [item for sublist in results for item in sublist]
            
            # Apply velocity updates
            for i, (dvx, dvy, dvz) in enumerate(flat_updates):
                p = planets[i]
                p.vx += dvx
                p.vy += dvy
                p.vz += dvz
            
            # Update positions (fast enough to do single threaded)
            for p in planets:
                p.x += p.vx * dt
                p.y += p.vy * dt
                p.z += p.vz * dt
                
    end_time = time.time()
    return end_time - start_time

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multiprocessing N-body benchmark")
    parser.add_argument("--n", type=int, default=100, help="Number of bodies")
    parser.add_argument("--steps", type=int, default=100, help="Number of steps")
    parser.add_argument("--procs", type=int, default=None, help="Number of processes")
    args = parser.parse_args()

    print(f"Running MP N-body with N={args.n}, Steps={args.steps}, Procs={args.procs}")
    duration = run_simulation(args.n, args.steps, n_processes=args.procs)
    print(f"Time: {duration:.4f} seconds")
    print(f"RESULT: {duration}")
