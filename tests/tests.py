import numpy as np
from capmatrix.core import compute_capacitance_matrix, Sphere

def test_isolated_sphere():
    R = 1e-9
    C = compute_capacitance_matrix([Sphere((0,0,0), R)])
    eps0 = 8.854187817e-12
    assert np.isclose(C[0,0], 4*np.pi*eps0*R)


def test_two_spheres_far():
    R = 1e-9
    spheres = [Sphere((0,0,0), R), Sphere((1e-6,0,0), R)]
    C = compute_capacitance_matrix(spheres, max_iter=10)
    eps0 = 8.854187817e-12
    C0 = 4*np.pi*eps0*R
    assert np.isclose(C[0,0], C0, rtol=1e-4)
    assert abs(C[0,1]) < 1e-15