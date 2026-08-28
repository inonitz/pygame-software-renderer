import numpy as np
import pygame

pygame.init()
pygame.display.init()

w, h = 700, 700
a, b = 525, 175
win = pygame.display.set_mode(size=(w, h), flags=pygame.RESIZABLE)
colors = (0, 249, 0), (255, 255, 255), (255, 0, 255), (124, 4, 211)

win.fill(colors[0])
