from vectors import Vec3
from camera import Camera
from model import load_model
from shader import PhongShader
from rasterizer import Rasterizer

IMAGE_WIDTH = 800
IMAGE_HEIGHT = 800
BACKGROUND_COLOR = (0, 0, 0)

CAMERA_POSITION = Vec3(0, 0, 3)
CAMERA_TARGET = Vec3(0, 0, 0)
CAMERA_FOV = 50

MODEL_PATH = "models/african_head.obj"
OUTPUT_PATH = "output.png"

triangles = load_model(MODEL_PATH)

aspect = IMAGE_WIDTH / IMAGE_HEIGHT

camera = Camera(CAMERA_POSITION, CAMERA_TARGET, CAMERA_FOV, aspect)

view = camera.view_matrix()
projection = camera.projection_matrix()
shader = PhongShader(view, projection, camera.position)

rasterizer = Rasterizer(IMAGE_WIDTH, IMAGE_HEIGHT, BACKGROUND_COLOR)
rasterizer.draw_model(triangles, shader)
rasterizer.save(OUTPUT_PATH)

print("Saved", OUTPUT_PATH)
