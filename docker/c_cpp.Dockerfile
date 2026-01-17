FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app"

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY src/c_impl /app/src/c_impl
COPY src/cpp_impl /app/src/cpp_impl
RUN gcc -O3 -o src/c_impl/nbody src/c_impl/nbody.c -lm && \
    g++ -O3 -o src/cpp_impl/nbody src/cpp_impl/nbody.cpp

COPY bench_runner.py .

CMD ["python", "bench_runner.py", "--type", "c_cpp"]
