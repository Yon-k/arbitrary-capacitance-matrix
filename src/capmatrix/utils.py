"""
Utility functions for the method of mirror images implementation.
"""

import numpy as np
from collections import deque
from .charges import Charge


def generate_image_charges(spheres, source_index, tolerance, max_iterations):
    """
    Iteratively generate image charges until convergence.
    
    Parameters
    ----------
    spheres : list of Sphere
        List of all spheres in the system
    source_index : int
        Index of the sphere held at unit potential
    tolerance : float
        Convergence tolerance for induced charges
    max_iterations : int
        Maximum number of iterations
        
    Returns
    -------
    list of Charge
        List of all charges (including the initial source charge)
    """
    N = len(spheres)
    
    # Initialize with source charge at sphere center
    source_sphere = spheres[source_index]
    source_charge = Charge(
        value=1.0,
        radial_distance=0.0,
        coordinates=source_sphere.center.copy(),
        sphere_index=source_index,
        iteration=0
    )
    
    all_charges = [source_charge]
    source_sphere.add_charge(source_charge.value)
    
    # Queue for processing charges level by level
    charge_queue = deque([source_charge])
    
    # Track total charge per sphere for convergence checking
    previous_totals = np.zeros(N)
    
    for iteration in range(max_iterations):
        next_level_charges = []
        
        # Process all charges from current iteration
        while charge_queue:
            current_charge = charge_queue.popleft()
            
            # Find the sphere that owns this charge
            owner_sphere = spheres[current_charge.sphere_index]
            
            # Create image charges in all other spheres
            image_charges = owner_sphere.create_image_charges(current_charge, spheres)
            next_level_charges.extend(image_charges)
            all_charges.extend(image_charges)
        
        # Calculate current totals for convergence check
        current_totals = np.zeros(N)
        for charge in all_charges:
            current_totals[charge.sphere_index] += charge.value
            
        # Check convergence
        if check_convergence(previous_totals, current_totals, tolerance):
            break
            
        previous_totals = current_totals.copy()
        charge_queue.extend(next_level_charges)
    
    return all_charges


def check_convergence(previous, current, tolerance):
    """
    Check if the induced charges have converged between iterations.
    
    Parameters
    ----------
    previous : numpy.ndarray
        Previous iteration's total charges per sphere
    current : numpy.ndarray  
        Current iteration's total charges per sphere
    tolerance : float
        Absolute tolerance for convergence
        
    Returns
    -------
    bool
        True if converged, False otherwise
    """
    return np.allclose(previous, current, atol=tolerance, rtol=0)


def calculate_final_capacitances(spheres, source_radius):
    """
    Calculate final capacitance coefficients for a source sphere.
    
    Parameters
    ----------
    spheres : list of Sphere
        List of all spheres with accumulated charges
    source_radius : float
        Radius of the source sphere
        
    Returns
    -------
    list of float
        Capacitance coefficients
    """
    eps_0 = 8.854187817e-12  # F/m
    coefficients = []
    
    for sphere in spheres:
        coeff = 4 * np.pi * eps_0 * source_radius * sphere.get_final_coefficient()
        coefficients.append(coeff)
        
    return coefficients


def surface_distance(sphere1, sphere2):
    """
    Calculate the surface-to-surface distance between two spheres.
    
    Parameters
    ----------
    sphere1, sphere2 : Sphere
        The two spheres
        
    Returns
    -------
    float
        Surface-to-surface distance
    """
    center_distance = np.linalg.norm(sphere1.center - sphere2.center)
    return center_distance - sphere1.radius - sphere2.radius