from rework2.math_short import *


class Camera:
    def __init__(self, position, target, up, fov, aspect_ratio, near, far):
        self.camera_position = np.array(position)
        self.view_angle = fov
        self.aspect_ratio = aspect_ratio
        self.n = near
        self.f = far

        self.direction_vec = norm(np.subtract(position, target))
        self.right_vec = norm(np.cross(up, self.direction_vec))
        self.up_vec = np.cross(self.direction_vec, self.right_vec)
        self.forward_vec = np.array([0, 0, -1])

        self.camera_speed = 1
        self.pitch = 90
        self.yaw = -90

        self.matrix_dict = {"rotation_mat": get_rotY(self.view_angle) * get_rotX(self.view_angle),
                            "translation_mat": get_identity(),
                            "scale_mat": get_identity(),
                            "localToWorld": get_identity(),
                            "view_mat": np.ndarray,
                            "projection": getProjectionMat(self.n, self.f, self.aspect_ratio, self.view_angle)
                            }
        self.matrix_dict["localToWorld"] = np.matmul(self.matrix_dict["translation_mat"],
                                                     np.matmul(self.matrix_dict["rotation_mat"],
                                                               self.matrix_dict["scale_mat"]))
        self.updateView()

    def updateView(self):
        lookAt = getLookAt(self.camera_position, self.camera_position + self.forward_vec, self.up_vec)
        self.matrix_dict["view_mat"] = lookAt

    def updateProjection(self):
        self.matrix_dict["projection"] = getProjectionMat(self.n, self.f, self.aspect_ratio, self.view_angle)

    def modelToView(self, vec):
        return np.matmul(self.matrix_dict["view_mat"], vec)

    # Only works with tensors of shape (3, 4, 1), meaning you cant pass a singular vector (4, 1) as argument.
    def viewToProjection(self, vec):
        projected = np.matmul(self.matrix_dict["projection"], vec)
        projected = np.array([vert[:2] / vert[-1] for vert in projected])
        return projected

    def MVP(self, vec):
        # PVMv = np.matmul(self.matrix_dict["localToWorld"], vec)
        PVMv = self.modelToView(vec)
        PVMv = self.viewToProjection(PVMv)
        return PVMv


    def update_angles(self, mouse_pos0, mouse_pos1, sens):
        if len(mouse_pos0) != 2 or len(mouse_pos1) != 2:
            raise AttributeError("mouse_pos must be a list with length 2!,"
                                 "position of mouse in the window")
        else:
            self.yaw += sens * (mouse_pos1[0] - mouse_pos0[0])
            self.pitch += sens * (mouse_pos1[1] - mouse_pos0[1])
        if self.pitch >= 89.9:
            self.pitch = 89.9
        elif self.pitch <= -89.9:
            self.pitch = -89.9

        if self.yaw > 89.9:
            self.yaw = 89.9
        elif self.yaw < -89.9:
            self.yaw = -89.9


    def update_direction_vec(self):
        self.forward_vec = np.array([
            cos(self.yaw) * cos(self.pitch),
            sin(self.pitch),
            sin(self.yaw) * cos(self.pitch)
        ])
        self.forward_vec = norm(self.forward_vec)
        self.updateView()

    def getViewMatrix(self):
        return self.matrix_dict["view_mat"]

    def setSpeed(self, val):
        self.camera_speed = val

    def debug_info(self):
        print('position {}\ndirection {} \nyaw: {} pitch: {}'.format(self.camera_position.tolist(), self.forward_vec, self.yaw,
                                                                     self.pitch))
