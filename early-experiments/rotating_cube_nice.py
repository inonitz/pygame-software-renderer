import numpy as np
import pygame
import sys

pygame.init()
pygame.display.init()


def project_vec(vector):
    projection_mat = [1, 0, 0], \
                     [0, 1, 0]
    return np.matmul(projection_mat, vector)


def rotateX(vector, ang):
    x = [1, 0, 0], \
        [0, np.cos(ang), -np.sin(ang)], \
        [0, np.sin(ang), np.sin(ang)]
    return np.matmul(x, vector)


def rotateY(vector, ang):
    y = [np.cos(ang), 0, np.sin(ang)], \
        [0, 1, 0], \
        [-np.sin(ang), 0, np.cos(ang)]
    return np.matmul(y, vector)


def rotateZ(vector, ang):
    z = [np.cos(ang), -np.sin(ang), 0], \
        [np.sin(ang), np.sin(ang), 0], \
        [0, 0, 1]
    return np.matmul(z, vector)


def connect_lines(p1, p2):
    pygame.draw.line(win, colors[0], p1, p2, 5)
    pygame.display.update()


def draw_cube():
    for i in range(len(ncube[0:4])):
        connect_lines(ncube[i - 1], ncube[i])

    for i in range(len(ncube[4:8])):
        connect_lines(ncube[i - 1], ncube[i])

    for i in range(4):
        connect_lines(ncube[i], ncube[i + 4])

    pygame.display.update()


def zoom_out():
    pass


def zoom_in():
    pass


w, h = 700, 700
px, py = 175, 175
a, b = 350 + px, 175 + py
win = pygame.display.set_mode(size=(w, h), flags=pygame.RESIZABLE)
colors = (0, 249, 0), (255, 255, 255), (255, 0, 255), (124, 4, 211), (0, 255, 255)

cube = np.array([[a, a, a],
                 [a, b, a],
                 [b, b, a],
                 [b, a, a],
                 [a, a, b],
                 [a, b, b],
                 [b, b, b],
                 [b, a, b]])

ncube = []
a = 0
while True:
    for i in range(len(cube)):
        v = rotateY(cube[i].reshape(3, 1), a)
        p = project_vec(v)
        ncube.append(p)
        pygame.draw.circle(win, colors[0], center=( p[0][0], p[1][0] ), radius=5)
        pygame.display.update()

    # draw_cube()
    a += .01
    win.fill(colors[1])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    """
    This probably needs to be in class format (especially the points drawn to screen) ->
    (variable v, p) --> ncube doesn't draw lines properly
    
    How everything should work in the drawing loop:
        1. calculate vectors
        2. Draw them
        3. Then, if keystore == up/down/left/right:
            update pos of cube
            
        In order to zoom out (seeing more of cube) you need:
        to multiply the points (of the cube) by a constant that will shrink or increase
        (depending if youre zooming in or zooming out) -->
            zooming in --> point + const
            zooming out --> point - const
            
        functions needed:
        zoom in
        zoom out
        go left
        go right
        go up
        go down
        rotate x
        rotate y
        rotate z
        (probably) event handler for each transformation (preferably rotate functions)
    """