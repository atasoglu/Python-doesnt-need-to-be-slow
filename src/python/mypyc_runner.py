#!/usr/bin/env python3
"""
Runner for MyPyc compiled N-body simulation
"""

import os
import sys
import subprocess
import argparse

def compile_mypyc():
    """Compile the mypyc implementation if needed"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check if compiled module exists
    import glob
    compiled_files = glob.glob(os.path.join(current_dir, "mypyc_impl*.so")) + \
                    glob.glob(os.path.join(current_dir, "mypyc_impl*.pyd"))
    
    if not compiled_files:
        print("Compiling MyPyc implementation...")
        try:
            # Run the setup script to compile
            result = subprocess.run([
                sys.executable, "setup_mypyc.py", "build_ext", "--inplace"
            ], cwd=current_dir, capture_output=True, text=True, check=True)
            print("MyPyc compilation successful")
        except subprocess.CalledProcessError as e:
            print(f"MyPyc compilation failed: {e}")
            print(f"stdout: {e.stdout}")
            print(f"stderr: {e.stderr}")
            return False
    
    return True

def main():
    parser = argparse.ArgumentParser(description="N-Body simulation with MyPyc")
    parser.add_argument("--n", type=int, default=100, help="Number of bodies")
    parser.add_argument("--steps", type=int, default=50, help="Number of simulation steps")
    args = parser.parse_args()
    
    # Compile if needed
    if not compile_mypyc():
        print("Failed to compile MyPyc implementation, falling back to regular Python")
        # Fall back to regular Python execution
        current_dir = os.path.dirname(os.path.abspath(__file__))
        result = subprocess.run([sys.executable, os.path.join(current_dir, "mypyc_impl.py"), 
                       "--n", str(args.n), "--steps", str(args.steps)], 
                       capture_output=True, text=True)
        print(result.stdout)
        return
    
    # Import and run the compiled module
    try:
        import mypyc_impl
        # Call run_simulation directly from compiled module
        duration = mypyc_impl.run_simulation(args.n, args.steps)
        print(f"RESULT: {duration}")
    except ImportError:
        print("Failed to import compiled module, falling back to regular Python")
        current_dir = os.path.dirname(os.path.abspath(__file__))
        result = subprocess.run([sys.executable, os.path.join(current_dir, "mypyc_impl.py"), 
                       "--n", str(args.n), "--steps", str(args.steps)], 
                       capture_output=True, text=True)
        print(result.stdout)

if __name__ == "__main__":
    main()