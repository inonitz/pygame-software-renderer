import pygame
import numba as nb
import numpy as np

def fill_tri_halfspace(vertices, color):
    xs, ys = vertices[:, 0], vertices[:, 1]
    step = 10
    minX, minY, maxX, maxY = np.min(xs), np.min(ys), np.max(xs), np.max(ys)
    print(minX, minY, maxX, maxY)
    j = minY
    i = minX
    while j < maxY:
        while i < maxX:
            pix_arr = np.array([i, i+step-1, j+step-1, j])
            flag = inside_tri(pix_arr[:2], minX, minY, maxX, maxY) and \
                    inside_tri(pix_arr[2:], minX, minY, maxX, maxY)
            if flag:
                draw_block(pix_arr, pygame.display.get_surface(), color)
                i += step
            elif not flag:
                i += step
                continue
            else:
                k = j, l = i
                while k < k+step:
                    while l < l+step:
                        if inside_tri([k, l], minX, minY, maxX, maxY):
                            pygame.display.get_surface().set_at((k, l), color)
                        l += 1
                    k += 1
                i += step
        j += step

@nb.njit()
def inside_tri(point, Xmin, Ymin, Xmax, Ymax):
    if Xmin <= point[0] <= Xmax and Ymin <= point[1] <= Ymax: return True
    return False

def draw_block(vertices, surface, color):
    i = vertices[0]
    j = vertices[1]
    while i < vertices[2]:
        while j < vertices[-1]:
            surface.set_at((i, j), color)
            j += 1
        i += 1

@nb.njit()
def normalize(point, w, h):
    x = 0.5*w * (point[0] + 1)
    y = 0.5*h * (point[1] + 1)
    return np.array([x, y])


width = 1080
height = 720
running = True
window = pygame.display.set_mode((width, height), pygame.HWSURFACE)


tri = np.random.rand(3, 2)
col = (255, 255, 255)
print(tri)
tri = np.array([normalize(vertex, width, height) for vertex in tri])
print(tri)
fill_tri_halfspace(tri, col)
pygame.display.update()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
