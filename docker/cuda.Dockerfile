FROM nvidia/cuda:12.0.1-devel-ubuntu22.04 AS builder

# Install nvidia-smi for GPU detection
RUN apt-get update && apt-get install -y nvidia-utils-525

WORKDIR /build
COPY src/cuda_impl .
RUN nvcc -O3 -arch=sm_70 -o nbody_cuda nbody.cu

FROM nvidia/cuda:12.0.1-runtime-ubuntu22.04
WORKDIR /app

# Install Python for the benchmark runner
RUN apt-get update && apt-get install -y python3 python-is-python3

COPY --from=builder /build/nbody_cuda /app/src/cuda_impl/nbody_cuda
COPY bench_runner.py .

# Test GPU availability
RUN nvidia-smi || echo "No GPU detected in container"

CMD ["python", "bench_runner.py", "--type", "cuda"]
