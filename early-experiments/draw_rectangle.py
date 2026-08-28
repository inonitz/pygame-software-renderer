import pygame
from numpy.random import randint as rand
import numpy as np


def gen_point(arg1, arg2):
    return rand(0, arg1), rand(0, arg2)




def main():
    pygame.init()
    pygame.display.init()
    w, h = 1280, 720
    square = [[400, 400],
              [600, 400],
              [600, 600],
              [400, 600]]
    colors = (0, 249, 0), (255, 255, 255), (255, 0, 255), (124, 4, 211)
    win = pygame.display.set_mode(size=(w, h), flags=pygame.RESIZABLE)

    win.fill(colors[1])
    while True:
        for i in range(len(square) - 1, -2, -1):
            pygame.draw.line(win, colors[0], square[i], square[i - 1], 5)
            pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break


if __name__ == '__main__':
    main()