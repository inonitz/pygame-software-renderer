import math
from Vertex import Vertex


class Camera:

    def __init__(self, x, y, z, xangle, yangle):

        self.x = x
        self.y = y
        self.z = z
        self.xangle = xangle
        self.yangle = yangle

    def isproject(self, vertex, screen):  # return a boolean value of whether a vertex is projectable

        new_vertex = Vertex(vertex.x - self.x, vertex.y - self.y, vertex.z - self.z)

        new_vertex = new_vertex.rotate_x(self.xangle)
        new_vertex = new_vertex.rotate_y(self.yangle)

        try:
            x = int(new_vertex.x * screen.get_size()[0] / new_vertex.z / 2 + screen.get_size()[0] / 2)
            y = int(new_vertex.y * screen.get_size()[1] / new_vertex.z / 2 + screen.get_size()[1] / 2)

            if abs(x) > screen.get_size()[0]*2 or abs(y) > screen.get_size()[1]*2 or new_vertex.z < 0:

                return False

        except ArithmeticError or OverflowError:
            return False

        return True

    def __str__(self):
        return "x: {0}, y: {1}, z:{2}".format(self.x, self.y, self.z)

    def project(self, vertex, screen):  # returns the projected coordinated of the vertex relative to the camera

        new_vertex = Vertex(vertex.x - self.x, vertex.y - self.y, vertex.z - self.z)

        new_vertex = new_vertex.rotate_x(self.xangle)
        new_vertex = new_vertex.rotate_y(self.yangle)

        x = new_vertex.x * screen.get_size()[0] / new_vertex.z / 2 + screen.get_size()[0] / 2
        y = new_vertex.y * screen.get_size()[1] / new_vertex.z / 2 + screen.get_size()[1] / 2

        return int(x), int(y)

    def move_forward(self, distance):  # moves camera forward some distance

        self.x -= distance * math.sin(self.xangle)
        self.z += distance * math.cos(self.xangle)

    def move_backward(self, distance):

        self.x += distance * math.sin(self.xangle)
        self.z -= distance * math.cos(self.xangle)

    def move_right(self, distance):

        self.x += distance * math.cos(self.xangle)
        self.z += distance * math.sin(self.xangle)

    def move_left(self, distance):

        self.x -= distance * math.cos(self.xangle)
        self.z -= distance * math.sin(self.xangle)

    def rotate(self, dif):  # rotates the camera according to the difference in mouse position

        self.xangle += dif[0] * math.pi / 900

        if abs(self.yangle + dif[1] * math.pi / 900) <= math.pi / 2:

            self.yangle += dif[1] * math.pi / 900


def get_dif(old_pos, new_pos):

    return old_pos[0] - new_pos[0], old_pos[1] - new_pos[1]


base_camera = Camera(0, 0, 0, 0, 0)
