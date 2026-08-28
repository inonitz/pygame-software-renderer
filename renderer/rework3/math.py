import numpy as np
from numpy import sin, cos, tan
import numba as nb


def normal(vec):
    return vec / np.sqrt(np.sum(vec**2))

def mag(vec):
    return np.sqrt(np.sum(vec**2))

@nb.njit()
def get_identity():
    return np.identity(4)

def get_rotate(x, y, z):
    return np.array([
        [cos(z)*sin(y), cos(z)*sin(y)*sin(x) - sin(z)*cos(x), cos(z)*sin(y)*cos(x) + sin(z)*sin(x), 0],
        [sin(z)*cos(y), sin(z)*sin(y)*sin(x) + cos(z)*cos(x), sin(z)*sin(y)*cos(z) - cos(z)*sin(x), 0],
        [-sin(y),       cos(y)*sin(x),                        cos(y)*cos(x),                        0],
        [0,             0,                                    0,                                    1]
    ])

def get_translate(vec):
    return np.array([
        [1, 0, 0, vec[0]],
        [0, 1, 0, vec[1]],
        [0, 0, 1, vec[2]],
        [0, 0, 0,      1]
    ])

def get_scale_mat(vector):
    return np.array([
        [vector[0], 0, 0, 0],
        [0, vector[1], 0, 0],
        [0, 0, vector[2], 0],
        [0, 0, 0,         1]
    ])


def get_LookAt(eye, at, up=np.array([0, 1, 0])):
    z = normal(eye - at)
    x = normal(np.cross(up, z))
    y = np.cross(z, x)
    return np.matmul(
        np.array([
            np.append(x, 0),
            np.append(y, 0),
            np.append(z, 0),
            np.array([0, 0, 0, 1])
        ]), get_translate(-eye)
    )

def update_EyeLookAt(lookAt_mat, new_eye):
    lookAt_mat[0:3, -1] = new_eye

def get_perspective_projection(near, far, aspect, fov):
    fov *= np.pi/180
    return np.array([
        [1/(aspect*tan(fov/2)), 0, 0, 0],
        [0, 1/tan(fov/2), 0, 0],
        [0, 0, (far+near)/(near-far), 2*far*near/(near-far)],
        [0, 0, -1, 0]
    ])

@nb.njit()
# Expects a flattened list (from numpy arr)
def in_range(list, r0, r1):
    for value in list:
        if value < r0 or value > r1:
            return False


