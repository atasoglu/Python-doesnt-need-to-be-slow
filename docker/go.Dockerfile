FROM golang:1.21-bookworm AS builder

WORKDIR /build
COPY src/go_impl .
RUN go build -o nbody_go main.go

FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app"

WORKDIR /app

# Copy the compiled binary from the builder stage
COPY --from=builder /build/nbody_go /app/src/go_impl/nbody_go

COPY bench_runner.py .

CMD ["python", "bench_runner.py", "--type", "go"]