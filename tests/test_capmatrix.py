"""
Tests for the arbitrary-capacitance-matrix package.
"""

import numpy as np
import pytest
from capmatrix import compute_capacitance_matrix, Sphere, Charge
from capmatrix.utils import surface_distance, check_convergence


class TestCharge:
    """Tests for the Charge class."""
    
    def test_charge_creation(self):
        """Test basic charge creation."""
        charge = Charge(
            value=1.5,
            radial_distance=0.5,
            coordinates=[1, 2, 3],
            sphere_index=0
        )
        assert charge.value == 1.5
        assert charge.radial_distance == 0.5
        assert np.allclose(charge.coordinates, [1, 2, 3])
        assert charge.sphere_index == 0
        assert charge.iteration == 0
    
    def test_charge_validation(self):
        """Test charge parameter validation."""
        # Invalid coordinates length
        with pytest.raises(ValueError, match="Coordinates must have 3 elements"):
            Charge(1.0, 0.0, [1, 2], 0)
        
        # Negative radial distance
        with pytest.raises(ValueError, match="Radial distance must be non-negative"):
            Charge(1.0, -0.1, [0, 0, 0], 0)


class TestSphere:
    """Tests for the Sphere class."""
    
    def test_sphere_creation(self):
        """Test basic sphere creation."""
        sphere = Sphere(center=[1, 2, 3], radius=2.5)
        assert np.allclose(sphere.center, [1, 2, 3])
        assert sphere.radius == 2.5
        assert sphere.accumulated_charge == 0.0
        assert len(sphere.charge_coefficients) == 0
    
    def test_sphere_validation(self):
        """Test sphere parameter validation."""
        # Negative radius
        with pytest.raises(ValueError, match="Sphere radius must be positive"):
            Sphere([0, 0, 0], -1.0)
        
        # Wrong center dimensions
        with pytest.raises(ValueError, match="Sphere center must have 3 coordinates"):
            Sphere([0, 0], 1.0)
    
    def test_charge_operations(self):
        """Test sphere charge operations."""
        sphere = Sphere([0, 0, 0], 1.0)
        
        # Add charges
        sphere.add_charge(1.5)
        sphere.add_charge(-0.5)
        assert sphere.accumulated_charge == 1.0
        
        # Save coefficient
        sphere.save_coefficient()
        assert len(sphere.charge_coefficients) == 1
        assert sphere.get_final_coefficient() == 1.0
        
        # Reset
        sphere.reset()
        assert sphere.accumulated_charge == 0.0
        assert len(sphere.charge_coefficients) == 0


class TestCapacitanceMatrix:
    """Tests for capacitance matrix computation."""
    
    def test_isolated_sphere(self):
        """Test that an isolated sphere has the correct capacitance C = 4πε₀R."""
        R = 1e-9
        sphere = Sphere(center=[0, 0, 0], radius=R)
        C = compute_capacitance_matrix([sphere])
        
        eps0 = 8.854187817e-12
        expected = 4 * np.pi * eps0 * R
        assert np.isclose(C[0, 0], expected, rtol=1e-6)
    
    def test_two_spheres_far_apart(self):
        """Test that two well-separated spheres behave like isolated spheres."""
        R = 1e-9
        separation = 1e-6  # 1000x the radius
        spheres = [
            Sphere(center=[0, 0, 0], radius=R),
            Sphere(center=[separation, 0, 0], radius=R)
        ]
        C = compute_capacitance_matrix(spheres, max_iterations=10)
        
        eps0 = 8.854187817e-12
        C0 = 4 * np.pi * eps0 * R
        
        # Diagonal elements should be close to isolated sphere value
        assert np.isclose(C[0, 0], C0, rtol=1e-3)
        assert np.isclose(C[1, 1], C0, rtol=1e-3)
        
        # Off-diagonal elements should be very small
        assert abs(C[0, 1]) < C0 * 1e-3
        assert abs(C[1, 0]) < C0 * 1e-3
    
    def test_matrix_symmetry(self):
        """Test that the capacitance matrix is symmetric."""
        R1, R2 = 1e-9, 1.5e-9
        spheres = [
            Sphere(center=[0, 0, 0], radius=R1),
            Sphere(center=[5e-9, 0, 0], radius=R2)
        ]
        C = compute_capacitance_matrix(spheres)
        
        # Matrix should be symmetric
        assert np.allclose(C, C.T, rtol=1e-10)
    
    def test_empty_system(self):
        """Test handling of empty sphere list."""
        C = compute_capacitance_matrix([])
        assert C.shape == (0,)
    
    def test_single_sphere_matrix_properties(self):
        """Test matrix properties for single sphere."""
        sphere = Sphere([0, 0, 0], 2e-9)
        C = compute_capacitance_matrix([sphere])
        
        assert C.shape == (1, 1)
        assert C[0, 0] > 0  # Capacitance should be positive


class TestUtils:
    """Tests for utility functions."""
    
    def test_surface_distance(self):
        """Test surface distance calculation."""
        sphere1 = Sphere([0, 0, 0], 1.0)
        sphere2 = Sphere([5, 0, 0], 2.0)
        
        # Distance should be: center_distance - r1 - r2 = 5 - 1 - 2 = 2
        dist = surface_distance(sphere1, sphere2)
        assert np.isclose(dist, 2.0)
    
    def test_convergence_check(self):
        """Test convergence checking."""
        prev = np.array([1.0, 2.0, 3.0])
        current1 = np.array([1.0, 2.0, 3.0])  # Same values
        current2 = np.array([1.1, 2.1, 3.1])  # Different values
        
        assert check_convergence(prev, current1, 1e-10)
        assert not check_convergence(prev, current2, 1e-10)
        assert check_convergence(prev, current2, 0.2)


if __name__ == "__main__":
    # Run tests if script is executed directly
    pytest.main([__file__])
