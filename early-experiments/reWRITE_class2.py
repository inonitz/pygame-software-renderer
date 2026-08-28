import numpy as np
import pygame
import sys


class reWRITE_3D:
    def __init__(self, w, h):
        self.win = pygame.display.set_mode(size=(w, h), flags=pygame.RESIZABLE)
        self.colors = (0, 249, 0), (255, 255, 255), (255, 0, 255), (124, 4, 211), (0, 150, 150)

        self.w = w
        self.h = h

        # constants
        self.camera_posx = 50
        self.camera_posy = 50
        self.a = 350 + self.camera_posx
        self.b = 175 + self.camera_posy
        self.line_w = 1
        self.point_r = 1
        self.rot_const = 3

        self.update_cube = []
        self.cube = np.array([[self.a, self.a, self.a],
                              [self.a, self.b, self.a],
                              [self.b, self.b, self.a],
                              [self.b, self.a, self.a],
                              [self.a, self.a, self.b],
                              [self.a, self.b, self.b],
                              [self.b, self.b, self.b],
                              [self.b, self.a, self.b]])
        self.normalize_cube()

        pygame.init()
        pygame.display.init()
        self.win.fill(self.colors[4])

    def normalize_cube(self):
        self.cube = [vector.reshape(3, 1) for vector in self.cube]

    @staticmethod
    def project_vec(vector):
        projection_mat = [1, 0, 0], \
                         [0, 1, 0]
        return np.matmul(projection_mat, vector)

    @staticmethod
    def rotateX(vector, ang):
        x = [1, 0, 0], \
            [0, np.cos(ang), -np.sin(ang)], \
            [0, np.sin(ang), np.cos(ang)]
        return np.matmul(x, vector)

    @staticmethod
    def rotateY(vector, ang):
        y = [np.cos(ang), 0, np.sin(ang)], \
            [0, 1, 0], \
            [-np.sin(ang), 0, np.cos(ang)]
        return np.matmul(y, vector)

    @staticmethod
    def rotateZ(vector, ang):
        z = [np.cos(ang), -np.sin(ang), 0], \
            [np.sin(ang), np.cos(ang), 0], \
            [0, 0, 1]
        return np.matmul(z, vector)

    def zoom_in(self):
        self.cube = np.array([np.multiply(vector, 1.01) for vector in self.cube])

    def zoom_out(self):
        self.cube = np.array([np.divide(vector, 1.01) for vector in self.cube])

        #  Make tidier
        # Fix rotation around the left of screen instead of front

    def move(self, dir):
        dir = dir.lower()
        for j in range(len(self.cube)):
            if dir == 'up':
                self.cube[j][1] -= 15
            elif dir == 'down':
                self.cube[j][1] += 15
            elif dir == 'left':
                self.cube[j][0] -= 15
            elif dir == 'right':
                self.cube[j][0] += 15

            pygame.display.update()

    def draw_loop(self):
        a = 0
        while True:
            # self.rotateY(self.cube, a)
            for i in range(2):
                # self.update_cube = self.rotateZ(self.cube, a)
                self.update_cube = self.cube
                self.update_cube = self.project_vec(self.update_cube)
                # [print(i, self.update_cube[i]-[175, 175]) for i in range(len(self.update_cube))]

                # [pygame.draw.circle(self.win, self.colors[0], vector, 4) for vector in self.update_cube]
                pygame.display.update()

                [pygame.draw.line(self.win, self.colors[0], self.update_cube[0:4][i - 1], self.update_cube[0:4][i], self.line_w) for i in range(len(self.update_cube[0:4]))]
                pygame.display.update()
                [pygame.draw.line(self.win, self.colors[0], self.update_cube[4:8][i - 1], self.update_cube[4:8][i], self.line_w) for i in range(len(self.update_cube[4:8]))]
                pygame.display.update()
                [pygame.draw.line(self.win, self.colors[0], self.update_cube[i], self.update_cube[i + 4], self.line_w) for i in range(int(len(self.update_cube)/2))]
                pygame.display.update()

                # a += .001

            self.win.fill(self.colors[4])
            keys_pressed = pygame.key.get_pressed()
            self.key_pressed(keys_pressed)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def key_pressed(self, keys_pressed):
        if keys_pressed[pygame.K_LEFT]:
            self.move('LEFT')
        elif keys_pressed[pygame.K_RIGHT]:
            self.move('RIGHT')
        elif keys_pressed[pygame.K_UP]:
            self.move('UP')
        elif keys_pressed[pygame.K_DOWN]:
            self.move('DOWN')
        elif keys_pressed[pygame.K_w]:
            self.cube = self.rotateZ(self.cube, -np.deg2rad(self.rot_const))
        elif keys_pressed[pygame.K_s]:
            self.cube = self.rotateZ(self.cube, np.deg2rad(self.rot_const))
        elif keys_pressed[pygame.K_d]:
            self.cube = self.rotateY(self.cube, np.deg2rad(self.rot_const))
        elif keys_pressed[pygame.K_a]:
            self.cube = self.rotateY(self.cube, -np.deg2rad(self.rot_const))
        elif keys_pressed[pygame.K_r]:
            self.cube = self.rotateX(self.cube, np.deg2rad(self.rot_const))
        elif keys_pressed[pygame.K_q]:
            self.cube = self.rotateX(self.cube, -np.deg2rad(self.rot_const))
        elif keys_pressed[pygame.K_z]:
            self.zoom_in()
        elif keys_pressed[pygame.K_c]:
            self.zoom_out()
        elif keys_pressed[pygame.K_e]:
            self.rot_const -= .5
            if self.rot_const <= 0:
                self.rot_const = 0.5


window_3D = reWRITE_3D(700, 700)
window_3D.draw_loop()
