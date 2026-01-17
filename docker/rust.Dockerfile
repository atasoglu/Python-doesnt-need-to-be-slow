FROM rust:1-slim-bookworm AS builder

WORKDIR /build
COPY src/rust_impl .
RUN cargo build --release

FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app"

WORKDIR /app

# Copy the compiled binary from the builder stage
COPY --from=builder /build/target/release/nbody_rust /app/src/rust_impl/target/release/nbody_rust

COPY bench_runner.py .

CMD ["python", "bench_runner.py", "--type", "rust"]
