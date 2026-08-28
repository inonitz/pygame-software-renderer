import numpy as np
import pygame

class Renderer:
    def __init__(self, context):
        self.context = context

    # def clip(self, vertices):
    #     if np.any(np.abs(vertices) == np.inf) or np.any(vertices == np.NaN):
    #         return
    #     return vertices

    def mesh(self, object):
        pygame.draw.polygon(self.context, object.color, object.vertices)

    def whole(self, object):
        pygame.draw.polygon(self.context, object.color, object.vertices, 1)

    def render(self, vertices, col):
        pygame.draw.polygon(self.context, col, vertices.tolist(), 1)

    @staticmethod
    def mesh_with_context(obj):
        pygame.draw.polygon(obj.context, obj.col, obj.vertices)

    @staticmethod
    def render_with_context(obj):
        pygame.draw.polygon(obj.context,  obj.col, obj.vertices, 1)

