from failed_attempts.window import *
import numpy as np
import pygame
import time

pygame.init()

window_width = 1080
window_height = 720
AspectR = window_width / window_height
win = Window(window_width, window_height, -1, 1)

color = np.random.randint(0, 255, (1, 3))
color = color.tolist()[0]

vertices0 = (2 * np.random.rand(3, 2) - 1).tolist()
# print(vertices0)
start = time.perf_counter()
for i in range(5):
    win.push_event(win.draw_triangle(vertices0, color, fill=True))
    win.push_event(win.update())
    vertices0 = (2 * np.random.rand(3, 2) - 1).tolist()
    color = np.random.randint(0, 255, (1, 3)).tolist()[0]
end = time.perf_counter()
print("time taken to draw triangle: {}".format(end-start))

square = np.array([[-1, 1], [1,  1], [-1,  -1], [1, -1]]) / AspectR
square = square.tolist()

square2 = np.array([[-1, -1], [1,  -1], [-1,  1], [1, 1]]) * AspectR * 0.5
square2 = square2.tolist()

triangles = [square[:3], [square[1], square[2], square[3]]]
# print(triangles)

start = time.perf_counter()
win.push_event(win.draw_triangle(triangles[0], (255, 255, 255), fill=False))
win.push_event(win.draw_triangle(triangles[1], (255, 255, 255), fill=False))
win.push_event(win.update())
end = time.perf_counter()
print("time taken to draw square: {}".format(end-start))
win.push_event(win.update())



win.start_program()
