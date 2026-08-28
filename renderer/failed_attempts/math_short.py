import numpy as np


def sin(x):
    return np.sin(x)


def cos(x):
    return np.cos(x)


def tan(x):
    return np.tan(x)


def mag(vector):
    if type(vector) != np.ndarray: vector = np.array(vector)
    return np.sqrt(vector.dot(vector))


def get_rotX(angle):
    angle *= np.pi / 180
    return np.array([
        [1, 0,           0,           0],
        [0, cos(angle), -sin(angle),  0],
        [0, sin(angle),  cos(angle),  0],
        [0, 0,           0,           1]
    ])


def get_rotY(angle):
    angle *= np.pi / 180
    return np.array([
        [cos(angle),  0, sin(angle), 0],
        [0,           1, 0,          0],
        [-sin(angle), 0, cos(angle), 0],
        [0,           0, 0,          1]
    ])


def get_rotZ(angle):
    angle *= np.pi / 180
    return np.array([
        [cos(angle), -sin(angle), 0, 0],
        [sin(angle),  cos(angle), 0, 0],
        [0,           0,          1, 0],
        [0,           0,          0, 1]
    ])


def rotate(angle, axis_vector):
    angle *= np.pi / 180
    u, v, w = axis_vector[0], axis_vector[1], axis_vector[2]
    return np.array([
        [u ** 2 + (1 - u ** 2) * np.cos(angle), u * v * (1 - np.cos(angle)) - w * np.sin(angle),
         u * w * (1 - np.cos(angle)) + v * np.sin(angle), 0],
        [u * v * (1 - np.cos(angle)) + w * np.sin(angle), v ** 2 + (1 - v ** 2) * np.cos(angle),
         v * w * (1 - np.cos(angle)) - u * np.sin(angle), 0],
        [u * w * (1 - np.cos(angle)) - v * np.sin(angle), v * w * (1 - np.cos(angle)) + u * np.sin(angle),
         w ** 2 + (1 - w ** 2) * np.cos(angle), 0],
        [0, 0, 0, 1]
    ])


def get_translate_mat(vector):
    return np.array([[1, 0, 0, vector[0]],
                     [0, 1, 0, vector[1]],
                     [0, 0, 1, vector[2]],
                     [0, 0, 0, 1]])


def get_rot_mat(angle):
    if 10 <= angle <= 360:
        angle *= np.pi / 180
    return np.array([[np.cos(angle), -np.sin(angle), 0, 0],
                     [np.sin(angle), np.cos(angle), 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]])


def get_scale_mat(vector):
    return np.array([[vector[0], 0, 0, 0],
                     [0, vector[1], 0, 0],
                     [0, 0, vector[2], 0],
                     [0, 0, 0, 1]])


def get_model_mat(translate_vec, rot_angle, scale_vec):
    model_matrix = get_translate_mat(translate_vec) * get_rot_mat(rot_angle) * get_scale_mat(scale_vec)
    return model_matrix
