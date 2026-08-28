import pygame
import OpenGL as gl


class test3d:
    class camera:
        def __init__(self, pos, fov, rotation):
            self.pos = pos
            self.fov = fov
            self.a = rotation

    class cube:
        def __init__(self):
            pass
