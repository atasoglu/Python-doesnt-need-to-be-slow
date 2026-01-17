import argparse
import time
import taichi as ti
import numpy as np

# Initialize Taichi
# Using cpu for fairness comparison with others initially, but can be switched to gpu
ti.init(arch=ti.cpu) 

@ti.data_oriented
class NBodyTaichi:
    def __init__(self, n_bodies, dt=0.01, soft_epsilon=1e-9):
        self.n = n_bodies
        self.dt = dt
        self.soft_epsilon = soft_epsilon
        
        self.pos = ti.Vector.field(3, dtype=ti.f64, shape=self.n)
        self.vel = ti.Vector.field(3, dtype=ti.f64, shape=self.n)
        self.mass = ti.field(dtype=ti.f64, shape=self.n)

    def initialize(self):
        np.random.seed(42)
        pos_np = np.random.uniform(-100, 100, (self.n, 3))
        vel_np = np.random.uniform(-1, 1, (self.n, 3))
        mass_np = np.random.uniform(1, 10, (self.n,))
        
        self.pos.from_numpy(pos_np)
        self.vel.from_numpy(vel_np)
        self.mass.from_numpy(mass_np)

    @ti.kernel
    def compute_step(self):
        for i in range(self.n):
            fx = 0.0
            fy = 0.0
            fz = 0.0
            p1 = self.pos[i]
            
            for j in range(self.n):
                if i != j:
                    p2 = self.pos[j]
                    disp = p2 - p1
                    dist_sq = disp.norm_sqr() + self.soft_epsilon
                    dist = ti.sqrt(dist_sq)
                    f = self.mass[j] / (dist_sq * dist)
                    
                    fx += f * disp[0]
                    fy += f * disp[1]
                    fz += f * disp[2]
            
            self.vel[i] += ti.Vector([fx, fy, fz]) * self.dt
            
        for i in range(self.n):
            self.pos[i] += self.vel[i] * self.dt

    def run(self, steps):
        for _ in range(steps):
            self.compute_step()

def run_simulation(n_bodies, n_steps, dt=0.01):
    sim = NBodyTaichi(n_bodies, dt)
    sim.initialize()
    
    # Warmup (JIT compilation)
    sim.run(1)
    
    ti.sync()
    start_time = time.time()
    sim.run(n_steps)
    ti.sync()
    end_time = time.time()
    
    return end_time - start_time

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Taichi N-body benchmark")
    parser.add_argument("--n", type=int, default=100, help="Number of bodies")
    parser.add_argument("--steps", type=int, default=100, help="Number of steps")
    args = parser.parse_args()

    print(f"Running Taichi N-body with N={args.n}, Steps={args.steps}")
    duration = run_simulation(args.n, args.steps)
    print(f"Time: {duration:.4f} seconds")
    print(f"RESULT: {duration}")
