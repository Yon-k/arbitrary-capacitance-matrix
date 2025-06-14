"""
Arbitrary Capacitance Matrix

Compute the capacitance matrix of N conducting spheres in an arbitrary 
spatial distribution using the method of mirror images.
"""

from .core import compute_capacitance_matrix, Sphere
from .charges import Charge
from .utils import generate_image_charges, check_convergence

__version__ = "0.1.0"
__author__ = "Carlos Pérez Espinar"

__all__ = [
    "compute_capacitance_matrix",
    "Sphere", 
    "Charge",
    "generate_image_charges",
    "check_convergence",
]