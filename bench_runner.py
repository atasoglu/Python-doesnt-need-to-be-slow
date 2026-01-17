import subprocess
import json
import platform
import os
import sys
import argparse

def get_system_info():
    processor = platform.processor()
    if not processor:
        try:
            if platform.system() == "Linux":
                with open("/proc/cpuinfo", "r") as f:
                    for line in f:
                        if "model name" in line:
                            processor = line.split(":")[1].strip()
                            break
            elif platform.system() == "Windows":
                import subprocess
                result = subprocess.run(["wmic", "cpu", "get", "name"], capture_output=True, text=True)
                lines = result.stdout.strip().split("\n")
                if len(lines) > 1:
                    processor = lines[1].strip()
        except:
            processor = "Unknown"
    
    return {
        "os": platform.system(),
        "release": platform.release(),
        "python": platform.python_version(),
        "processor": processor or "Unknown",
    }

def run_benchmark(command, name, n, steps):
    print(f"Benchmarking {name} (N={n}, Steps={steps})...")
    try:
        # Construct command
        cmd = command + [f"--n", str(n), f"--steps", str(steps)]
        
        # Run process
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            check=True
        )
        
        # Parse output for "RESULT: <float>"
        for line in result.stdout.splitlines():
            if line.startswith("RESULT: "):
                return float(line.split("RESULT: ")[1])
        return None
    except subprocess.CalledProcessError as e:
        print(f"Error running {name}: {e}")
        # print(e.stderr) # Optional: print stderr
        return None
    except FileNotFoundError:
        print(f"Executable not found for {name}: {command[0]}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run N-body benchmarks")
    parser.add_argument("--type", choices=["all", "python", "c_cpp", "rust"], default="all", help="Type of benchmarks to run")
    parser.add_argument("--n", type=int, nargs="+", default=[100, 1000], help="N values to test")
    parser.add_argument("--steps", type=int, default=50, help="Number of steps")
    args = parser.parse_args()

    # Configuration
    N_VALUES = args.n
    STEPS = args.steps
    
    # List of implementations to test
    # (command_list, name, type)
    all_implementations = [
        (["python", "src/python/baseline.py"], "Vanilla Python", "python"),
        (["python", "src/python/numpy_impl.py"], "NumPy", "python"),
        (["python", "src/python/numba_impl.py"], "Numba", "python"),
        (["python", "src/python/taichi_impl.py"], "Taichi", "python"),
        (["python", "src/python/cython_runner.py"], "Cython", "python"),
        (["python", "src/python/mypyc_runner.py"], "MyPyc", "python"),
        (["python", "src/python/mp_impl.py"], "Multiprocessing", "python"),
        # Native binaries
        (["src/rust_impl/target/release/nbody_rust.exe"] if os.name == 'nt' else ["./src/rust_impl/target/release/nbody_rust"], "Rust (Native)", "rust"),
        (["src/c_impl/nbody.exe"] if os.name == 'nt' else ["./src/c_impl/nbody"], "C (Native)", "c_cpp"),
        (["src/cpp_impl/nbody.exe"] if os.name == 'nt' else ["./src/cpp_impl/nbody"], "C++ (Native)", "c_cpp"),
    ]
    
    # Filter implementations
    if args.type == "all":
        implementations = all_implementations
    else:
        implementations = [i for i in all_implementations if i[2] == args.type]

    new_results = []
    
    for n in N_VALUES:
        for cmd, name, _ in implementations:
            time_taken = run_benchmark(cmd, name, n, STEPS)
            if time_taken is not None:
                new_results.append({
                    "method": name,
                    "n": n,
                    "steps": STEPS,
                    "time": time_taken
                })
            else:
                print(f"Skipping {name} due to failure.")
    
    # Save to specific file based on type
    output_filename = f"results_{args.type}.json"
    output_path = os.path.join("results", output_filename)
    os.makedirs("results", exist_ok=True)
    
    final_data = {
        "system": get_system_info(),
        "benchmarks": new_results
    }
            
    print(json.dumps(final_data, indent=2))
    
    with open(output_path, "w") as f:
        json.dump(final_data, f, indent=2)
    print(f"Results saved to {output_path}")

