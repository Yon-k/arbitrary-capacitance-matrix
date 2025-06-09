# Arbitrary Capacitance Matrix

**Compute the capacitance matrix of _N_ conducting spheres in an arbitrary spatial distribution using the method of mirror images.**

This project is based on the numerical implementation I developed during my [BSc thesis](https://diposit.ub.edu/dspace/bitstream/2445/141682/1/P%C3%89REZ%20ESPINAR%20Carlos.pdf). It allows for the computation of the mutual capacitance matrix of multiple spherical conductors in a bounded region using a physically grounded and mathematically robust approach.


> ⚠️ _Work in progress_: I’m currently restructuring this into a reusable Python package. If you're interested in using or contributing to this, feel free to reach out — I’d be happy to prioritize development!

## 🔬 Background & Theory

The **method of mirror images** is a classic electrostatics technique to enforce boundary conditions by introducing fictitious “image charges.” For a system of _N_ conducting spheres, we recursively place image charges inside each sphere to satisfy the equipotential condition, then assemble the resulting potentials into the **capacitance matrix** **C**:

C_ij = 4 * π * ε₀ * sum_over_images ( q_image^(j) / distance_to_sphere_i )

This approach handles:
- Arbitrary number (_N_) of spheres  
- Random positions & radii  
- No assumed symmetries or simplifying approximations  

## 🖼 Images & Diagrams

### 1. Basic image-charge construction  
![Mirror‐image construction for two spheres](/schema-amilcar-1.png)  
*Iterative placement of image charges inside each sphere to enforce constant potential.*

### 2. Generalized vector formulation  
![Vector form of image‐charge positions](/schema-amilcar-2.png)  
*Vector-based formula for computing the coordinates and strength of each new image charge \( q' \) from known charge positions.*

## 🔍 Examples

See the `examples/` folder for Jupyter notebooks demonstrating:

- Two-sphere benchmark  
- Random distributions of 5, 10, 20 spheres (TBA)
- Performance & scaling analysis (TBA)  


## 📚 References

1. Wasshuber, C. (1997). *About Single-Electron Devices and Circuits*. PhD Thesis, Technische Universität Wien. [Online PDF – Chapter on method of images](https://www.iue.tuwien.ac.at/phd/wasshuber/node77.html)  
2. Pérez Espinar, C. [BSc Thesis (2019), Universitat de Barcelona](https://diposit.ub.edu/dspace/bitstream/2445/141682/1/P%C3%89REZ%20ESPINAR%20Carlos.pdf)


