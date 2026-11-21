import math

from PIL import Image

from shader import interpolate

MAX_COLOR = 255


def edge_function(ax, ay, bx, by, px, py):
    return (bx - ax) * (py - ay) - (by - ay) * (px - ax)


def color_to_byte(value):
    if value < 0:
        value = 0
    if value > 1:
        value = 1
    return int(value * MAX_COLOR)


class Rasterizer:
    def __init__(self, width, height, background_color):
        self.width = width
        self.height = height
        self.image = Image.new("RGB", (width, height), background_color)

        self.depth_buffer = []
        for i in range(width * height):
            self.depth_buffer.append(math.inf)

    def draw_model(self, triangles, shader):
        for triangle in triangles:
            clip_positions = []
            outputs = []

            for vertex in triangle:
                clip_position, output = shader.vertex(vertex)
                clip_positions.append(clip_position)
                outputs.append(output)

            self.draw_triangle(clip_positions, outputs, shader)

    def draw_triangle(self, clip_positions, outputs, shader):
        screen_x = []
        screen_y = []
        depth = []

        for clip in clip_positions:
            x = clip[0]
            y = clip[1]
            z = clip[2]
            w = clip[3]

            if w <= 0:
                return

            ndc_x = x / w
            ndc_y = y / w
            ndc_z = z / w

            screen_x.append((ndc_x + 1) / 2 * self.width)
            screen_y.append((1 - ndc_y) / 2 * self.height)
            depth.append(ndc_z)

        x0 = screen_x[0]
        x1 = screen_x[1]
        x2 = screen_x[2]
        y0 = screen_y[0]
        y1 = screen_y[1]
        y2 = screen_y[2]

        area = edge_function(x0, y0, x1, y1, x2, y2)
        if area == 0:
            return

        min_x = int(min(screen_x))
        max_x = int(max(screen_x)) + 1
        min_y = int(min(screen_y))
        max_y = int(max(screen_y)) + 1

        min_x = max(min_x, 0)
        min_y = max(min_y, 0)
        max_x = min(max_x, self.width - 1)
        max_y = min(max_y, self.height - 1)

        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                pixel_x = x + 0.5
                pixel_y = y + 0.5

                b0 = edge_function(x1, y1, x2, y2, pixel_x, pixel_y) / area
                b1 = edge_function(x2, y2, x0, y0, pixel_x, pixel_y) / area
                b2 = edge_function(x0, y0, x1, y1, pixel_x, pixel_y) / area

                if b0 < 0 or b1 < 0 or b2 < 0:
                    continue

                z = b0 * depth[0] + b1 * depth[1] + b2 * depth[2]
                index = y * self.width + x

                if z >= self.depth_buffer[index]:
                    continue

                self.depth_buffer[index] = z

                data = interpolate(outputs, b0, b1, b2)
                color = shader.fragment(data)

                red = color_to_byte(color.x)
                green = color_to_byte(color.y)
                blue = color_to_byte(color.z)
                self.image.putpixel((x, y), (red, green, blue))

    def save(self, path):
        self.image.save(path)
