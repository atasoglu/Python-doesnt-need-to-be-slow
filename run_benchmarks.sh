#!/bin/bash

FORCE_BUILD=0
if [ "$1" = "--force" ]; then
    FORCE_BUILD=1
fi

echo "Creating results directory..."
mkdir -p results

echo
echo "=========================================="
echo "Building and Running Python Benchmarks..."
echo "=========================================="
SHOULD_BUILD=0
if [ "$FORCE_BUILD" = "1" ]; then
    SHOULD_BUILD=1
elif ! docker image inspect nbody-python >/dev/null 2>&1; then
    SHOULD_BUILD=1
fi

if [ "$SHOULD_BUILD" = "0" ]; then
    echo "Image nbody-python found, skipping build."
else
    echo "Building nbody-python..."
    docker build -f docker/python.Dockerfile -t nbody-python .
    if [ $? -ne 0 ]; then exit $?; fi
fi
docker run --rm -v "$(pwd)/results:/app/results" nbody-python

echo
echo "=========================================="
echo "Building and Running C/C++ Benchmarks..."
echo "=========================================="
SHOULD_BUILD=0
if [ "$FORCE_BUILD" = "1" ]; then
    SHOULD_BUILD=1
elif ! docker image inspect nbody-c-cpp >/dev/null 2>&1; then
    SHOULD_BUILD=1
fi

if [ "$SHOULD_BUILD" = "0" ]; then
    echo "Image nbody-c-cpp found, skipping build."
else
    echo "Building nbody-c-cpp..."
    docker build -f docker/c_cpp.Dockerfile -t nbody-c-cpp .
    if [ $? -ne 0 ]; then exit $?; fi
fi
docker run --rm -v "$(pwd)/results:/app/results" nbody-c-cpp

echo
echo "=========================================="
echo "Building and Running Rust Benchmarks..."
echo "=========================================="
SHOULD_BUILD=0
if [ "$FORCE_BUILD" = "1" ]; then
    SHOULD_BUILD=1
elif ! docker image inspect nbody-rust >/dev/null 2>&1; then
    SHOULD_BUILD=1
fi

if [ "$SHOULD_BUILD" = "0" ]; then
    echo "Image nbody-rust found, skipping build."
else
    echo "Building nbody-rust..."
    docker build -f docker/rust.Dockerfile -t nbody-rust .
    if [ $? -ne 0 ]; then exit $?; fi
fi
docker run --rm -v "$(pwd)/results:/app/results" nbody-rust

echo
echo "=========================================="
echo "Building and Running Go Benchmarks..."
echo "=========================================="
SHOULD_BUILD=0
if [ "$FORCE_BUILD" = "1" ]; then
    SHOULD_BUILD=1
elif ! docker image inspect nbody-go >/dev/null 2>&1; then
    SHOULD_BUILD=1
fi

if [ "$SHOULD_BUILD" = "0" ]; then
    echo "Image nbody-go found, skipping build."
else
    echo "Building nbody-go..."
    docker build -f docker/go.Dockerfile -t nbody-go .
    if [ $? -ne 0 ]; then exit $?; fi
fi
docker run --rm -v "$(pwd)/results:/app/results" nbody-go

echo
echo "=========================================="
echo "All Benchmarks Completed!"
echo "Results saved to results/latest_run.json"
echo "=========================================="
