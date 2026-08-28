from failed_attempts.math_short import *
import pygame
pygame.init()

""" 
    Note: Must use Column-Major Vectors for multiplication, else nothing will work.
    I'm not doing any error checking, and will not create my own class for that,
    because numpy has too many features for me to create a class for them.

    Remember: v' = M*v [Column Major] else v' = v*M [Row Major]
    So ==> Use v' = M*v for multiplications!

    Transformations that happen: 
    Object coords --> world coords --> Camera coords --> Project Coords --> Device coords [Screen pixels]
    v' = P*V*M*v [Model, View, Projection matrices]

    Vertex_World = M * Vertex_LocalWorld, where M is a linear transformation matrix
    [M == local-to-world]
"""

class fps_camera:
    def __init__(self, eye_pos, target, upVec, fov, aspect_ratio, near, far):
        if eye_pos is None:
            eye_pos = np.array([0, 0, -1, 1])
        if target is None:
            target = np.array([0, 0, 0, 1])
        if upVec is None:
            upVec = np.array([0, 1, 0, 1])

        self.pos = eye_pos
        self.view_angle = fov
        self.aspect_ratio = aspect_ratio
        self.near = near
        self.far = far

        # ============================================================
        # View Transform
        self.cameraForward = (eye_pos - target) / mag(eye_pos - target)
        self.cameraRight = np.cross(upVec, self.cameraForward)
        self.cameraRight /= mag(self.cameraRight)
        self.cameraUp = np.cross(self.cameraForward, self.cameraRight)
        # View Matrix, lookAt
        self.lookAtMat = np.array([
            np.append(self.cameraRight,   self.pos[0]),
            np.append(self.cameraUp,      self.pos[1]),
            np.append(self.cameraForward, self.pos[2]),
            [0,        0,        0,                  1]
        ])
        self.lookAtMat *= get_translate_mat(eye_pos)


        self.WorldToViewMat = np.linalg.inv(self.lookAtMat)
        print(self.WorldToViewMat)
        # ============================================================


        # ============================================================
        # Projection matrix
        #  Takes care of projection matrix [Right handed Coordinate system, openGL implementation]
        top = self.near * np.tan(0.5 * self.view_angle * np.pi / 180)
        bottom = -top

        right = top * self.aspect_ratio
        left = -right

        x0, x2 = 2 * self.near / (right - left), (right + left) / (right - left)
        y1, y2 = 2 * self.near / (top - bottom), (top + bottom) / (top - bottom)
        z2, z3 = -(self.far + self.near) / (self.far - self.near), -2 * self.far * self.near / (self.far - self.near)
        self.viewToProjection_mat = np.array([
            [x0, 0, x2, 0],
            [0, y1, y2, 0],
            [0, 0, z2, z3],
            [0, 0, -1,  0]
        ])
        # ============================================================



        # x, y, z :: -90 < pitch < 90 ; 0 < yaw < 360
        self.pitch = 0
        self.yaw = 0
        self.roll = 0

    def setRotAngles(self, pitch, yaw, roll):
        if pitch is not None:
            self.pitch = pitch
        if yaw is not None:
            self.yaw = yaw
        if roll is not None:
            self.roll = roll


    def updateView(self, cameraPosition, forward, right, up):
        self.cameraForward = forward
        self.cameraRight = right
        self.cameraUp = up
        self.lookAtMat = np.array([
            np.append(self.cameraRight,   cameraPosition[0]),
            np.append(self.cameraUp,      cameraPosition[1]),
            np.append(self.cameraForward, cameraPosition[2]),
                     [0, 0, 0,                            1]
        ])
        self.lookAtMat *= get_translate_mat(cameraPosition)

    def lookAt(self, position=np.array([0, 0, -1]), target=np.array([0, 0, 0]), up=np.array([0, 1, 0])):
        dir = position - target
        dir = dir / mag(dir)
        right = np.cross(up, dir)
        right = right / mag(right)
        upVec = np.cross(dir, right)
        print(dir, right, upVec)
        self.updateView(position, dir, right, upVec)


    def world_to_view(self, vec):
        return np.matmul(self.WorldToViewMat, vec)

    def view_to_projection(self, vec):
        projected = np.matmul(self.viewToProjection_mat, vec)
        return projected
