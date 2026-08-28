import pygame
import pygame.gfxdraw
from rework3.camera import *
from rework3.renderer import *

pygame.font.init()


class gui:
    def __init__(self, w_width, w_height):
        self.window = pygame.display.set_mode((w_width, w_height), pygame.RESIZABLE)
        self.win_dim = [w_width, w_height]
        self.fill_col = [100, 100, 100]
        self.camera = Camera
        self.renderer = Renderer(self.window)

    # def draw_poly(self, vertices, color):
    #     pygame.draw.polygon(self.window, color, vertices)
    #
    # def draw_poly_wire(self, vertices, color, mesh=True):
    #     if mesh:
    #         self.renderer.mesh()
    #     pygame.gfxdraw.polygon(self.window, vertices, color)


    def toScreenCoords(self, vertex_array):
        return np.array([np.multiply(vertex_array[i].flatten(), self.win_dim) for i in range(len(vertex_array))])

    def render_debug(self):
        font = pygame.font.SysFont("Comic Sans MS", 15)
        surf = font.render(self.camera.debug(), False, (255, 255, 255), self.fill_col)
        self.window.blit(surf, (0, 0))

    def show_text(self, position, text, font, size, color, background_col=None):
        if background_col is None:
            background_col = self.fill_col
        font = pygame.font.SysFont(font, size)

        self.window.blit(font.render(text, False, color, background_col), position)

    def clear(self):
        self.window.fill(self.fill_col)

    def update(self):
        pygame.display.update()
        # print(self.camera.dt, self.camera.t0, self.camera.t, self.camera.dt)
        self.camera.t0 = self.camera.t
        self.camera.t = time.time()
