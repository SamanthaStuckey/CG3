import math

from vectors import Vec3, subtract, normalize, cross, dot


class Camera:
    def __init__(self, position, target, fov, aspect):
        self.position = position
        self.target = target
        self.up = Vec3(0, 1, 0)
        self.fov = fov
        self.aspect = aspect
        self.near = 0.1
        self.far = 100

    def view_matrix(self):
        forward = normalize(subtract(self.position, self.target))
        right = normalize(cross(self.up, forward))
        up = cross(forward, right)

        return [
            [right.x, right.y, right.z, -dot(right, self.position)],
            [up.x, up.y, up.z, -dot(up, self.position)],
            [forward.x, forward.y, forward.z, -dot(forward, self.position)],
            [0, 0, 0, 1],
        ]

    def projection_matrix(self):
        fov_radians = math.radians(self.fov)
        f = 1 / math.tan(fov_radians / 2)

        near = self.near
        far = self.far

        return [
            [f / self.aspect, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, (far + near) / (near - far), (2 * far * near) / (near - far)],
            [0, 0, -1, 0],
        ]
