package main

import (
	"flag"
	"fmt"
	"math"
	"math/rand"
	"time"
)

type Planet struct {
	x, y, z    float64
	vx, vy, vz float64
	mass       float64
}

func computeForces(planets []Planet, dt float64) {
	const softEpsilon = 1e-9
	n := len(planets)
	forces := make([][3]float64, n)

	for i := 0; i < n; i++ {
		p1x, p1y, p1z := planets[i].x, planets[i].y, planets[i].z

		for j := 0; j < n; j++ {
			if i == j {
				continue
			}

			dx := planets[j].x - p1x
			dy := planets[j].y - p1y
			dz := planets[j].z - p1z

			distSq := dx*dx + dy*dy + dz*dz + softEpsilon
			dist := math.Sqrt(distSq)
			f := planets[j].mass / (distSq * dist)

			forces[i][0] += f * dx
			forces[i][1] += f * dy
			forces[i][2] += f * dz
		}
	}

	// Update velocities
	for i := 0; i < n; i++ {
		planets[i].vx += forces[i][0] * dt
		planets[i].vy += forces[i][1] * dt
		planets[i].vz += forces[i][2] * dt
	}
}

func updatePositions(planets []Planet, dt float64) {
	for i := range planets {
		planets[i].x += planets[i].vx * dt
		planets[i].y += planets[i].vy * dt
		planets[i].z += planets[i].vz * dt
	}
}

func main() {
	var n, steps int
	flag.IntVar(&n, "n", 100, "Number of bodies")
	flag.IntVar(&steps, "steps", 100, "Number of simulation steps")
	flag.Parse()

	fmt.Printf("Running Go N-body with N=%d, Steps=%d\n", n, steps)

	// Initialize random seed for deterministic results
	rand.Seed(42)

	// Initialize planets
	planets := make([]Planet, n)
	for i := 0; i < n; i++ {
		planets[i] = Planet{
			x:    rand.Float64()*200.0 - 100.0,
			y:    rand.Float64()*200.0 - 100.0,
			z:    rand.Float64()*200.0 - 100.0,
			vx:   rand.Float64()*2.0 - 1.0,
			vy:   rand.Float64()*2.0 - 1.0,
			vz:   rand.Float64()*2.0 - 1.0,
			mass: rand.Float64()*9.0 + 1.0,
		}
	}

	start := time.Now()
	dt := 0.01

	for s := 0; s < steps; s++ {
		computeForces(planets, dt)
		updatePositions(planets, dt)
	}

	duration := time.Since(start)
	seconds := duration.Seconds()

	fmt.Printf("Time: %.4f seconds\n", seconds)
	fmt.Printf("RESULT: %.4f\n", seconds)
}