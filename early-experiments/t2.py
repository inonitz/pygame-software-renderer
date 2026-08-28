import numpy as np
import pygame
import sys

pygame.init()
pygame.display.init()


def project_vec(vector):
    return np.matmul(projection_mat, vector)


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


def connect_lines(p1, p2):
    p1_coord = ( p1[0][0], p1[1][0] )
    p2_coord = ( p2[0][0], p2[1][0] )
    pygame.draw.line(win, colors[0], p1_coord, p2_coord, 5)
    pygame.display.update()


def draw_point(po):
    pygame.draw.circle(win, colors[0], center=( po[0][0], po[1][0] ), radius=10)


def update(fx):
    eval(fx)
    pygame.display.update()


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


# def rotate(axis, vec, ang):
#     ev = 'rotate' + axis.upper()
#
#     if type(vec) == np.array:
#         return eval(ev + '(vec, ang)')
#     elif type(vec) == list:
#         return [eval(ev + '(vec[i], ang)') for i in range(len(vec))]

def rotatep(axis, vec, ang):
    if axis == 'x':
        return [rotateX(vec[i].reshape(3, 1), ang) for i in range(len(vec))]
    elif axis == 'y':
        return [rotateY(vec[i].reshape(3, 1), ang) for i in range(len(vec))]
    elif axis == 'z':
        return [rotateZ(vec[i].reshape(3, 1), ang) for i in range(len(vec))]


xoffset, yoffset = 100, 100
w, h = 700, 700
a, b = 350+xoffset, 175+yoffset
win = pygame.display.set_mode(size=(w, h), flags=pygame.RESIZABLE)

colors = (0, 249, 0), (255, 255, 255), (255, 0, 255), (124, 4, 211)
projection_mat = [1, 0, 0], \
                 [0, 1, 0]

projected = []
cube = np.array([[a, a, a],
                 [a, b, a],
                 [b, b, a],
                 [b, a, a],
                 [a, a, b],
                 [a, b, b],
                 [b, b, b],
                 [b, a, b]])
win.fill(colors[1])
a = np.deg2rad(0)
while True:
    for i in range(len(cube)):
        v = cube[i].reshape(3, 1)
        p = project_vec(v)
        projected.append(p)
        pygame.draw.circle(win, colors[0], center=( p[0][0], p[1][0] ), radius=5)
        pygame.display.update()
        a += .001

    for i in range(len(projected[0:4])):
        connect_lines(projected[i - 1], projected[i])

    for i in range(len(projected[4:8])):
        connect_lines(projected[i - 1], projected[i])

    for i in range(4):
        connect_lines(projected[i], projected[i + 4])

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
        rotatep('z', projected, np.deg2rad(30))

    win.fill(colors[1])
    projected = []

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
