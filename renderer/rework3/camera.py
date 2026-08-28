from rework3.math import *
from numpy.linalg import inv
from numpy import deg2rad as rad
import time
import pygame


class Camera:
    def __init__(self, window_dim, aspect_ratio, fov, near, far, eye, at, up=np.array([0, 1, 0])):
        self.n, self.f, self.ar, self.fov = near, far, aspect_ratio, fov
        self.eye = eye
        self.front = np.array([0, 0, -1])
        self.matrices = {"projection": get_perspective_projection(near, far, aspect_ratio, fov),
                         "worldToView": get_LookAt(eye, at, up=np.array([0, 1, 0]))}

        #  Moving the camera:
        # 1. Mouse callback moving
        self.sensitivity = 0.02
        self.last_pos = window_dim[0] / 2, window_dim[1] / 2
        self.yaw = rad(60)
        self.pitch = rad(60)

        # 2. Key callback
        self.t0 = time.time()
        self.t = time.time()
        self.dt = self.t0 - self.t
        self.speed = 0.2

    def update_view(self):
        self.matrices["worldToView"] = get_LookAt(self.eye, self.eye + self.front)

    def update_projection(self):
        self.matrices["projection"] = get_perspective_projection(self.n, self.f, self.ar, self.fov)

    def MVP(self, mat):
        Pv = np.matmul(self.matrices["projection"], np.matmul(self.matrices["worldToView"], mat))
        Pv = np.array([np.divide(Pv[i, 0:2], Pv[:, -1][0]) for i in range(len(Pv))])
        return Pv

    def key_callback(self, key):
        if key == pygame.K_w:
            self.eye = np.add(self.eye, self.speed * self.front)
        elif key == pygame.K_s:
            self.eye = np.subtract(self.eye, self.speed * self.front)
        elif key == pygame.K_a:
            self.eye = np.subtract(self.eye, normal(np.cross(self.front, [0, 1, 0])) * self.speed)
        elif key == pygame.K_d:
            self.eye = np.add(self.eye, normal(np.cross(self.front, [0, 1, 0])) * self.speed)

        self.dt = self.t0 - self.t
        self.speed = 2 * self.dt

    def mouse_callback(self, mouse_pos):
        offset = np.subtract(self.last_pos, mouse_pos) * self.sensitivity
        self.last_pos = mouse_pos
        self.pitch -= offset[1]
        self.yaw -= offset[0]

        if self.pitch > 89:
            self.pitch = 89
        elif self.pitch < -89:
            self.pitch = -89

        self.front = normal(
            np.array([cos(self.pitch) * cos(self.yaw), sin(self.pitch), cos(self.pitch) * sin(self.yaw)]))

    def debug(self):
        return "Position: {}, front: {}, at: {} ".format(self.eye, self.front, np.add(self.eye, self.front))
