# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True

import time
import numpy as np
cimport numpy as np
from libc.math cimport sqrt

# We need to define types for speed
# Using double precision (float64)

def run_simulation(int n_bodies, int n_steps, double dt=0.01, double soft_epsilon=1e-9):
    # Initialize implementation
    # We use typed memoryviews or arrays
    
    # Initialize with numpy
    np.random.seed(42)
    cdef double[:, ::1] pos = np.random.uniform(-100, 100, (n_bodies, 3))
    cdef double[:, ::1] vel = np.random.uniform(-1, 1, (n_bodies, 3))
    cdef double[::1] mass = np.random.uniform(1, 10, (n_bodies,))
    
    cdef int i, j, step
    cdef double fx, fy, fz
    cdef double dx, dy, dz
    cdef double dist_sq, dist, f
    cdef double p1_x, p1_y, p1_z
    
    start_time = time.time()
    
    with nogil:
        for step in range(n_steps):
            for i in range(n_bodies):
                fx = 0.0
                fy = 0.0
                fz = 0.0
                p1_x = pos[i, 0]
                p1_y = pos[i, 1]
                p1_z = pos[i, 2]
                
                for j in range(n_bodies):
                    if i == j:
                        continue
                    
                    dx = pos[j, 0] - p1_x
                    dy = pos[j, 1] - p1_y
                    dz = pos[j, 2] - p1_z
                    
                    dist_sq = dx*dx + dy*dy + dz*dz + soft_epsilon
                    dist = sqrt(dist_sq)
                    
                    f = mass[j] / (dist_sq * dist)
                    
                    fx = fx + f * dx
                    fy = fy + f * dy
                    fz = fz + f * dz
                
                # Update velocity
                vel[i, 0] = vel[i, 0] + fx * dt
                vel[i, 1] = vel[i, 1] + fy * dt
                vel[i, 2] = vel[i, 2] + fz * dt
                
            # Update positions (this could be merged or separate)
            for i in range(n_bodies):
                pos[i, 0] = pos[i, 0] + vel[i, 0] * dt
                pos[i, 1] = pos[i, 1] + vel[i, 1] * dt
                pos[i, 2] = pos[i, 2] + vel[i, 2] * dt
                
    end_time = time.time()
    return end_time - start_time
