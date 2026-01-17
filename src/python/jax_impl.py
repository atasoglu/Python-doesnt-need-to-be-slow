import argparse
import time
import jax
import jax.numpy as jnp
from jax import jit

@jit
def compute_forces_and_update(pos, vel, mass, dt, soft_epsilon=1e-9):
    # Compute pairwise differences: diff[i,j] = pos[j] - pos[i]
    diff = pos[None, :, :] - pos[:, None, :]
    
    # Distance squared with softening
    dist_sq = jnp.sum(diff**2, axis=2) + soft_epsilon
    dist = jnp.sqrt(dist_sq)
    
    # Force scalar: mass[j] / (dist^3)
    force_scalar = mass.T / (dist_sq * dist)
    
    # Total acceleration: sum over j
    acc = jnp.sum(force_scalar[..., None] * diff, axis=1)
    
    # Update velocity and position (semi-implicit Euler)
    new_vel = vel + acc * dt
    new_pos = pos + new_vel * dt
    
    return new_pos, new_vel

def run_simulation(n_bodies, n_steps, dt=0.01):
    # Initialize bodies
    key = jax.random.PRNGKey(42)
    key1, key2, key3 = jax.random.split(key, 3)
    
    pos = jax.random.uniform(key1, (n_bodies, 3), minval=-100, maxval=100)
    vel = jax.random.uniform(key2, (n_bodies, 3), minval=-1, maxval=1)
    mass = jax.random.uniform(key3, (n_bodies, 1), minval=1, maxval=10)
    
    # JIT compile the function
    step_fn = jit(compute_forces_and_update)
    
    start_time = time.time()
    
    for _ in range(n_steps):
        pos, vel = step_fn(pos, vel, mass, dt)
    
    # Block until computation is complete
    pos.block_until_ready()
    
    end_time = time.time()
    return end_time - start_time

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="JAX N-body benchmark")
    parser.add_argument("--n", type=int, default=100, help="Number of bodies")
    parser.add_argument("--steps", type=int, default=100, help="Number of steps")
    args = parser.parse_args()

    print(f"Running JAX N-body with N={args.n}, Steps={args.steps}")
    duration = run_simulation(args.n, args.steps)
    print(f"Time: {duration:.4f} seconds")
    print(f"RESULT: {duration}")