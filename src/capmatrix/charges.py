"""
Charge class for representing point charges in the method of mirror images.
"""

import numpy as np


class Charge:
    """
    Represents a point charge in 3D space.
    
    Parameters
    ----------
    value : float
        Charge magnitude (can be positive or negative)
    radial_distance : float
        Distance from the center of the sphere that owns this charge
    coordinates : array_like
        3D coordinates [x, y, z] of the charge
    sphere_index : int
        Index of the sphere that owns this charge
    iteration : int, optional
        Iteration number when this charge was created (default: 0)
        
    Attributes
    ----------
    value : float
        Charge magnitude
    radial_distance : float
        Distance from sphere center
    coordinates : numpy.ndarray
        3D position as numpy array
    sphere_index : int
        Owner sphere index
    iteration : int
        Creation iteration
    """
    
    def __init__(self, value, radial_distance, coordinates, sphere_index, iteration=0):
        self.value = float(value)
        self.radial_distance = float(radial_distance)
        self.coordinates = np.array(coordinates, dtype=float)
        self.sphere_index = int(sphere_index)
        self.iteration = int(iteration)
        
        if len(self.coordinates) != 3:
            raise ValueError("Coordinates must have 3 elements [x, y, z]")
        if self.radial_distance < 0:
            raise ValueError("Radial distance must be non-negative")
            
    def __repr__(self):
        return (f"Charge(value={self.value:.6f}, "
                f"radial_distance={self.radial_distance:.6f}, "
                f"coordinates={self.coordinates}, "
                f"sphere_index={self.sphere_index}, "
                f"iteration={self.iteration})")
