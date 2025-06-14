"""
Example: Two spheres capacitance calculation

This example demonstrates computing the capacitance matrix for two equal spheres
using the method of mirror images, and compares with analytical results.
"""

import numpy as np
from capmatrix import compute_capacitance_matrix, Sphere


def main():
    # Two equal spheres, radius a and b, center separation d
    a = 1e-9  # radius of first sphere (m)
    b = 1e-9  # radius of second sphere (m)  
    d = 3e-9  # center-to-center distance (m)

    print("Two spheres capacitance calculation")
    print("=" * 40)
    print(f"Sphere 1: radius = {a*1e9:.1f} nm at (0,0,0)")
    print(f"Sphere 2: radius = {b*1e9:.1f} nm at ({d*1e9:.1f},0,0)")
    print(f"Center separation: {d*1e9:.1f} nm")
    print(f"Surface separation: {(d-a-b)*1e9:.1f} nm")
    print()

    # Create spheres
    spheres = [
        Sphere(center=[0, 0, 0], radius=a), 
        Sphere(center=[d, 0, 0], radius=b)
    ]

    # Compute capacitance matrix
    print("Computing capacitance matrix...")
    C = compute_capacitance_matrix(spheres, tolerance=1e-20, max_iterations=100)

    print("\nCapacitance matrix (F):")
    print(f"C11 = {C[0,0]:.6e}")
    print(f"C12 = {C[0,1]:.6e}")
    print(f"C21 = {C[1,0]:.6e}")
    print(f"C22 = {C[1,1]:.6e}")
    print()

    # The matrix should be symmetric for identical spheres
    symmetry_error = abs(C[0,1] - C[1,0])
    print(f"Matrix symmetry check: |C12 - C21| = {symmetry_error:.2e}")

    # Compare to series expansion from Wasshuber (Table A.1)
    # For identical spheres: C11 ≈ 4πε₀a(1 + a/d + a²/d² + ...)
    eps0 = 8.854187817e-12
    theoretical_C11_approx = 4 * np.pi * eps0 * a * (1 + a/d + (a/d)**2)
    relative_error = abs(C[0,0] - theoretical_C11_approx)/theoretical_C11_approx*100
    
    print(f"\nComparison with analytical approximation:")
    print(f"Theoretical C11 (series approx): {theoretical_C11_approx:.6e}")
    print(f"Computed C11:                    {C[0,0]:.6e}")
    print(f"Relative error: {relative_error:.2f}%")

    # Isolated sphere comparison
    C_isolated = 4 * np.pi * eps0 * a
    print(f"\nIsolated sphere capacitance: {C_isolated:.6e}")
    print(f"Interaction effect: {(C[0,0]/C_isolated - 1)*100:.2f}% increase")


if __name__ == "__main__":
    main()