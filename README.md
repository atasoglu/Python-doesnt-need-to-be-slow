# Python Doesn't Need To Be Slow

Welcome to the **Python Speed-Up Benchmark** project! 

The goal of this repository is to explore and compare various methods for accelerating Python code, using the classic **N-Body Simulation** as our test case. We also include native implementations in C, C++, and Rust to serve as a high-performance baseline.

## The Problem: N-Body Simulation

An [N-body simulation](https://en.wikipedia.org/wiki/N-body_simulation) calculates the gravitational interaction between $N$ bodies. The computational complexity of the naive algorithm is $O(N^2)$, making it computationally expensive and a perfect candidate for optimization.

We simulate particles in a 3D space, calculating forces, velocities, and positions at each time step.

### Complexity & Parallelism

The naive pairwise approach involves $O(N^2)$ calculations. As $N$ grows, the workload increases quadratically (doubling $N$ means $4\times$ the work).

*   **Serial Execution**: Inefficient for large $N$. Performance is strictly bound by single-core clock speed and instruction throughput.
*   **Parallel Execution**: The problem is "embarrassingly parallel" because the force on each body is independent of the others for a given step. Using multi-core CPUs or thousands of GPU cores allows for massive speedups, especially as $N$ becomes large enough to saturate the hardware.

**Behavior at Different Scales:**

*   **Small N**: For small inputs, the overhead of managing threads (Multiprocessing) or transferring data to GPU (CUDA) often outweighs the computational benefits. In these cases, optimized **Serial** or **Vectorized** (NumPy) implementations may actually be faster.
*   **Large N**: As $N$ increases, the $O(N^2)$ complexity dominates. Serial implementations slow down drastically. **Parallel** implementations shine here, as they can distribute the massive calculation load across many cores, making the overhead negligible compared to the computation time.

### Simplified Core Logic (Python)

```python
# 1. Update velocities based on forces
for a in bodies:
    for b in bodies:
        if a is b: continue
        
        dx, dy, dz = b.x-a.x, b.y-a.y, b.z-a.z
        f = b.mass / (dx**2 + dy**2 + dz**2)**1.5 * dt
        
        a.vx += dx * f; a.vy += dy * f; a.vz += dz * f

# 2. Update positions
for a in bodies:
    a.x += a.vx * dt; a.y += a.vy * dt; a.z += a.vz * dt
```

## Implementations

We have implemented the simulation using the following technologies:

### Python Ecosystem

1.  **Vanilla Python**
    - Reference implementation using standard lists and classes.
    - *Pros*: easy to read. *Cons*: very slow due to interpreter overhead.
2.  **NumPy**
    - Uses vectorized operations to push loops to C level.
    - *Pros*: cleaner code, significant speedup.
3.  **Numba**
    - JIT (Just-In-Time) compiler that translates Python functions to optimized machine code.
    - *Pros*: near-native speed, supports **automatic multi-core parallelism** (CPU) with simple flags.
4.  **JAX**
    - Google's NumPy-compatible library with JIT compilation and functional programming.
    - *Pros*: XLA compilation, supports **automatic vectorization & parallelism** (SIMD/Multi-device), GPU support.
5.  **Taichi Lang**
    - A high-performance compiler for computer graphics and simulation.
    - *Pros*: extremely fast, **automatically parallelizes** workloads across all available CPU cores or GPU.
6.  **Cython**
    - Compiles Python-like code to C extensions.
    - *Pros*: robust, widely used. *Cons*: requires separate build step.
7.  **MyPyc**
    - MyPy's compiler that translates type-annotated Python to C extensions.
    - *Pros*: significant speedup with minimal code changes, leverages existing type hints.
8.  **PyPy**
    - Alternative Python implementation with a JIT (Just-In-Time) compiler.
    - *Pros*: significant speedup for pure Python code with no code changes required.
9.  **Multiprocessing**
    - Uses multiple CPU cores to parallelize the workload.
    - *Pros*: utilizes hardware. *Cons*: high overhead for process communication.

### Native Baselines

These serve as the "speed limit" to see how close our Python optimizations can get to raw machine performance.

- **Rust**
- **C**
- **C++**
- **Go**

### GPU/CUDA Implementation

- **CUDA C++**
  - Explicit GPU parallelization using NVIDIA CUDA
  - Requires NVIDIA GPU with Compute Capability 3.5+
  - *Pros*: Massive parallelization, 10-100x speedup for large N
  - *Cons*: Requires NVIDIA GPU, complex memory management

#### GPU Requirements
- NVIDIA GPU with CUDA support
- CUDA Toolkit 11.0+
- Docker with nvidia-docker2 support

#### Running with GPU:
```bash
# Requires --gpus flag
docker run --gpus all nbody-cuda
```

## How to Run

> **Note:** Ensure you have Docker installed on your machine to run the benchmarks seamlessly.

Use the runner script to execute all benchmarks.

```bash
# Windows
.\run_benchmarks.bat

# Linux / macOS
./run_benchmarks.sh
```

To force rebuild all Docker images, use the `--force` flag.

## Results

After running the benchmarks, you can analyze the results using our analysis script:

```bash
python analysis.py
```

This generates performance comparison charts in the `figures/` directory.

### Performance Comparison

![Execution Time](figures/execution_time.png)

*Execution time comparison across different methods and problem sizes (N-body count)*

![Speedup Factor](figures/speedup_factor.png)

*Speedup factor relative to vanilla Python implementation*

---

*Happy Optimizing!*
