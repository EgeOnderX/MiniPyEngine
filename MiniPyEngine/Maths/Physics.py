import math

class AABB:
    def __init__(self, min_bounds, max_bounds):
        self.min_bounds = list(min_bounds)
        self.max_bounds = list(max_bounds)

    def intersects(self, other):
        return (self.min_bounds[0] <= other.max_bounds[0] and self.max_bounds[0] >= other.min_bounds[0] and
                self.min_bounds[1] <= other.max_bounds[1] and self.max_bounds[1] >= other.min_bounds[1] and
                self.min_bounds[2] <= other.max_bounds[2] and self.max_bounds[2] >= other.min_bounds[2])

class Physics:
    GRAVITY = -18.0

    @staticmethod
    def apply_gravity(position_y, velocity_y, dt):
        velocity_y += Physics.GRAVITY * dt
        position_y += velocity_y * dt
        return position_y, velocity_y
