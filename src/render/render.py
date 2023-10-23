import math

import numpy as np

from .window import Window


def mmv(i, m):
    o = np.array([0, 0, 0], dtype=float)
    o[0] = i[0] * m[0][0] + i[1] * m[1][0] + i[2] * m[2][0] + m[3][0]
    o[1] = i[0] * m[0][1] + i[1] * m[1][1] + i[2] * m[2][1] + m[3][1]
    o[2] = i[0] * m[0][2] + i[1] * m[1][2] + i[2] * m[2][2] + m[3][2]
    w = i[0] * m[0][3] + i[1] * m[1][3] + i[2] * m[2][3] + m[3][3]

    if w != 0:
        o /= w

    return o


def load_obj(filename: str) -> np.ndarray:
    vertices = []
    triangles = []

    with open(filename, "r") as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip().split(" ")
            if line[0] == "v":
                vertices.append([float(line[1]), float(line[2]), float(line[3])])
            elif line[0] == "f":
                triangles.append(
                    [
                        vertices[int(line[1]) - 1],
                        vertices[int(line[2]) - 1],
                        vertices[int(line[3]) - 1],
                    ]
                )

        file.close()

    return np.array(triangles)


class Object3d:
    def __init__(self, triangles: np.ndarray) -> None:
        self.position = np.array([0, 0, 0], dtype=float)
        self.rotation = [
            np.array(
                [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], dtype=float
            )
        ] * 3
        self.triangles = triangles

    def translate(self, x: float, y: float, z: float) -> None:
        self.position += np.array([x, y, z], dtype=float)

    def rotate(self, x: float, y: float, z: float) -> None:
        rot_x = np.array(
            [
                [1, 0, 0, 0],
                [0, math.cos(x), math.sin(x), 0],
                [0, -math.sin(x), math.cos(x), 0],
                [0, 0, 0, 1],
            ]
        )
        rot_y = np.array(
            [
                [math.cos(y), 0, -math.sin(y), 0],
                [0, 1, 0, 0],
                [math.sin(y), 0, math.cos(y), 0],
                [0, 0, 0, 1],
            ]
        )
        rot_z = np.array(
            [
                [math.cos(z), math.sin(z), 0, 0],
                [-math.sin(z), math.cos(z), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]
        )

        self.rotation = (rot_x, rot_y, rot_z)


class Renderer:
    def __init__(
        self, display: Window, near: float = 0.1, far: float = 1000, fov: float = 90
    ) -> None:
        self.objects: list[Object3d] = []
        self.display = display
        self.near = near
        self.far = far
        self.fov = fov
        self.aspect_ratio = 1920 / 1080

    def sort_triangles(self, triangle):
        return (triangle[0][2] + triangle[1][2] + triangle[2][2]) / 3

    def render(self) -> None:
        fov_rad = 1 / math.tan(math.radians(self.fov) * 0.5)
        projection = np.array(
            [
                [self.aspect_ratio * fov_rad, 0, 0, 0],
                [0, fov_rad, 0, 0],
                [0, 0, self.far / (self.far - self.near), 1],
                [0, 0, (-self.far * self.near) / (self.far - self.near), 0],
            ]
        )

        light = np.array([0, 0, -1], dtype=float)
        light /= np.max(np.abs(light))

        camera = np.array([0, 0, 0], dtype=float)

        for obj in self.objects:
            dtriangles = []
            for triangle in obj.triangles:
                rtriangle = triangle.copy()
                rtriangle[0] = mmv(rtriangle[0], obj.rotation[0])
                rtriangle[1] = mmv(rtriangle[1], obj.rotation[0])
                rtriangle[2] = mmv(rtriangle[2], obj.rotation[0])

                rtriangle[0] = mmv(rtriangle[0], obj.rotation[1])
                rtriangle[1] = mmv(rtriangle[1], obj.rotation[1])
                rtriangle[2] = mmv(rtriangle[2], obj.rotation[1])

                rtriangle[0] = mmv(rtriangle[0], obj.rotation[2])
                rtriangle[1] = mmv(rtriangle[1], obj.rotation[2])
                rtriangle[2] = mmv(rtriangle[2], obj.rotation[2])

                ttriangle = rtriangle.copy()
                ttriangle[0][2] += 8
                ttriangle[1][2] += 8
                ttriangle[2][2] += 8
                ttriangle += obj.position

                normal = np.cross(
                    ttriangle[1] - ttriangle[0], ttriangle[2] - ttriangle[0]
                )
                normal /= np.max(np.abs(normal))

                if np.sum(normal * (ttriangle[0] - camera)) > 0:
                    # dtriangles.append(ttriangle)
                    ptriangle = ttriangle.copy()
                    ptriangle[0] = mmv(ptriangle[0], projection)
                    ptriangle[1] = mmv(ptriangle[1], projection)
                    ptriangle[2] = mmv(ptriangle[2], projection)

                    ptriangle[0][0] = round(
                        (1920 * 0.5) + (ptriangle[0][0] * 1920 * 0.5)
                    )
                    ptriangle[1][0] = round(
                        (1920 * 0.5) + (ptriangle[1][0] * 1920 * 0.5)
                    )
                    ptriangle[2][0] = round(
                        (1920 * 0.5) + (ptriangle[2][0] * 1920 * 0.5)
                    )
                    ptriangle[0][1] = round(
                        (1080 * 0.5) + (ptriangle[0][1] * 1080 * 0.5)
                    )
                    ptriangle[1][1] = round(
                        (1080 * 0.5) + (ptriangle[1][1] * 1080 * 0.5)
                    )
                    ptriangle[2][1] = round(
                        (1080 * 0.5) + (ptriangle[2][1] * 1080 * 0.5)
                    )
                    shade = np.abs(np.sum(normal * light) * 255).astype(int)
                    self.display.fill_triangle(ptriangle, (shade, shade, shade))

            dtriangles.sort(key=self.sort_triangles)
            for triangle in dtriangles:
                ptriangle = triangle.copy()
                ptriangle[0] = mmv(ptriangle[0], projection)
                ptriangle[1] = mmv(ptriangle[1], projection)
                ptriangle[2] = mmv(ptriangle[2], projection)

                ptriangle[0][0] = round((1920 * 0.5) + (ptriangle[0][0] * 1920 * 0.5))
                ptriangle[1][0] = round((1920 * 0.5) + (ptriangle[1][0] * 1920 * 0.5))
                ptriangle[2][0] = round((1920 * 0.5) + (ptriangle[2][0] * 1920 * 0.5))
                ptriangle[0][1] = round((1080 * 0.5) + (ptriangle[0][1] * 1080 * 0.5))
                ptriangle[1][1] = round((1080 * 0.5) + (ptriangle[1][1] * 1080 * 0.5))
                ptriangle[2][1] = round((1080 * 0.5) + (ptriangle[2][1] * 1080 * 0.5))

                shade = np.abs(np.sum(normal * light) * 255).astype(int)
                self.display.fill_triangle(ptriangle, (shade, shade, shade))
