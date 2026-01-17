FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app:/app/src/python"

# Runtime deps for Taichi and build deps for Cython
# Enable non-free repositories for nvidia-cuda-toolkit
RUN sed -i 's/main/main contrib non-free non-free-firmware/' /etc/apt/sources.list.d/debian.sources && \
    apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libtbb-dev \
    libx11-6 \
    libgl1 \
    pypy3 \
    nvidia-cuda-toolkit \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Build Cython
COPY src/python /app/src/python
WORKDIR /app/src/python
RUN python setup_cython.py build_ext --inplace

WORKDIR /app
COPY bench_runner.py .

# Fix Taichi
RUN ln -sf /usr/lib/x86_64-linux-gnu/libtbb.so.12 /usr/lib/x86_64-linux-gnu/libtbb.so.2 || true

CMD ["python", "bench_runner.py", "--type", "python"]
