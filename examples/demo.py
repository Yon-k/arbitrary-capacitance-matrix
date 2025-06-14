"""
Simple demonstration script for the arbitrary-capacitance-matrix package.

This script shows basic usage of the package for computing capacitance matrices
of conducting spheres using the method of mirror images.
"""

# Note: This script assumes the package is installed. 
# To install in development mode, run: pip install -e .

try:
    import numpy as np
    from capmatrix import compute_capacitance_matrix, Sphere
    
    def demo_two_spheres():
        """Demonstrate capacitance calculation for two spheres."""
        print("Two Spheres Demo")
        print("================")
        
        # Two equal spheres
        radius = 1e-9  # 1 nm
        separation = 3e-9  # 3 nm center-to-center
        
        spheres = [
            Sphere(center=[0, 0, 0], radius=radius),
            Sphere(center=[separation, 0, 0], radius=radius)
        ]
        
        print(f"Sphere 1: center=(0,0,0), radius={radius*1e9:.1f} nm")
        print(f"Sphere 2: center=({separation*1e9:.1f},0,0), radius={radius*1e9:.1f} nm")
        print(f"Surface separation: {(separation - 2*radius)*1e9:.1f} nm")
        
        # Compute capacitance matrix
        C = compute_capacitance_matrix(spheres)
        
        print("\nCapacitance matrix (F):")
        print(f"  C11 = {C[0,0]:.6e}")
        print(f"  C12 = {C[0,1]:.6e}")
        print(f"  C21 = {C[1,0]:.6e}")
        print(f"  C22 = {C[1,1]:.6e}")
        
        # Check symmetry
        symmetry_error = abs(C[0,1] - C[1,0])
        print(f"\nSymmetry check: |C12 - C21| = {symmetry_error:.2e}")
        
        return C
    
    def demo_isolated_sphere():
        """Demonstrate isolated sphere capacitance."""
        print("\nIsolated Sphere Demo")
        print("===================")
        
        radius = 2e-9  # 2 nm
        sphere = Sphere(center=[0, 0, 0], radius=radius)
        
        C = compute_capacitance_matrix([sphere])
        
        # Compare with analytical result
        eps0 = 8.854187817e-12  # F/m
        analytical = 4 * np.pi * eps0 * radius
        
        print(f"Sphere radius: {radius*1e9:.1f} nm")
        print(f"Computed capacitance: {C[0,0]:.6e} F")
        print(f"Analytical (4πε₀R): {analytical:.6e} F")
        print(f"Relative error: {abs(C[0,0] - analytical)/analytical*100:.4f}%")
        
        return C
    
    if __name__ == "__main__":
        print("Arbitrary Capacitance Matrix - Demo Script")
        print("==========================================\n")
        
        # Run demonstrations
        demo_isolated_sphere()
        demo_two_spheres()
        
        print("\nDemo completed successfully!")
        print("\nFor more examples, see the 'examples/' directory.")

except ImportError as e:
    print("Error: Package not installed or dependencies missing.")
    print(f"Details: {e}")
    print("\nTo install the package, run:")
    print("  pip install -e .")
    print("\nTo install dependencies:")
    print("  pip install numpy")
except Exception as e:
    print(f"Error running demo: {e}")
    print("Please check your installation and try again.")
