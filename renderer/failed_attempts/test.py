import numpy as np


def make_translate_mat(vector):
    return np.array([[1, 0, 0, vector[0]],
                     [0, 1, 0, vector[1]],
                     [0, 0, 1, vector[2]],
                     [0, 0, 0, 1]])


def make_rot_mat(angle):
    if 10 <= angle <= 360:
        angle *= np.pi/180
    return np.array([[np.cos(angle), -np.sin(angle), 0, 0],
                     [np.sin(angle), np.cos(angle), 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]])


def make_scale_mat(vector):
    return np.array([
        [vector[0], 0, 0, 0],
        [0, vector[1], 0, 0],
        [0, 0, vector[2], 0],
        [0, 0, 0,        1]]
    )


def make_model_mat(translate_vec, rot_angle, scale_vec):
    model_matrix = make_translate_mat(translate_vec) * make_rot_mat(rot_angle) * make_scale_mat(scale_vec)
    return model_matrix


def translate(vector, translate_vec):
    if vector.shape[1] != 4 and vector.shape[0] != vector.shape[1]:
        vector = np.array([vector[0], vector[1], vector[2], 1])

    mat_translate = make_translate_mat(translate_vec)
    return mat_translate * vector


def rotate(vector, angle, return_mat=False):
    angle *= np.pi / 180
    mat_rotate = make_rot_mat(angle)
    if return_mat:
        return mat_rotate

    if vector.shape[1] != 4 and vector.shape[0] != vector.shape[1]:
        vector = np.array([vector[0], vector[1], vector[2], 1])
    return mat_rotate * vector


def scale(vector, scale_vector, return_mat=False):
    mat_scale = make_scale_mat(scale_vector)

    if vector.shape[1] != 4 and vector.shape[0] != vector.shape[1]:
        vector = np.array([vector[0], vector[1], vector[2], 1])
    return mat_scale * vector


def model_mat(vector=np.array([]), translate_vec=np.array([]), rot_angle=90, scale_vec=np.array([])):
    model_matrix = make_model_mat(translate_vec, rot_angle, scale_vec)
    return model_matrix * vector


class camera:
    def __init__(self, pos, aspect_ratio, fov=60, near=1.0, far=100.0):
        self.pos = pos
        self.fov = fov
        self.near_plane = near
        self.far_plane = far
        self.ar = aspect_ratio

        a = 0.5 * np.tan(np.deg2rad(self.fov / 2))
        b = a * 1 / self.ar
        c = -(self.near_plane + self.far_plane) / (self.near_plane - self.far_plane)
        d = (2 * self.far_plane * self.near_plane) / (self.near_plane - self.far_plane)
        self.transform_matrix = np.array([[b, 0, 0, 0],
                                          [0, a, 0, 0],
                                          [0, 0, c, d],
                                          [0, 0, 1, 0]])

    def lookAt(self, target, upVector=np.array([0, 1, 0])):
        pass

    def project_perspective(self, vector):
        if vector.shape[1] != 4:
            if vector.shape[1] == 3:
                vector = np.array([vector[0], vector[1], vector[2], 1])
            else:
                raise TypeError(
                    "Vector must be column major && of shape ==> [1, 3] OR [1, 4]"
                )
        return self.transform_matrix * vector

    def proj_to_device(self, vector):
        return
