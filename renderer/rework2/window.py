from rework2.math_short import *
import pygame
import pygame.gfxdraw


class Window:
    def __init__(self, width, height):
        self.window = pygame.display.set_mode((width, height), pygame.HWSURFACE)
        self.width = width
        self.height = height
        self.min = -1
        self.max = 1
        self.col_clear = [0, 0, 0]

    def normToScreen(self, norm_dev_coords):
        return [[self.width*0.5*(vertex[0] + 1), self.height*0.5*(vertex[1] + 1)] for vertex in norm_dev_coords]

    # Vec is column major, (2, 1) vector shape.
    def normToScreenVec(self, vec):
        return [self.width*0.5*(vec[0][0] + 1) if i == 0 else self.height*0.5*(vec[0][0] + 1) for i in range(len(vec))]

    def clip_triangle(self, vertices):
        pass

    def draw_triangle(self, vertices, col=(255, 255, 255), fill=True):
        if fill:
            pygame.draw.polygon(self.window, col, vertices)
        else:
            pygame.draw.polygon(self.window, col, vertices, 1)

    def draw_tri_gfx(self, verts, col=(255, 255, 255), fill=True):
        verts = np.array(verts).astype(int).flatten().tolist()
        if False not in [-32767 < p < 32767 for p in verts]:
            if fill:
                pygame.gfxdraw.filled_trigon(self.window,
                                             verts[0], verts[1], verts[2], verts[3], verts[4], verts[5],
                                             col)
            else:
                pygame.gfxdraw.aatrigon(self.window,
                                        verts[0], verts[1], verts[2], verts[3], verts[4], verts[5],
                                        col)

    def clear(self, col=None):
        self.window.fill(self.col_clear) if col is None else self.window.fill(col)

    def setFill(self, col):
        self.col_clear = col

    @staticmethod
    def update():
        pygame.display.update()
