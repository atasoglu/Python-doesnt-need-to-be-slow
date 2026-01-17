import argparse
import time
import numpy as np

def run_simulation(n_bodies, n_steps, dt=0.01, soft_epsilon=1e-9):
    # Initialize bodies
    np.random.seed(42)
    pos = np.random.uniform(-100, 100, (n_bodies, 3))
    vel = np.random.uniform(-1, 1, (n_bodies, 3))
    mass = np.random.uniform(1, 10, (n_bodies, 1))
    
    start_time = time.time()
    
    for _ in range(n_steps):
        # Compute forces using broadcasting
        # pos is (N, 3)
        # We need pairwise differences.
        # reshape pos for broadcasting:
        # pos[:, None, :] is (N, 1, 3)
        # pos[None, :, :] is (1, N, 3)
        # diff will be (N, N, 3) -> displacement vector from j to i
        
        # r_ij = r_j - r_i 
        # But we want force ON i FROM j. 
        # F_ij = G * m_i * m_j / |r_ij|^3 * r_ij
        # Let's say we calculate force on i. Sum over j.
        
        # diff = pos_j - pos_i
        # diff[i, j] = pos[j] - pos[i]
        diff = pos[None, :, :] - pos[:, None, :] 
        
        # dist_sq = dx^2 + dy^2 + dz^2
        # diff is (N, N, 3), squred is (N, N, 3), sum over axis 2 -> (N, N)
        dist_sq = np.sum(diff**2, axis=2) + soft_epsilon
        
        # dist = sqrt(dist_sq)
        dist = np.sqrt(dist_sq) # (N, N)
        
        # Force magnitude (without G, just proportional part): M_j / (dist^3)
        # We need to broadcast mass. Mass is (N, 1).
        # We want mass[j] for each element (i, j).
        # mass.T is (1, N).
        force_scalar = mass.T / (dist_sq * dist) # (N, N)
        
        # Fill diagonal with 0 to avoid self-interaction (though dist_sq handles NaN/Inf usually with softening, but explicit 0 is safer/cleaner)
        # Actually, self-force is 0 distance -> soft_epsilon -> non-zero but small. 
        # But diff is 0, so force vector is 0. So it's fine.
        
        # Total acceleration: sum(force_scalar * diff) over j
        # diff is (N, N, 3). force_scalar is (N, N).
        # force_scalar[..., None] is (N, N, 1)
        acc = np.sum(force_scalar[..., None] * diff, axis=1) # (N, 3)
        
        # Update velocity (semi-implicit Euler)
        vel += acc * dt
        
        # Update position
        pos += vel * dt
        
    end_time = time.time()
    return end_time - start_time

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NumPy N-body benchmark")
    parser.add_argument("--n", type=int, default=100, help="Number of bodies")
    parser.add_argument("--steps", type=int, default=100, help="Number of steps")
    args = parser.parse_args()

    print(f"Running NumPy N-body with N={args.n}, Steps={args.steps}")
    duration = run_simulation(args.n, args.steps)
    print(f"Time: {duration:.4f} seconds")
    print(f"RESULT: {duration}")
