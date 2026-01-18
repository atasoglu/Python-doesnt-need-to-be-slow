import argparse
import random
import time
import math
from typing import List, final

@final
class Planet:
    def __init__(self, x: float, y: float, z: float, vx: float, vy: float, vz: float, mass: float) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.mass = mass

def compute_forces(planets: List[Planet], dt: float, soft_epsilon: float = 1e-9) -> None:
    # This is the O(N^2) part
    n = len(planets)
    for i in range(n):
        p1 = planets[i]
        fx = 0.0
        fy = 0.0
        fz = 0.0
        for j in range(n):
            if i == j:
                continue
            p2 = planets[j]
            dx = p2.x - p1.x
            dy = p2.y - p1.y
            dz = p2.z - p1.z
            dist_sq = dx*dx + dy*dy + dz*dz + soft_epsilon
            dist = math.sqrt(dist_sq)
            f = p2.mass / (dist_sq * dist)
            fx += f * dx
            fy += f * dy
            fz += f * dz
        
        # Update velocities (semi-implicit Euler part 1)
        p1.vx += fx * dt
        p1.vy += fy * dt
        p1.vz += fz * dt

def update_positions(planets: List[Planet], dt: float) -> None:
    # Update positions (semi-implicit Euler part 2)
    for p in planets:
        p.x += p.vx * dt
        p.y += p.vy * dt
        p.z += p.vz * dt

def run_simulation(n_bodies: int, n_steps: int, dt: float = 0.01) -> float:
    planets: List[Planet] = []
    # Initialize random planets
    random.seed(42)
    for _ in range(n_bodies):
        planets.append(Planet(
            x=random.uniform(-100, 100),
            y=random.uniform(-100, 100),
            z=random.uniform(-100, 100),
            vx=random.uniform(-1, 1),
            vy=random.uniform(-1, 1),
            vz=random.uniform(-1, 1),
            mass=random.uniform(1, 10)
        ))

    start_time = time.time()
    
    for _ in range(n_steps):
        compute_forces(planets, dt)
        update_positions(planets, dt)
        
    end_time = time.time()
    return end_time - start_time

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MyPyc Python N-body benchmark")
    parser.add_argument("--n", type=int, default=100, help="Number of bodies")
    parser.add_argument("--steps", type=int, default=100, help="Number of steps")
    args = parser.parse_args()

    print(f"Running MyPyc Python N-body with N={args.n}, Steps={args.steps}")
    duration = run_simulation(args.n, args.steps)
    print(f"Time: {duration:.4f} seconds")
    # Output for simple parsing
    print(f"RESULT: {duration}")
