use std::env;
use std::time::Instant;
use rand::SeedableRng;
use rand::Rng;
use rand::rngs::StdRng;

#[derive(Clone, Copy)]
struct Planet {
    x: f64, y: f64, z: f64,
    vx: f64, vy: f64, vz: f64,
    mass: f64,
}

fn run_simulation_rust(n_bodies: usize, n_steps: usize, dt: f64) {
    // Deterministic RNG
    let mut rng = StdRng::seed_from_u64(42);
    
    // Structure of Arrays (SoA) for better SIMD/Cache matches usage
    let mut x: Vec<f64> = (0..n_bodies).map(|_| rng.gen_range(-100.0..100.0)).collect();
    let mut y: Vec<f64> = (0..n_bodies).map(|_| rng.gen_range(-100.0..100.0)).collect();
    let mut z: Vec<f64> = (0..n_bodies).map(|_| rng.gen_range(-100.0..100.0)).collect();
    let mut vx: Vec<f64> = (0..n_bodies).map(|_| rng.gen_range(-1.0..1.0)).collect();
    let mut vy: Vec<f64> = (0..n_bodies).map(|_| rng.gen_range(-1.0..1.0)).collect();
    let mut vz: Vec<f64> = (0..n_bodies).map(|_| rng.gen_range(-1.0..1.0)).collect();
    let mass: Vec<f64> = (0..n_bodies).map(|_| rng.gen_range(1.0..10.0)).collect();

    let start_time = Instant::now();
    let soft_epsilon = 1e-9;

    for _ in 0..n_steps {
        // PERF: Single-threaded implementation to be fair against C/C++
        // We compute all forces first, then update velocities/positions
        
        let mut forces: Vec<(f64, f64, f64)> = Vec::with_capacity(n_bodies);

        for i in 0..n_bodies {
            let mut fx = 0.0;
            let mut fy = 0.0;
            let mut fz = 0.0;
            let p1x = x[i];
            let p1y = y[i];
            let p1z = z[i];
            
            for j in 0..n_bodies {
                if i == j { continue; }
                
                let dx = x[j] - p1x;
                let dy = y[j] - p1y;
                let dz = z[j] - p1z;
                
                let dist_sq = dx*dx + dy*dy + dz*dz + soft_epsilon;
                let dist = dist_sq.sqrt();
                let f = mass[j] / (dist_sq * dist);
                
                fx += f * dx;
                fy += f * dy;
                fz += f * dz;
            }
            forces.push((fx, fy, fz));
        }
        
        // Update velocity and position
        for i in 0..n_bodies {
            let (fx, fy, fz) = forces[i];
            vx[i] += fx * dt;
            vy[i] += fy * dt;
            vz[i] += fz * dt;
            
            x[i] += vx[i] * dt;
            y[i] += vy[i] * dt;
            z[i] += vz[i] * dt;
        }
    }

    let duration = start_time.elapsed();
    let secs = duration.as_secs_f64();
    println!("Time: {:.4} seconds", secs);
    println!("RESULT: {:.4}", secs);
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let mut n = 100;
    let mut steps = 100;

    let mut i = 1;
    while i < args.len() {
        if args[i] == "--n" && i + 1 < args.len() {
            n = args[i+1].parse().unwrap_or(100);
            i += 1;
        } else if args[i] == "--steps" && i + 1 < args.len() {
            steps = args[i+1].parse().unwrap_or(100);
            i += 1;
        }
        i += 1;
    }

    println!("Running Native Rust N-body with N={}, Steps={}", n, steps);
    run_simulation_rust(n, steps, 0.01);
}
