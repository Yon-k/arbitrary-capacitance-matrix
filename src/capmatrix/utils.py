import numpy as np
from collections import deque

class Charge:
    def __init__(self, q, owner, position):
        self.q = q              # charge magnitude
        self.owner = owner      # sphere index
        self.position = position  # 3D coordinates


def generate_image_charges(spheres, source_index, tol, max_iter):
    """
    Iteratively generate image charges until convergence.
    Returns list of Charge instances (including the real source).
    """
    N = len(spheres)
    # Initialize queue with the real source charge at sphere center
    real = Charge(q=1.0, owner=source_index, position=spheres[source_index].center)
    all_charges = [real]
    queue = deque([real])

    # Track induced charge per sphere after each iteration\m    prev_total = np.zeros(N)

    for it in range(max_iter):
        next_level = []
        # Process each charge from previous iteration
        while queue:
            c = queue.popleft()
            # Create image on every other sphere
            for i, sph in enumerate(spheres):
                if i == c.owner:
                    continue
                d_vec = c.position - sph.center
                d = np.linalg.norm(d_vec)
                # image parameters per Wasshuber: q' = -a/d * q, pos' = centre + (a^2/d^2)*(pos - centre)
                q_img = - sph.radius / d * c.q
                pos_img = sph.center + (sph.radius**2 / d**2) * (c.position - sph.center)
                img = Charge(q=q_img, owner=i, position=pos_img)
                next_level.append(img)
                all_charges.append(img)
        # Sum induced on each sphere
        totals = np.zeros(N)
        for ch in all_charges:
            totals[ch.owner] += ch.q
        # Convergence check
        if check_convergence(prev_total, totals, tol):
            break
        prev_total = totals.copy()
        queue.extend(next_level)
    return all_charges


def check_convergence(prev, current, tol):
    return np.allclose(prev, current, atol=tol, rtol=0)