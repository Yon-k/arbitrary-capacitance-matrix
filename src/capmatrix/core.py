import numpy as np
#from .utils import generate_image_charges, check_convergence
from src.capmatrix.utils import generate_image_charges, check_convergence

def compute_capacitance_matrix(spheres, tol=1e-8, max_iter=50):
    """
    Compute the NxN capacitance matrix for given spheres.
    :param spheres: list of Sphere
    :param tol: convergence tolerance on induced charges
    :param max_iter: maximum image-charge iterations
    :return: NxN numpy array of capacitances
    """
    N = len(spheres)
    # Q_matrix[i,j] = net induced charge on sphere i when sphere j is held at 1 V and others at 0
    Q_matrix = np.zeros((N, N))

    for j, sphere_j in enumerate(spheres):
        # Generate all image charges for unit potential on sphere j
        charges = generate_image_charges(spheres, source_index=j, tol=tol, max_iter=max_iter)
        # Sum each sphere's total induced charge
        for charge in charges:
            Q_matrix[charge.owner, j] += charge.q

    # Assemble C: C_ij = 4·π·ε0·R_i·Q_matrix[i,j]
    eps0 = 8.854187817e-12
    C = np.zeros_like(Q_matrix)
    for i, sphere in enumerate(spheres):
        C[i, :] = 4 * np.pi * eps0 * sphere.radius * Q_matrix[i, :]
    return C


class Sphere:
    def __init__(self, center, radius):
        self.center = np.array(center, dtype=float)
        self.radius = float(radius)