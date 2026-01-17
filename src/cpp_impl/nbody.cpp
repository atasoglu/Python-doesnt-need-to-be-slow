#include <iostream>
#include <vector>
#include <cmath>
#include <chrono>
#include <random>
#include <string>
#include <cstring>

struct Planet {
    double x, y, z;
    double vx, vy, vz;
    double mass;
};

void run_simulation(int n, int steps) {
    std::mt19937 gen(42);
    std::uniform_real_distribution<> dist_pos(-100.0, 100.0);
    std::uniform_real_distribution<> dist_vel(-1.0, 1.0);
    std::uniform_real_distribution<> dist_mass(1.0, 10.0);
    
    std::vector<Planet> planets(n);
    for(int i=0; i<n; ++i) {
        planets[i].x = dist_pos(gen);
        planets[i].y = dist_pos(gen);
        planets[i].z = dist_pos(gen);
        planets[i].vx = dist_vel(gen);
        planets[i].vy = dist_vel(gen);
        planets[i].vz = dist_vel(gen);
        planets[i].mass = dist_mass(gen);
    }
    
    double dt = 0.01;
    double soft_epsilon = 1e-9;
    
    auto start = std::chrono::high_resolution_clock::now();
    
    for(int s=0; s<steps; ++s) {
        // Force calculation
        for(int i=0; i<n; ++i) {
            double fx = 0.0, fy = 0.0, fz = 0.0;
            double p1x = planets[i].x;
            double p1y = planets[i].y;
            double p1z = planets[i].z;
            
            for(int j=0; j<n; ++j) {
                if(i == j) continue;
                
                double dx = planets[j].x - p1x;
                double dy = planets[j].y - p1y;
                double dz = planets[j].z - p1z;
                
                double dist_sq = dx*dx + dy*dy + dz*dz + soft_epsilon;
                double dist = std::sqrt(dist_sq);
                double f = planets[j].mass / (dist_sq * dist);
                
                fx += f * dx;
                fy += f * dy;
                fz += f * dz;
            }
            
            planets[i].vx += fx * dt;
            planets[i].vy += fy * dt;
            planets[i].vz += fz * dt;
        }
        
        // Update positions
        for(int i=0; i<n; ++i) {
            planets[i].x += planets[i].vx * dt;
            planets[i].y += planets[i].vy * dt;
            planets[i].z += planets[i].vz * dt;
        }
    }
    
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> duration = end - start;
    
    std::cout << "Time: " << duration.count() << " seconds" << std::endl;
    std::cout << "RESULT: " << duration.count() << std::endl;
}

int main(int argc, char* argv[]) {
    int n = 100;
    int steps = 100;
    
    for(int i=1; i<argc; i++) {
        if(std::string(argv[i]) == "--n" && i+1 < argc) n = std::stoi(argv[i+1]);
        if(std::string(argv[i]) == "--steps" && i+1 < argc) steps = std::stoi(argv[i+1]);
    }
    
    std::cout << "Running C++ N-body with N=" << n << ", Steps=" << steps << std::endl;
    run_simulation(n, steps);
    
    return 0;
}
