from rework.draw_lib import *
from rework.window import *
from rework.camera import *
import numpy as np
import pygame

pygame.init()

vertices = np.array([
    [-1, -1, 1, 1],
    [1, -1, 1, 1],
    [1, 1, 1, 1],
    [-1, 1, 1, 1],
    [-1, -1, -1, 1],
    [1, -1, -1, 1],
    [1, 1, -1, 1],
    [-1, 1, -1, 1]
])

cube_indices = np.array([
    [3, 2, 0],
    [0, 2, 1],
    [2, 6, 1],
    [1, 6, 5],
    [6, 7, 5],
    [5, 7, 4],
    [7, 3, 4],
    [4, 3, 0],
    [3, 7, 6],
    [3, 6, 2],
    [0, 4, 5],
    [0, 5, 1],
])


def translate_camera(event, speed):
    movement_checker = {"100": False, "97": False, "119": False, "115": False}
    translation_list = np.array([[1, 0, 0, 0], [-1, 0, 0, 0], [0, 0, -1, 0], [0, 0, 1, 0]]) * speed
    if event.type == pygame.KEYDOWN:
        movement_checker[str(event.key)] = True
    elif event.type == pygame.KEYUP:
        movement_checker[str(event.key)] = False
    i = 0
    for val in movement_checker.values():
        if val:
            return translation_list[i]
        i += 1
    return None


def create_triangles(obj_vertices, obj_indices):
    triangle_array = []
    for tri_indices in obj_indices:
        tri = [np.array(obj_vertices[tri_indices[0]]).reshape(4, 1),
               np.array(obj_vertices[tri_indices[1]]).reshape(4, 1),
               np.array(obj_vertices[tri_indices[2]]).reshape(4, 1)]
        triangle_array.append(tri)
    return np.array(triangle_array)


window_width = 720
window_height = 720
AspectR = window_width / window_height

camera_pos = np.array([0, 0, 1])
camera_target = np.array([0, 0, 0])
camera_front = np.array([0, 0, -1])
camera_up = np.array([0, 1, 0])
fieldOfView = 110
near = 10
far = 1000

win = Window(window_width, window_height, -1, 1)
win.setMousePos(window_width/2, window_height/2)
clock = pygame.time.Clock()
clock.tick(100)


class win_main(Window):
    def start_program(self):
        painter = draw_lib(win)
        camera = fps_camera(camera_pos, camera_target, camera_up, fieldOfView, AspectR, near, far)
        camera.translate([0, 0, 10, 0])
        camera.update_view()

        view_mat = camera.getViewMatrix()
        proj_mat = camera.getProjectionMatrix()
        triangles = create_triangles(vertices, cube_indices)
        move_cameraVector = []
        col = (255, 255, 255, 200)
        fps_counter = 0
        rotation_val = 10
        speed_const = .1
        mpos = [0, 0]
        mpos_last = []

        self.running = True
        while self.running:
            mpos_last = self.getMousePos()
            self.update()
            self.clear()
            fps_counter += 1
            # if fps_counter % 100 == 0:
            #     col = np.random.randint(0, 255, (4,)).tolist()
            for event in pygame.event.get():
                move_cameraVector = translate_camera(event, speed_const)
                camera.rot_pos(self.mouse_sens, mpos, mpos_last)
                camera.update_view()
                if event.type == pygame.QUIT:
                    self.running = False

            for triangle in triangles:
                tri = np.matmul(get_rotY(rotation_val), triangle)
                tri = np.matmul(get_rotX(rotation_val), tri)
                tri_viewed = np.matmul(view_mat, tri)
                tri_projected = np.matmul(proj_mat, tri_viewed)


                tri_projected = np.array([np.array(tri[:2] / tri[-1]).reshape(2, ) for tri in tri_projected])
                # painter.draw_triangle(tri_projected.tolist(), (255, 255, 255), fill=True)
                painter.draw_poly_pygame(win.screen, col, tri_projected.tolist())

            rotation_val += .1
            if move_cameraVector is not None:
                camera.translate(move_cameraVector)

            # camera.setRotation_params(pitch, yaw, 0)
            camera.update_view()
            view_mat = camera.getViewMatrix()
            mpos = self.getMousePos()


main = win_main(win.width, win.height, win.a, win.b)
main.start_program()
