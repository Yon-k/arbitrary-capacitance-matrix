#from capmatrix.core import compute_capacitance_matrix, Sphere
from src.capmatrix.core import compute_capacitance_matrix, Sphere

# Two equal spheres, radius a, center separation d
a = 1e-9
b = 1e-9
d = 3e-9
spheres = [Sphere((0,0,0), a), Sphere((d,0,0), b)]
C = compute_capacitance_matrix(spheres)
print("Capacitance matrix (F):")
print(C)
# Compare to series expansion from Wasshuber (Table A.1)