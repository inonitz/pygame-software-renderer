import random


def abs(x):
    if x < 0:
        return -x


def sqrt(num):
    low, high = 0, num
    mid = float
    for i in range(10000):
        mid = (low + high) / 2
        if mid ** 2 == num:
            return mid
        elif mid ** 2 > num:
            high = mid
        else:
            low = mid
    return mid


def dot(vec1, vec2):
    if len(vec1) != len(vec2):
        raise Exception("Vectors must be equal length!")

    sum = 0
    for i in range(len(vec1)):
        sum += vec1[i] * vec2[i]


class transformations:
    def __init__(self):
        self.scale_mat = matrix(4, 4)
        self.translate_mat = matrix(4, 4)
        self.model_view_transformation_mat = matrix(4, 4)
        self.projection_mat = matrix(4, 4)
        self.projected_to_device = matrix(4, 4)

    def MVTransform(self, vec4):
        return self.model_view_transformation_mat.multiply(vec4)

    def project(self, vec4):
        return self.projection_mat.multiply(vec4)

    def proj_to_device(self, vec2):
        pass


class vector3f:
    def __init__(self, *args):
        self.vec = []
        self.T = False

        for arg in args:
            if type(arg) == vector3f:
                self.vec = arg.vec
                self.T = arg.T
            elif type(arg) == float or type(arg) == int:
                self.vec.append(arg)
            elif type(arg) == tuple and len(arg) == 3:
                self.vec = list(arg)
            elif type(arg) == list and len(arg) == 3:
                self.vec = arg

    def T(self):
        self.T = not self.T

    def mag(self):
        return abs(sqrt(self.vec[0] ** 2 + self.vec[1] ** 2 + self.vec[2] ** 2))

    def cross(self, vector):
        x = self.vec[1] * vector[2] - self.vec[2] * vector[1]
        y = self.vec[2] * vector[0] - self.vec[0] * vector[2]
        z = self.vec[0] * vector[1] - self.vec[1] * vector[0]
        return vector3f([x, y, z])

    def multiply_mag(self, mag):
        self.vec = [self.vec[i] * mag for i in range(len(self.vec))]

    def add(self, vector):
        self.vec = [self.vec[i] + vector.vec[i] for i in range(len(self.vec))]

    def sub(self, vector):
        self.vec = [self.vec[i] - vector.vec[i] for i in range(len(self.vec))]

    def normalize(self):
        self.vec = [self.vec[i] / self.mag() for i in range(len(self.vec))]

    def shape(self):
        if self.T:
            return 3, 1
        else:
            return 1, 3

    def __setitem__(self, key, value):
        self.vec[key] = value

    def __getitem__(self, key):
        if key < 3:
            return self.vec[key]

    def print(self):
        print("({}, {}, {})".format(self.vec[0], self.vec[1], self.vec[2]))


class matrix:
    def __init__(self, row, col, val=0, mat=None):
        self.row = row
        self.col = col
        self.val = val
        self.T = False
        if mat is not None:
            self.matrix = mat
        else:
            if self.val == 'r':
                self.matrix = [[random.random() for j in range(self.col)] for i in range(self.row)]
            else:
                self.matrix = [[self.val for j in range(self.col)] for i in range(self.row)]

    def transpose(self):
        self.T = not self.T
        temp = self.row
        self.row = self.col
        self.col = temp
        self.matrix = [list(mat) for mat in zip(*self.matrix)]

    def multiply(self, mat):
        if self.shape()[1] != mat.shape()[0]:
            raise ValueError(
                "dim 1 {} != dim 0 {} for matrices shapes {}, {}".format(self.shape()[1], mat.shape()[0], self.shape(),
                                                                         mat.shape()))
        else:
            return [dot(self.matrix[i], mat.matrix[i]) for i in range(self.col)]

    def shape(self):
        return self.col, self.row

    def print(self):
        [print(self.matrix[i]) for i in range(self.row)]
