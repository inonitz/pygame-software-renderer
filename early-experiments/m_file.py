import numpy as np
import pygame


class project_3d:
    def __init__(self, w, h):
        pygame.init()
        pygame.display.init()
        self.win = pygame.display.set_mode(size=(w, h), flags=pygame.RESIZABLE)
        """
        How The vectors are rotated then projected:
                [[x],
                  y],   <--- Vector (shape = (3, 1)) 
                  z]] 
                  
                [[0.72980565,  0.56106888, 0.41662344],
                 [0.80145539,  0.91094252, 0.1699921 ],    <--- Rotation matrix (shape = (3, 3))
                 [0.833717  ,  0.20763845, 0.39009586]])
                 
                 [[1, 0, 0],     <--- Projection matrix (shape = (3, 2))
                  [0, 1, 0]]
                
                operations:
                    1. np.matmul(Vector, Rotation matrix)
                    2. np.matmul(result(1), Projection matrix)
        """

        self.w, self.h = w, h
        self.const_amount = 20
        self.projection_mat = [1, 0, 0], \
                              [0, 1, 0]

        self.cube = np.array([[640, 640, 640],
                              [640, 360, 640],
                              [360, 360, 640],
                              [640, 360, 640],
                              [640, 360, 360],
                              [640, 640, 360],
                              [360, 640, 360],
                              [360, 360, 360]])
        self.colors = (0, 249, 0), (255, 255, 255), (255, 0, 255), (124, 4, 211)
        self.win.fill(self.colors[1])

    def rotateX(self, vector, ang):
        x = [1, 0, 0], \
            [0, np.cos(ang), -np.sin(ang)], \
            [0, np.sin(ang), np.sin(ang)]
        return np.matmul(x, vector)

    def rotateY(self, vector, ang):
        y = [np.cos(ang), 0, np.sin(ang)], \
            [0, 1, 0], \
            [-np.sin(ang), 0, np.cos(ang)]
        return np.matmul(y, vector)

    def rotateZ(self, vector, ang):
        z = [np.cos(ang), -np.sin(ang), 0], \
            [np.sin(ang), np.sin(ang), 0], \
            [0, 0, 1]

        return np.matmul(z, vector)

    def reduce_axis(self, axis, amount):
        idx = 0
        if axis == 'y':
            idx = 1
        elif axis == 'z':
            idx = 2

        for i in range(len(self.cube)):
            self.cube[i][idx] -= amount

    def increase_axis(self, axis, amount):
        idx = 0
        if axis == 'y':
            idx = 1
        elif axis == 'z':
            idx = 2

        for i in range(len(self.cube)):
            self.cube[i][idx] += amount

    def key_pressed(self, event, v, a):
        if event.type == pygame.KEYDOWN:
            self.rotateZ(v, -a)
        elif event.type == pygame.KEYUP:
            self.rotateZ(v, a)
        elif event.type == pygame.K_LEFT:
            self.rotateX(v, -a)
        elif event.type == pygame.K_RIGHT:
            self.rotateX(v, a)
        elif event.type == pygame.K_w:
            self.increase_axis('y', self.const_amount)
        elif event.type == pygame.K_d:
            self.reduce_axis('y', self.const_amount)

    def project_vec(self, vector):
        return np.matmul(self.projection_mat, vector)

    def run(self):
        a = np.deg2rad(35)
        while True:
            v = 0
            for i in range(100):
                for i in range(len(self.cube) - 1, -2, -1):
                    v = self.cube[i].reshape(3, 1)
                    p = self.project_vec(v)
                    pygame.draw.circle(self.win, self.colors[2], (p[0][0], p[1][0]), 10)

                    for event in pygame.event.get():
                        self.key_pressed(event, v, a)
                        if event.type == pygame.QUIT:
                            break

                        pygame.display.update()
            self.win.fill(self.colors[1])


x = project_3d(w=1280, h=720)
x.run()

"""
Comment:
Re-Make this, but this time: firat draw all the points properly.
                             then, use arrow keys to go left and right up and down (x, y)
                             Also, dont update it as you do, because its very clutterly and looks bad. Try and make sure
                             that you dont have to include everything in the while Loop.
                             P.S: Make lots of functions.

"""
