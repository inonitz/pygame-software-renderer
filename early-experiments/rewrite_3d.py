import numpy as np
import pygame
import sys

pygame.init()
pygame.display.init()


def project_vec(vector):
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


def draw_point(po):
    pygame.draw.circle(win, colors[0], po, 5)


def connect_lines(p1, p2):
    pygame.draw.line(win, colors[0], p1, p2, 5)
    pygame.display.update()


def draw_cube():
    for i in range(len(projected[0:4])):
        connect_lines(projected[i - 1], projected[i])

    for i in range(len(projected[4:8])):
        connect_lines(projected[i - 1], projected[i])

    for i in range(4):
        connect_lines(projected[i], projected[i + 4])

    pygame.display.update()


def up():
    for j in range(len(cube)):
        cube[j][1] -= 30

    pygame.display.update()


def down():
    for j in range(len(cube)):
        cube[j][1] += 30
    pygame.display.update()


def left():
    for j in range(len(cube)):
        cube[j][0] -= 30
    pygame.display.update()


def right():
    for j in range(len(cube)):
        cube[j][0] += 30
    pygame.display.update()


xoffset, yoffset = 100, 100
w, h = 700, 700
a, b = 350+xoffset, 175+yoffset
win = pygame.display.set_mode(size=(w, h), flags=pygame.RESIZABLE)

colors = [ (0, 249, 0), (255, 255, 255), (255, 0, 255), (124, 4, 211), (0, 255, 255) ]
projection_mat = [1, 0, 0], \
                 [0, 1, 0]

projected = []
rot_cube = []
cube = np.array([[a, a, a],
                 [a, b, a],
                 [b, b, a],
                 [b, a, a],
                 [a, a, b],
                 [a, b, b],
                 [b, b, b],
                 [b, a, b]])

win.fill(colors[1])

while True:
    v = 0
    a = 0
    for i in range(len(cube)):
        v = cube[i].reshape(3, 1)
        r = rotateY(v, np.deg2rad(a))
        p = project_vec(r)
        projected.append(p)
        print(p[0].shape )
        pygame.draw.circle(win, colors[0], center=( p[0][0], p[1][0] ), radius=5)
        pygame.display.update()
        a += 10

    win.fill(colors[1])
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_LEFT]:
        left()
    if keys_pressed[pygame.K_RIGHT]:
        right()
    if keys_pressed[pygame.K_UP]:
        up()
    if keys_pressed[pygame.K_DOWN]:
        down()
    if keys_pressed[pygame.K_a]:
        for i in range(len(cube)):
            rot_cube.append(rotateY(cube[i], np.deg2rad(30)))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
