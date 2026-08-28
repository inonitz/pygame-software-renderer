import pygame
import numpy as np

pygame.init()


class Window:
    # normalization is done in bounds [-1, 1], where [0,0] is the middle
    def __init__(self, width, height, a, b):
        self.screen = pygame.display.set_mode((width, height))
        self.width = width
        self.height = height
        self.a, self.b = a, b
        self.AspectRatio = height / width
        self.running = False
        self.event_queue = []
        self.draw_queue = []

        self.mousePos = []
        self.mouse_sens = .25

    def draw_pixel(self, pos, col):
        # if 0 <= pos[0] <= self.width and 0 <= pos[1] <= self.height:
        pygame.draw.line(self.screen, col, pos, pos)

    def draw_line(self, pos0, pos1, col):
        if type(pos0) == np.ndarray or type(pos1) == np.ndarray:
            pos0 = pos0.tolist()
            pos1 = pos1.tolist()
        # if -1 < pos0[0] < 1 and -1 < pos0[1] < 1 and -1 < pos1[0] < 1 and -1 < pos1[1] < 1:
        pos0 = self.normalize(pos0)
        pos1 = self.normalize(pos1)
        dy = (pos1[1] - pos0[1])
        dx = (pos1[0] - pos0[0])
        inc_const = 1
        if dy == 0:
            yBounds = [pos0[0], pos1[0]]
            yBounds.sort()
            x = yBounds[0]
            while x <= yBounds[1]:
                self.draw_pixel((x, pos0[1]), col)
                x += inc_const

        elif dx == 0:
            xBounds = [pos0[1], pos1[1]]
            xBounds.sort()
            y = xBounds[0]
            while y <= xBounds[1]:
                self.draw_pixel((pos0[0], y), col)
                y += inc_const
        else:
            m = dy / dx
            yBounds = [pos0[0], pos1[0]]
            yBounds.sort()
            x = yBounds[0]
            dx = (yBounds[1] - x) / 1000
            while x <= yBounds[1]:
                y = m * (x - pos0[0]) + pos0[1]
                self.draw_pixel((x, y), col)
                x += dx

    def draw_triangle_equalParams(self, color, vertexSorted, grad_list):
        """
        The Purpose of this function is to fill triangles which has dy's/dx's which are equal to 0,
        and so they require taking care of edge cases, which i'm not very fond of.
        There are 6 edge cases, which need to be taken care of & will be taken care of in this function.
         0? dx0  dx1  dx2  dy0  dy1  dy2
        """
        dx0, dx1, dx2, dy0, dy1, dy2 = grad_list
        vertexSorted.sort(key=lambda vertex: vertex[0], reverse=False)
        self.draw_pixel(vertexSorted[0], (255, 0, 0))
        self.draw_pixel(vertexSorted[1], (255, 0, 0))
        self.draw_pixel(vertexSorted[2], (255, 0, 0))

    def draw_triangle(self, vertices, col, fill=True):
        if len(vertices) != 3:
            raise ValueError("length of vertices array must equal 3 to draw a triangle!")
        else:
            if type(vertices) == np.ndarray:
                vertices = vertices.tolist()
            self.draw_line(vertices[0], vertices[1], col)
            self.draw_line(vertices[1], vertices[2], col)
            self.draw_line(vertices[2], vertices[0], col)
            if fill:
                vertexSorted = vertices
                vertexSorted.sort(key=lambda vertex: vertex[1], reverse=True)
                dx0, dx1, dx2 = vertexSorted[2][0] - vertexSorted[0][0], vertexSorted[1][0] - vertexSorted[0][0], \
                                vertexSorted[2][0] - vertexSorted[1][0]
                dy0, dy1, dy2 = vertexSorted[2][1] - vertexSorted[0][1], vertexSorted[1][1] - vertexSorted[0][1], \
                                vertexSorted[2][1] - vertexSorted[1][1]
                check_zero = [dx0, dx1, dx2, dy0, dy1, dy2]
                check_flag = True
                i = 0
                while i < len(check_zero) and check_flag:
                    if check_zero[i] == 0:
                        check_flag = False
                        self.draw_triangle_equalParams(col, vertexSorted, check_zero)
                    i += 1

                if check_flag:
                    m0 = dy0 / dx0
                    m1 = dy1 / dx1
                    m2 = dy2 / dx2
                    inc_const = .95
                    y_sub = self.normalizeH(vertexSorted[0][1])
                    while y_sub <= self.normalizeH(vertexSorted[1][1]):
                        y = self.normalizeH(y_sub, rev=False)
                        x0 = (y - vertexSorted[0][1]) / m0 + vertexSorted[0][0]
                        x1 = (y - vertexSorted[0][1]) / m1 + vertexSorted[0][0]
                        self.draw_line((x0, y), (x1, y), col)
                        y_sub += inc_const
                    y_sub = self.normalizeH(vertexSorted[1][1])
                    while y_sub <= self.normalizeH(vertexSorted[2][1]):
                        y = self.normalizeH(y_sub, rev=False)
                        x0 = (y - vertexSorted[2][1]) / m2 + vertexSorted[2][0]
                        x1 = (y - vertexSorted[2][1]) / m0 + vertexSorted[2][0]
                        self.draw_line((x0, y), (x1, y), col)
                        y_sub += inc_const

    """
    To normalize V between [x, y]:
    Vn = y-x * ( v - min(v) ) / ( max(v) - min(v) ) + x
    for val in range[0, h] we normalize to --> [1, -1]
    """

    def normalizeH(self, val, rev=True):
        a = -self.a
        b = -self.b
        if rev:
            return (val - a) * self.height / (b - a)
        return (b - a) * val / self.height + a

    def normalizeW(self, val, rev=True):
        if rev:
            return ((val - self.a) * self.width) / (self.b - self.a)
        return (self.b - self.a) * val / self.width + self.a

    def normalize(self, val, rev=True):
        if rev:
            return [self.normalizeW(val[0]), self.normalizeH(val[1])]
        return [self.normalizeW(val[0], rev=False), self.normalizeH(val[1], rev=False)]

    def start_program(self):
        self.running = True
        event_copy = self.event_queue.copy()
        while self.running:
            self.mousePos.append(pygame.mouse.get_pos())
            if len(self.event_queue) != 0:
                string = str(self.remove_event())
                eval(string)
            else:
                self.event_queue = event_copy
            self.check_quit()

    def draw(self, draw_call):
        self.draw_queue.insert(len(self.draw_queue), draw_call)

    def push_event(self, event):
        le = len(self.event_queue)
        self.event_queue.insert(le, event)

    def remove_event(self):
        return self.event_queue.pop(0)

    def check_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        pygame.display.update()

    def clear(self, col=(0, 0, 0)):
        self.screen.fill(col)
        pygame.display.update()

    def getMousePos(self):
        return pygame.mouse.get_pos()

    def setMouseSensitivity(self, sensitivity):
        self.mouse_sens = sensitivity
