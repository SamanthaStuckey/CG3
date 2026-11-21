import math


class Vec3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


def add(a, b):
    return Vec3(a.x + b.x, a.y + b.y, a.z + b.z)


def subtract(a, b):
    return Vec3(a.x - b.x, a.y - b.y, a.z - b.z)


def scale(v, number):
    return Vec3(v.x * number, v.y * number, v.z * number)


def multiply(a, b):
    return Vec3(a.x * b.x, a.y * b.y, a.z * b.z)


def dot(a, b):
    return a.x * b.x + a.y * b.y + a.z * b.z


def cross(a, b):
    x = a.y * b.z - a.z * b.y
    y = a.z * b.x - a.x * b.z
    z = a.x * b.y - a.y * b.x
    return Vec3(x, y, z)


def length(v):
    return math.sqrt(dot(v, v))


def normalize(v):
    v_length = length(v)
    if v_length == 0:
        return v
    return scale(v, 1 / v_length)
