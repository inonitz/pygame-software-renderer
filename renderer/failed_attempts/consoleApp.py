from failed_attempts.camera import *
from failed_attempts.window import *
import numpy as np
pygame.init()


vertices = np.array([
        [-1, -1, 1,  1],
        [1, -1, 1,   1],
        [1, 1, 1,    1],
        [-1, 1, 1,   1],
        [-1, -1, -1, 1],
        [1, -1, -1,  1],
        [1, 1, -1,   1],
        [-1, 1, -1,  1]
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
fov = 65
near = 10
far = 1000

win = Window(window_width, window_height, -1, 1)
camera = fps_camera(camera_pos, camera_target, camera_up, fov, AspectR, near, far)
camera.translate([0, 0, 5, 1])
# camera.setRotation_params(30, 30, 0)
camera.update_view()
view_mat = camera.getViewMatrix()
proj_mat = camera.getProjectionMatrix()

triangles = create_triangles(vertices, cube_indices)

yaw = 0
pitch = 0
i = 0
while i < 20:
    pos0 = win.getMousePos()
    win.push_event(win.clear())
    for triangle in triangles:
        tri = np.matmul(get_rotY(yaw), triangle)
        tri_viewed = np.matmul(view_mat, tri)
        tri_projected = np.matmul(proj_mat, tri_viewed)

        tri_projected = np.array([np.array(tri[:2] / tri[-1]).reshape(2,) for tri in tri_projected])
        # print(tri_projected)
        win.draw(win.draw_triangle(tri_projected.tolist(), (255, 255, 255), fill=True))
        win.draw(win.update())

    pos1 = win.getMousePos()
    dx = pos1[0] - pos0[0]
    dy = pos1[1] - pos0[1]
    if dx > 0:
        pitch += win.mouse_sens * dx
    if dy > 0:
        yaw += win.mouse_sens * dy
    # camera.setRotation_params(pitch, yaw, 0)
    camera.translate([0, 0, 0.01, 0])
    camera.update_view()
    view_mat = camera.getViewMatrix()
    i += 0.2
    # yaw += 10
    # pitch += 1

win.start_program()
