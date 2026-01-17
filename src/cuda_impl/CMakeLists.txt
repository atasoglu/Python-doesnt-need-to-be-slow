cmake_minimum_required(VERSION 3.18)
project(NBodyCUDA LANGUAGES CUDA CXX)

set(CMAKE_CUDA_ARCHITECTURES 70)

add_executable(nbody_cuda nbody.cu)

target_compile_options(nbody_cuda PRIVATE -O3)
