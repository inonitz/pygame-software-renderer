from failed_attempts.math_short import *


class fps_camera:
    def __init__(self, position, target, up, fov, aspectRatio, near, far):
        if position.shape[0] == 3 or target.shape[0] == 3 or up.shape[0] == 3:
            position = np.append(position, 1)
            target = np.append(target, 1)
            up = np.append(up, 1)

        self.pos = position
        self.target = target
        self.up = up
        self.fov = fov
        self.aspect = aspectRatio
        self.near = near
        self.far = far


        self.model_mat = np.array([])
        self.view_mat = np.array([])
        t = np.tan(self.fov / 360 * np.pi) * self.near
        b = -t
        r = t * self.aspect
        l = b
        x0 = 2 * self.near / (r - l)
        x2 = (r + l) / (r - l)
        y1 = 2 * self.near / (t - b)
        y2 = (t + b) / (t - b)
        z2 = -(self.far + self.near) / (self.far - self.near)
        z3 = -2 * self.far * self.near / (self.far - self.near)

        self.projection_mat = np.array([
            [x0, 0, x2, 0],
            [0, y1, y2, 0],
            [0, 0, z2, z3],
            [0, 0, -1,  0]
        ])

        self.translateVec = np.array([0, 0, 0, 0])
        self.pitch = 0
        self.yaw = 0
        self.roll = 0

    def getViewMatrix(self):
        return self.view_mat

    def getProjectionMatrix(self):
        return self.projection_mat

    def update_view(self):
        mat_rotate = get_rotY(self.yaw)
        mat_rotate = np.matmul(get_rotX(self.pitch), mat_rotate)
        mat_rotate = np.matmul(get_rotZ(self.roll), mat_rotate)
        self.translateVec = get_translate_mat(-self.pos)
        self.view_mat = np.matmul(mat_rotate, -self.translateVec)

    def setRotation_params(self, pitch=0, yaw=0, roll=0):
        self.pitch = pitch
        self.yaw = yaw
        self.roll = roll

    def translate(self, translate_vec):
        self.pos = self.pos + np.array(translate_vec)

    def viewToProjection(self, vec):
        projected = np.matmul(self.projection_mat, vec)
        projected = projected / projected[-1, :]
        projected = projected[:2, :]
        return projected

    def keyPressed(self, key):
        pass

    def mouseMove(self, mouse_pos):
        pass
