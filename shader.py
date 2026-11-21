from vectors import Vec3, add, subtract, scale, multiply, dot, normalize
from matrices import multiply_matrix_by_vector


class VertexOutput:
    def __init__(self, world_position, normal):
        self.world_position = world_position
        self.normal = normal


def interpolate(outputs, b0, b1, b2):
    position0 = scale(outputs[0].world_position, b0)
    position1 = scale(outputs[1].world_position, b1)
    position2 = scale(outputs[2].world_position, b2)
    world_position = add(add(position0, position1), position2)

    normal0 = scale(outputs[0].normal, b0)
    normal1 = scale(outputs[1].normal, b1)
    normal2 = scale(outputs[2].normal, b2)
    normal = add(add(normal0, normal1), normal2)

    return VertexOutput(world_position, normal)


class Shader:
    def vertex(self, vertex):
        pass

    def fragment(self, data):
        pass


class PhongShader(Shader):
    def __init__(self, view, projection, camera_position):
        self.view = view
        self.projection = projection
        self.camera_position = camera_position

        self.light_direction = normalize(Vec3(1, 1, 1))
        self.light_color = Vec3(1, 1, 1)
        self.object_color = Vec3(0.8, 0.6, 0.5)

        self.ambient_strength = 0.1
        self.specular_strength = 0.5
        self.shininess = 32

    def vertex(self, vertex):
        position = vertex.position
        point = [position.x, position.y, position.z, 1]

        point_in_camera = multiply_matrix_by_vector(self.view, point)
        clip_position = multiply_matrix_by_vector(self.projection, point_in_camera)

        output = VertexOutput(vertex.position, vertex.normal)
        return clip_position, output

    def fragment(self, data):
        normal = normalize(data.normal)
        to_light = self.light_direction
        to_camera = normalize(subtract(self.camera_position, data.world_position))

        ambient = scale(self.light_color, self.ambient_strength)

        diffuse_power = dot(normal, to_light)
        if diffuse_power < 0:
            diffuse_power = 0
        diffuse = scale(self.light_color, diffuse_power)

        reflected = subtract(scale(normal, 2 * dot(normal, to_light)), to_light)
        specular_power = dot(reflected, to_camera)
        if specular_power < 0 or diffuse_power == 0:
            specular_power = 0
        specular_power = specular_power ** self.shininess
        specular = scale(self.light_color, specular_power * self.specular_strength)

        color = multiply(add(ambient, diffuse), self.object_color)
        color = add(color, specular)
        return color
