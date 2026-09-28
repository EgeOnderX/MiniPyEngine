import math

class Ray:
    def __init__(self, origin, direction):
        self.origin = list(origin)
        # Normalize direction
        length = math.sqrt(sum(d ** 2 for d in direction))
        self.direction = [d / length for d in direction] if length > 0 else [0, 0, -1]

def ray_aabb_intersection(ray, aabb):
    """Slab method for Ray vs AABB intersection test."""
    t_min = float('-inf')
    t_max = float('inf')

    for i in range(3):
        if ray.direction[i] != 0.0:
            t1 = (aabb.min_bounds[i] - ray.origin[i]) / ray.direction[i]
            t2 = (aabb.max_bounds[i] - ray.origin[i]) / ray.direction[i]

            t_near = min(t1, t2)
            t_far = max(t1, t2)

            t_min = max(t_min, t_near)
            t_max = min(t_max, t_far)
        else:
            if ray.origin[i] < aabb.min_bounds[i] or ray.origin[i] > aabb.max_bounds[i]:
                return False, 0.0

    if t_max >= t_min and t_max > 0:
        return True, t_min
    return False, 0.0
