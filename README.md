# Arbitrary Capacitance Matrix

**Compute the capacitance matrix of _N_ conducting spheres in an arbitrary spatial distribution using the method of mirror images.**

This project is based on the numerical implementation I developed during my [BSc thesis](https://diposit.ub.edu/dspace/bitstream/2445/141682/1/P%C3%89REZ%20ESPINAR%20Carlos.pdf). It allows for the computation of the mutual capacitance matrix of multiple spherical conductors in a bounded region using a physically grounded and mathematically robust approach.

## 🚀 Installation

Install the package using pip:

```bash
pip install arbitrary-capacitance-matrix
```

Or for development:

```bash
git clone https://github.com/carlosperezespinar/arbitrary-capacitance-matrix.git
cd arbitrary-capacitance-matrix
pip install -e .
```

## 📖 Quick Start

```python
import numpy as np
from capmatrix import compute_capacitance_matrix, Sphere

# Define two spheres
spheres = [
    Sphere(center=[0, 0, 0], radius=1e-9),      # 1 nm radius at origin
    Sphere(center=[3e-9, 0, 0], radius=1e-9)    # 1 nm radius, 3 nm away
]

# Compute capacitance matrix
C = compute_capacitance_matrix(spheres)
print("Capacitance matrix (F):")
print(C)
```

## 🔬 Background & Theory

The **method of mirror images** is a classic electrostatics technique to enforce boundary conditions by introducing fictitious "image charges." For a system of _N_ conducting spheres, we recursively place image charges inside each sphere to satisfy the equipotential condition, then assemble the resulting potentials into the **capacitance matrix** **C**:

C_ij = 4 * π * ε₀ * R_i * Q_ij

where Q_ij is the total induced charge on sphere i when sphere j is held at unit potential and all others are grounded.

This approach handles:
- Arbitrary number (_N_) of spheres  
- Random positions & radii  
- No assumed symmetries or simplifying approximations  

## 🖼 Images & Diagrams

### 1. Basic image-charge construction  
![Mirror‐image construction for two spheres](screenshots/schema-amilcar-1.png)  
*Iterative placement of image charges inside each sphere to enforce constant potential.*

### 2. Generalized vector formulation  
![Vector form of image‐charge positions](screenshots/schema-amilcar-2.png)  
*Vector-based formula for computing the coordinates and strength of each new image charge from known charge positions.*

## 🔍 Examples

### Two Spheres
```python
from capmatrix import compute_capacitance_matrix, Sphere

# Two identical spheres
radius = 1e-9  # 1 nm
separation = 3e-9  # 3 nm center-to-center

spheres = [
    Sphere([0, 0, 0], radius),
    Sphere([separation, 0, 0], radius)
]

C = compute_capacitance_matrix(spheres)
```

### Three Spheres in a Line
```python
# Three spheres with different radii
spheres = [
    Sphere([-6e-9, 0, 0], 2e-9),   # Left sphere
    Sphere([0, 0, 0], 1.5e-9),     # Center sphere  
    Sphere([6e-9, 0, 0], 1e-9)     # Right sphere
]

C = compute_capacitance_matrix(spheres, tolerance=1e-10, max_iterations=100)
```

See the `examples/` folder for complete working examples:
- `examples/two_spheres.py` - Two sphere benchmark with analytical comparison
- `examples/three_spheres.py` - Three sphere configuration
- `demo.py` - Simple demonstration script

## 📋 API Reference

### Classes

#### `Sphere(center, radius)`
Represents a conducting sphere.
- `center`: 3D coordinates [x, y, z] 
- `radius`: Sphere radius (must be positive)

#### `Charge(value, radial_distance, coordinates, sphere_index, iteration=0)`
Represents a point charge in the system.

### Functions

#### `compute_capacitance_matrix(spheres, tolerance=1e-8, max_iterations=50)`
Compute the capacitance matrix for a list of spheres.

**Parameters:**
- `spheres`: List of Sphere objects
- `tolerance`: Convergence tolerance (default: 1e-8)
- `max_iterations`: Maximum iterations (default: 50)

**Returns:** NxN numpy array of capacitances in Farads

## 🧪 Testing

Run the test suite:
```bash
pytest tests/
```

## 📚 References

1. Wasshuber, C. (1997). *About Single-Electron Devices and Circuits*. PhD Thesis, Technische Universität Wien. [Online PDF – Chapter on method of images](https://www.iue.tuwien.ac.at/phd/wasshuber/node77.html)  
2. Pérez Espinar, C. [BSc Thesis (2019), Universitat de Barcelona](https://diposit.ub.edu/dspace/bitstream/2445/141682/1/P%C3%89REZ%20ESPINAR%20Carlos.pdf)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
