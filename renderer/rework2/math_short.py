import numpy as np


def sin(x):
    return np.sin(x)


def cos(x):
    return np.cos(x)


def tan(x):
    return np.tan(x)


def mag(vector):
    if type(vector) != np.ndarray: vector = np.array(vector)
    return np.sqrt((vector**2).sum())

def norm(vec):
    if type(vec) != np.ndarray: vec = np.array(vec)
    return vec/mag(vec)


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


def get_identity():
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
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


def get_scale_mat(vector):
    return np.array([[vector[0], 0, 0, 0],
                     [0, vector[1], 0, 0],
                     [0, 0, vector[2], 0],
                     [0, 0, 0,         1]])

def get_TRS(scale, trans, angle, axis='y'):
    rot = get_identity()
    if axis == 'y':
        rot = get_rotY(angle)
    elif axis == 'x':
        rot = get_rotX(angle)
    elif axis == 'z':
        rot = get_rotZ(angle)
    return np.matmul(get_translate_mat(trans), np.matmul(rot, get_scale_mat(scale)))

def getProjectionMat(near, far, aspect, fov):
    fov *= np.pi/180
    t = np.tan(fov/2) * near
    r = t*aspect
    l = -r
    b = -t
    return np.array([
        [2*near/(l-r), 0, (r+l)/(r-l), 0],
        [0, 2*near/(t-b), (t+b)/(t-b), 0],
        [0, 0, -(far+near)/(far-near), -(2*far*near)/(far-near)],
        [0, 0, -1, 0]
    ])


def getLookAt(pos, target, up):
    forward = norm(np.subtract(pos, target))
    right = norm(np.cross(up, forward))
    up = np.cross(forward, right)
    forward = np.append(forward, 1)
    right = np.append(right, 1)
    up = np.append(up, 1)

    orientation = np.array([right, up, forward, np.array([0, 0, 0, 1]).T])
    translate = get_translate_mat(-pos)
    return np.matmul(orientation, translate)

#  update matrices\vectors, i cant be bothered to update each ne manually/
def update():
    pass





# def get_model_mat(translate_vec, rot_angle, scale_vec):
#     model_matrix = get_translate_mat(translate_vec) * get_rot_mat(rot_angle) * get_scale_mat(scale_vec)
#     return model_matrix


def normalize(val, min, max):
    if type(val) is not np.ndarray: val = np.array(val)
    val = val.T
    return [(max - min) * ((v - np.min(val)) / (np.max(val) - np.min(val))) - min for v in val]

def norm_singleVal(val, min, max):
    val += 1 # if val is in range [-1, 1], add 1 for range [0, 2]
    val /= 2
    return max - 2*min



def rad(angle):
    return (angle/180) * np.pi

def to_homogeneous(vec):
    if type(vec) != np.ndarray:
        vec = np.array(vec)
    if vec.shape[0] != 4:
        vec = np.append(vec, 1)

    vec = vec.reshape(vec.shape[0], 1)
    return vec
