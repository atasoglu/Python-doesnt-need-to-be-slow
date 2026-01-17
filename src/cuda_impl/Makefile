NVCC = nvcc
NVCC_FLAGS = -O3 -arch=sm_70

TARGET = nbody_cuda
SRC = nbody.cu

all: $(TARGET)

$(TARGET): $(SRC)
	$(NVCC) $(NVCC_FLAGS) -o $(TARGET) $(SRC)

clean:
	rm -f $(TARGET)
