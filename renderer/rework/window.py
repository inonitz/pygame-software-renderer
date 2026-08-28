import pygame
import numpy as np

pygame.init()


class Window:
    # normalization is done in bounds [-1, 1], where [0,0] is the middle
    def __init__(self, width, height, a, b):
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.width = width
        self.height = height
        self.a, self.b = a, b
        self.AspectRatio = height / width
        self.running = False
        self.event_queue = []
        self.draw_queue = []

        self.mousePos = []
        self.mouse_sens = 0.2


    def start_program(self):
        self.running = True
        while self.running:
            self.clear()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

    def update(self):
        pygame.display.update()

    def clear(self, col=(0, 0, 0)):
        self.screen.fill(col)

    @staticmethod
    def getMousePos():
        return pygame.mouse.get_pos()

    def setMouseSensitivity(self, sensitivity):
        self.mouse_sens = sensitivity

    @staticmethod
    def setMousePos(posX, posY):
        pygame.mouse.set_pos(posX, posY)
