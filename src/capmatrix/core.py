"""
Core classes and functions for computing capacitance matrices.
"""

import numpy as np
from .charges import Charge
from .utils import generate_image_charges


# Physical constants
EPSILON_0 = 8.854187817e-12  # F/m (vacuum permittivity)


class Sphere:
    """
    A conducting sphere in 3D space.
    
    Parameters
    ----------
    center : array_like
        3D coordinates of the sphere center [x, y, z]
    radius : float
        Radius of the sphere (must be positive)
        
    Attributes
    ----------
    center : numpy.ndarray
        3D center coordinates as numpy array
    radius : float
        Sphere radius
    accumulated_charge : float
        Total accumulated charge from all image charges
    charge_coefficients : list
        History of charge coefficients for convergence tracking
    """
    
    def __init__(self, center, radius):
        self.center = np.array(center, dtype=float)
        self.radius = float(radius)
        self.accumulated_charge = 0.0
        self.charge_coefficients = []
        
        if self.radius <= 0:
            raise ValueError("Sphere radius must be positive")
        if len(self.center) != 3:
            raise ValueError("Sphere center must have 3 coordinates [x, y, z]")
            
    def add_charge(self, charge_value):
        """Add a charge value to the accumulated charge."""
        self.accumulated_charge += charge_value
        
    def get_charge_coefficient(self):
        """Get the current accumulated charge coefficient."""
        return self.accumulated_charge
        
    def save_coefficient(self):
        """Save the current charge coefficient for convergence tracking."""
        self.charge_coefficients.append(self.accumulated_charge)
        
    def get_final_coefficient(self):
        """Get the most recent charge coefficient."""
        return self.charge_coefficients[-1] if self.charge_coefficients else 0.0
        
    def reset(self):
        """Reset accumulated charge and coefficients."""
        self.accumulated_charge = 0.0
        self.charge_coefficients = []
        
    def create_image_charges(self, source_charge, target_spheres):
        """
        Create image charges in all target spheres for a given source charge.
        
        Parameters
        ----------
        source_charge : Charge
            The source charge creating images
        target_spheres : list of Sphere
            Spheres where image charges will be created
            
        Returns
        -------
        list of Charge
            List of newly created image charges
        """
        image_charges = []
        
        for i, target_sphere in enumerate(target_spheres):
            if target_sphere is self:
                continue
                
            # Calculate distance between source charge and target sphere center
            distance = np.linalg.norm(source_charge.coordinates - target_sphere.center)
            
            # Image charge value: Q' = -(q₀ × R) / (d - r₀)
            image_value = -(source_charge.value * target_sphere.radius) / (distance - source_charge.radial_distance)
            
            # Image charge radial distance: r' = R² / (d - r₀)
            image_radial_distance = (target_sphere.radius**2) / (distance - source_charge.radial_distance)
            
            # Image charge position: center + (R/d)² × (source_pos - center)
            image_coordinates = (target_sphere.center - 
                               (target_sphere.radius/distance)**2 * 
                               (target_sphere.center - source_charge.coordinates))
            
            # Create image charge
            image_charge = Charge(
                value=image_value,
                radial_distance=image_radial_distance,
                coordinates=image_coordinates,
                sphere_index=i,
                iteration=source_charge.iteration + 1
            )
            
            # Add to target sphere's accumulated charge
            target_sphere.add_charge(image_charge.value)
            image_charges.append(image_charge)
            
        return image_charges
        
    def __repr__(self):
        return f"Sphere(center={self.center}, radius={self.radius})"


def compute_capacitance_matrix(spheres, tolerance=1e-8, max_iterations=50):
    """
    Compute the NxN capacitance matrix for N conducting spheres.
    
    Uses the method of mirror images to iteratively place image charges
    until convergence, then assembles the resulting capacitance matrix.
    
    Parameters
    ----------
    spheres : list of Sphere
        List of conducting spheres in the system
    tolerance : float, optional
        Convergence tolerance for induced charges (default: 1e-8)
    max_iterations : int, optional
        Maximum number of image-charge iterations (default: 50)
        
    Returns
    -------
    numpy.ndarray
        NxN capacitance matrix where C[i,j] is the capacitance between
        spheres i and j in Farads
        
    Notes
    -----
    The capacitance matrix is computed using:
    C_ij = 4·π·ε₀·R_i·Q_ij
    
    where Q_ij is the total induced charge on sphere i when sphere j 
    is held at unit potential and all others are grounded.
    """
    N = len(spheres)
    if N == 0:
        return np.array([])
        
    # Q_matrix[i,j] = net induced charge on sphere i when sphere j is held at 1V and others at 0V
    Q_matrix = np.zeros((N, N))

    for j, source_sphere in enumerate(spheres):
        # Generate all image charges for unit potential on sphere j
        total_charges = generate_image_charges(
            spheres, 
            source_index=j, 
            tolerance=tolerance, 
            max_iterations=max_iterations
        )
        
        # Sum each sphere's total induced charge
        for charge in total_charges:
            Q_matrix[charge.sphere_index, j] += charge.value
        
        # Reset spheres for next iteration
        for sphere in spheres:
            sphere.reset()

    # Assemble capacitance matrix: C_ij = 4·π·ε₀·R_i·Q_matrix[i,j]
    C = np.zeros_like(Q_matrix)
    for i, sphere in enumerate(spheres):
        C[i, :] = 4 * np.pi * EPSILON_0 * sphere.radius * Q_matrix[i, :]
        
    return C
