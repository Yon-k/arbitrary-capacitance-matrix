"""
Example: Three spheres in a line

Demonstrates capacitance calculation for three conducting spheres
arranged in a line with different radii.
"""

import numpy as np
from capmatrix import compute_capacitance_matrix, Sphere
from tqdm import tqdm

def main():
    r1, r2, r3 = 2e-9, 1.5e-9, 1e-9
    spacing = 6e-9

    print("\033[96m\033[1mThree spheres capacitance calculation\033[0m")
    print("\033[96m" + "=" * 42 + "\033[0m")
    print(f"\033[93mSphere 1: radius = {r1*1e9:.1f} nm at (-{spacing*1e9:.0f}, 0, 0)\033[0m")
    print(f"\033[93mSphere 2: radius = {r2*1e9:.1f} nm at (0, 0, 0)\033[0m")
    print(f"\033[93mSphere 3: radius = {r3*1e9:.1f} nm at ({spacing*1e9:.0f}, 0, 0)\033[0m")
    print()

    spheres = [
        Sphere(center=[-spacing, 0, 0], radius=r1),
        Sphere(center=[0, 0, 0], radius=r2),
        Sphere(center=[spacing, 0, 0], radius=r3)
    ]

    print("\033[92mChecking for sphere overlaps...\033[0m")
    n = len(spheres)
    for i in tqdm(range(n), desc="Overlap check"):
        for j in range(i+1, n):
            center_dist = np.linalg.norm(np.array(spheres[i].center) - np.array(spheres[j].center))
            surface_dist = center_dist - spheres[i].radius - spheres[j].radius
            print(f"Surface distance {i+1}-{j+1}: {surface_dist*1e9:.2f} nm")
    print()

    print("\033[92mComputing capacitance matrix...\033[0m")
    C = compute_capacitance_matrix(spheres, tolerance=1e-10, max_iterations=100)

    print("\n\033[95mCapacitance matrix (F):\033[0m")
    for i in range(len(spheres)):
        row_str = " ".join(f"{C[i,j]:.4e}" for j in range(len(spheres)))
        print(f"[{row_str}]")
    print()

    print("\033[94mMatrix properties:\033[0m")
    print(f"Symmetry check (max off-diagonal difference): {np.max(np.abs(C - C.T)):.2e}")

    row_sums = np.sum(C, axis=1)
    print("\033[96mRow sums (should be small for weakly coupled spheres):\033[0m")
    for i, row_sum in enumerate(row_sums):
        print(f"  Row {i+1}: {row_sum:.4e}")

    eps0 = 8.854187817e-12
    print("\n\033[96mCompare to isolated sphere capacitances:\033[0m")
    for i, sphere in enumerate(spheres):
        C_isolated = 4 * np.pi * eps0 * sphere.radius
        interaction_effect = (C[i,i]/C_isolated - 1) * 100
        print(f"  Sphere {i+1}: {interaction_effect:+.2f}% change from isolation")

if __name__ == "__main__":
    main()
