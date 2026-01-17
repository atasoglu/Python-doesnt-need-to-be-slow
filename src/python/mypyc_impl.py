import argparse
import random
import time
import math
from typing import List, Tuple

def compute_forces(
    positions: List[Tuple[float, float, float]], 
    masses: List[float], 
    velocities: List[Tuple[float, float, float]], 
    dt: float
) -> List[Tuple[float, float, float]]:
    n = len(positions)
    new_velocities: List[Tuple[float, float, float]] = []
    
    for i in range(n):
        x1, y1, z1 = positions[i]
        vx, vy, vz = velocities[i]
        fx = 0.0
        fy = 0.0
        fz = 0.0
        
        for j in range(n):
            if i == j:
                continue
            x2, y2, z2 = positions[j]
            dx = x2 - x1
            dy = y2 - y1
            dz = z2 - z1
            dist_sq = dx*dx + dy*dy + dz*dz + 1e-9
            dist = math.sqrt(dist_sq)
            f = masses[j] / (dist_sq * dist)
            fx += f * dx
            fy += f * dy
            fz += f * dz
        
        new_velocities.append((vx + fx * dt, vy + fy * dt, vz + fz * dt))
    
    return new_velocities

def update_positions(
    positions: List[Tuple[float, float, float]], 
    velocities: List[Tuple[float, float, float]], 
    dt: float
) -> List[Tuple[float, float, float]]:
    new_positions: List[Tuple[float, float, float]] = []
    
    for i in range(len(positions)):
        x, y, z = positions[i]
        vx, vy, vz = velocities[i]
        new_positions.append((x + vx * dt, y + vy * dt, z + vz * dt))
    
    return new_positions

def run_simulation(n_bodies: int, n_steps: int, dt: float = 0.01) -> float:
    # Initialize with separate lists for better optimization
    positions: List[Tuple[float, float, float]] = []
    velocities: List[Tuple[float, float, float]] = []
    masses: List[float] = []
    
    random.seed(42)
    for _ in range(n_bodies):
        positions.append((
            random.uniform(-100, 100),
            random.uniform(-100, 100), 
            random.uniform(-100, 100)
        ))
        velocities.append((
            random.uniform(-1, 1),
            random.uniform(-1, 1),
            random.uniform(-1, 1)
        ))
        masses.append(random.uniform(1, 10))

    start_time = time.time()
    
    for _ in range(n_steps):
        velocities = compute_forces(positions, masses, velocities, dt)
        positions = update_positions(positions, velocities, dt)
        
    end_time = time.time()
    return end_time - start_time

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Optimized Python N-body benchmark")
    parser.add_argument("--n", type=int, default=100, help="Number of bodies")
    parser.add_argument("--steps", type=int, default=100, help="Number of steps")
    args = parser.parse_args()

    duration = run_simulation(args.n, args.steps)
    print(f"RESULT: {duration}")