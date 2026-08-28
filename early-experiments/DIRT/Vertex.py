import math


class Vertex:

    def __init__(self, x, y, z):

        self.x = x
        self.y = y
        self.z = z

    def getx(self):
        return self.x

    def gety(self):
        return self.y

    def getz(self):
        return self.z

    def rotate_x(self, x_angle):

        if x_angle == 0:
            return self

        x = self.x * math.cos(x_angle) + self.z * math.sin(x_angle)

        y = self.y

        z = self.z * math.cos(x_angle) - self.x * math.sin(x_angle)

        return Vertex(x, y, z)

    def __str__(self):
        return "x: {0}, y: {1}, z:{2}".format(self.x, self.x, self.z)

    def rotate_y(self, y_angle):

        if y_angle == 0:
            return self

        x = self.x

        y = self.y * math.cos(y_angle) + self.z * math.sin(y_angle)

        z = self.z * math.cos(y_angle) - self.y * math.sin(y_angle)

        return Vertex(x, y, z)

    def get_dist(self, camera):

        return (self.x - camera.x)**2 + (self.y - camera.y)**2 + (self.z - camera.z)**2
