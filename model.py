from vectors import Vec3


class Vertex:
    def __init__(self, position, normal):
        self.position = position
        self.normal = normal


def read_vec3(parts):
    x = float(parts[1])
    y = float(parts[2])
    z = float(parts[3])
    return Vec3(x, y, z)


def load_model(path):
    positions = []
    normals = []
    triangles = []

    file = open(path)

    for line in file:
        parts = line.split()

        if len(parts) == 0:
            continue

        if parts[0] == "v":
            positions.append(read_vec3(parts))

        if parts[0] == "vn":
            normals.append(read_vec3(parts))

        if parts[0] == "f":
            triangle = []

            for i in range(1, 4):
                numbers = parts[i].split("/")
                position_index = int(numbers[0]) - 1
                normal_index = int(numbers[2]) - 1

                vertex = Vertex(positions[position_index], normals[normal_index])
                triangle.append(vertex)

            triangles.append(triangle)

    file.close()

    return triangles
