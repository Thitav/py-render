import os
import time

import numpy as np

from render.render import Object3d, Renderer, load_obj
from render.window import Window

cube_mesh = np.array(
    [
        [[0, 0, 0], [0, 1, 0], [1, 1, 0]],
        [[0, 0, 0], [1, 1, 0], [1, 0, 0]],
        [[1, 0, 0], [1, 1, 0], [1, 1, 1]],
        [[1, 0, 0], [1, 1, 1], [1, 0, 1]],
        [[1, 0, 1], [1, 1, 1], [0, 1, 1]],
        [[1, 0, 1], [0, 1, 1], [0, 0, 1]],
        [[0, 0, 1], [0, 1, 1], [0, 1, 0]],
        [[0, 0, 1], [0, 1, 0], [0, 0, 0]],
        [[0, 1, 0], [0, 1, 1], [1, 1, 1]],
        [[0, 1, 0], [1, 1, 1], [1, 1, 0]],
        [[1, 0, 1], [0, 0, 1], [0, 0, 0]],
        [[1, 0, 1], [0, 0, 0], [1, 0, 0]],
    ],
    dtype=float,
)


# cube = Object3d(cube_mesh)
sphere = Object3d(load_obj(os.path.dirname(os.path.abspath(__file__)) + "\\sphere.obj"))
window = Window("Test")


renderer = Renderer(window)
renderer.objects.append(sphere)

window.show()
theta = 0
while True:
    theta += 0.05
    window.fill((0, 0, 0))

    sphere.rotate(theta, theta, theta)
    renderer.render()
    window.draw()

    window.update()
    time.sleep(1 / 60)
