import argparse
import sys
import os

# Ensure the compiled module is in path
sys.path.append(os.path.join(os.getcwd(), 'src', 'python'))

# Try importing the compiled module.
# If build_ext --inplace was run in root, it might be in src/python or root depending on setup.py
# Our setup.py says "src/python/cython_impl.pyx", so typically it builds in place next to it.
# So we need to be careful about import.
try:
    # If running from root, and file is src/python/cython_impl.clike...
    # We should add src/python to path
    import cython_impl
except ImportError:
    try:
        from src.python import cython_impl
    except ImportError:
        print("Error: Could not import cython_impl. Make sure to compile it first.")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cython N-body benchmark")
    parser.add_argument("--n", type=int, default=100, help="Number of bodies")
    parser.add_argument("--steps", type=int, default=100, help="Number of steps")
    args = parser.parse_args()

    print(f"Running Cython N-body with N={args.n}, Steps={args.steps}")
    duration = cython_impl.run_simulation(args.n, args.steps)
    print(f"Time: {duration:.4f} seconds")
    print(f"RESULT: {duration}")
