# Python Doesn't Need To Be Slow

Welcome to the **Python Speed-Up Benchmark** project! 

The goal of this repository is to explore and compare various methods for accelerating Python code, using the classic **N-Body Simulation** as our test case. We also include native implementations in C, C++, and Rust to serve as a high-performance baseline.

## 🌌 The Problem: N-Body Simulation

An N-body simulation calculates the gravitational interaction between $N$ bodies. The computational complexity of the naive algorithm is $O(N^2)$, making it computationally expensive and a perfect candidate for optimization.

We simulate particles in a 3D space, calculating forces, velocities, and positions at each time step.

## 🏎️ Implementations

We have implemented the simulation using the following technologies:

### Python Ecosystem
1.  **Vanilla Python** 🐍
    - Reference implementation using standard lists and classes.
    - *Pros*: easy to read. *Cons*: very slow due to interpreter overhead.
2.  **NumPy** 🔢
    - Uses vectorized operations to push loops to C level.
    - *Pros*: cleaner code, significant speedup.
3.  **Numba** ⚡
    - JIT (Just-In-Time) compiler that translates Python functions to optimized machine code.
    - *Pros*: near-native speed with minimal code changes.
4.  **Taichi Lang** ☯️
    - A high-performance compiler for computer graphics and simulation.
    - *Pros*: extremely fast, parallelizes on CPU/GPU automatically.
5.  **Cython** ⚙️
    - Compiles Python-like code to C extensions.
    - *Pros*: robust, widely used. *Cons*: requires separate build step.
6.  **Multiprocessing** 🧵
    - Uses multiple CPU cores to parallelize the workload.
    - *Pros*: utilizes hardware. *Cons*: high overhead for process communication.

### Native Baselines
These serve as the "speed limit" to see how close our Python optimizations can get to raw machine performance.
- **Rust** 🦀 (Safe, concurrent, fast)
- **C** (The classic standard)
- **C++** (High-performance object-oriented)

## 📊 Benchmarking & Analysis

We provide a comprehensive analysis notebook to verify our results.
👉 **[View Analysis Notebook](notebooks/analysis.ipynb)**

The notebook automatically aggregates results from all runs (`results/results_*.json`) and provides visualizations comparing execution time and speedup factors.

## 🛠️ How to Run

### prerequisites
- **Python 3.11+**
- **Docker** (Optional, for reproducible builds)
- For generic local run: `g++`, `gcc`, `rustc` / `cargo` (if running native benchmarks locally)

### Option 1: Using Docker (Recommended)

We have Dockerfiles for each environment to ensure reproducibility.

**Rust Implementation:**
```bash
# Build the image (uses multi-stage build)
docker build -f docker/rust.Dockerfile -t nbody-rust .

# Run the benchmark
docker run --rm nbody-rust
```

**Python Implementations:**
```bash
# Build
docker build -f docker/python.Dockerfile -t nbody-python .

# Run
docker run --rm nbody-python
```

### Option 2: Running Locally

1.  **Install Python Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Build Native Binaries (Optional):**
    If you have `gcc` and `cargo` installed:
    ```bash
    ./build_native.bat
    ```

3.  **Run Benchmarks:**
    Use the runner script to execute specific or all benchmarks.
    ```bash
    # Run all
    python bench_runner.py --type all

    # Run specific type
    python bench_runner.py --type python --n 100 1000
    ```

## 📂 Project Structure

- `src/`: Source code for all implementations.
    - `src/python/`: Python variants (numpy, numba, etc.).
    - `src/rust_impl/`: Rust Cargo project.
    - `src/c_impl/`: C source.
    - `src/cpp_impl/`: C++ source.
- `docker/`: Dockerfiles.
- `notebooks/`: analysis.ipynb and data visualization.
- `results/`: JSON output from benchmarks.

---
*Happy Optimizing!*
