"""
Example: Three spheres in a line

Demonstrates capacitance calculation for three conducting spheres
arranged in a line with different radii.
"""

import numpy as np
from capmatrix import compute_capacitance_matrix, Sphere


def main():
    # Three spheres with different radii in a line
    r1, r2, r3 = 2e-9, 1.5e-9, 1e-9  # radii in meters
    spacing = 6e-9  # separation between centers
    
    print("Three spheres capacitance calculation")
    print("=" * 42)
    print(f"Sphere 1: radius = {r1*1e9:.1f} nm at (-{spacing*1e9:.0f}, 0, 0)")
    print(f"Sphere 2: radius = {r2*1e9:.1f} nm at (0, 0, 0)")
    print(f"Sphere 3: radius = {r3*1e9:.1f} nm at ({spacing*1e9:.0f}, 0, 0)")
    print()

    # Create spheres
    spheres = [
        Sphere(center=[-spacing, 0, 0], radius=r1),
        Sphere(center=[0, 0, 0], radius=r2),
        Sphere(center=[spacing, 0, 0], radius=r3)
    ]
    
    # Check for overlaps
    print("Checking for sphere overlaps...")
    for i, sphere_i in enumerate(spheres):
        for j, sphere_j in enumerate(spheres):
            if i < j:
                center_dist = np.linalg.norm(sphere_i.center - sphere_j.center)
                surface_dist = center_dist - sphere_i.radius - sphere_j.radius
                print(f"Surface distance {i+1}-{j+1}: {surface_dist*1e9:.2f} nm")
    print()

    # Compute capacitance matrix
    print("Computing capacitance matrix...")
    C = compute_capacitance_matrix(spheres, tolerance=1e-10, max_iterations=100)

    print("\nCapacitance matrix (F):")
    for i in range(len(spheres)):
        row_str = " ".join(f"{C[i,j]:.4e}" for j in range(len(spheres)))
        print(f"[{row_str}]")
    print()

    # Check matrix properties
    print("Matrix properties:")
    print(f"Symmetry check (max off-diagonal difference): {np.max(np.abs(C - C.T)):.2e}")
    
    # Row sums (should be close to zero for well-separated spheres)
    row_sums = np.sum(C, axis=1)
    print("Row sums (should be small for weakly coupled spheres):")
    for i, row_sum in enumerate(row_sums):
        print(f"  Row {i+1}: {row_sum:.4e}")
    
    # Compare diagonal elements to isolated spheres
    eps0 = 8.854187817e-12
    print("\nCompare to isolated sphere capacitances:")
    for i, sphere in enumerate(spheres):
        C_isolated = 4 * np.pi * eps0 * sphere.radius
        interaction_effect = (C[i,i]/C_isolated - 1) * 100
        print(f"  Sphere {i+1}: {interaction_effect:+.2f}% change from isolation")


if __name__ == "__main__":
    main()
