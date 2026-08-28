from failed_attempts.window import *
from second_attempt.camera import *
import numpy as np
import pygame

pygame.init()

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
# print(vertices[cube_indices[0]][:, :2] * .5)
# win.push_event(win.draw_triangle((vertices[cube_indices[0]][:, :2] * 0.5).tolist(), (255, 255, 255), fill=False))
# win.push_event(win.update())
def create_triangles(obj_vertices, obj_indices):
    triangle_array = []
    for tri_indices in obj_indices:
        tri = [obj_vertices[tri_indices[0]],
               obj_vertices[tri_indices[1]],
               obj_vertices[tri_indices[2]]]
        triangle_array.append(tri)
    return triangle_array


def scale_tensor(tris, factor_vec):
    scaler = get_scale_mat(factor_vec)
    ret = []
    for i in range(tris.shape[0]):
        temp = [np.matmul(scaler, np.array(vertex).reshape(4, 1)) for vertex in tris[i]]
        ret.append(temp)
    return np.array(ret)


camera.lookAt(position=np.array([0, 0, -5]), target=np.array([0, 0, 0]))
angle = 10
col = (255, 255, 255)
triangles = scale_tensor(np.array(create_triangles(vertices, cube_indices)), [.5, .5, .5])
# tris_viewed = np.array([camera.world_to_view(tris) for tris in triangles])
tris_projected = np.array([camera.view_to_projection(tris) for tris in triangles])
# tris_projected = np.array([tris / tris[:, :, -1] for tris in tris_projected])
# tris_projected = tris_projected[:, :, :, :2]
i = 0
while i < 1:
    for triangle in tris_projected:
        # if i % 10 == 0:
        #     win.push_event(win.clear())
        triangle[0] = np.matmul(get_rotY(angle), triangle[0])
        triangle[1] = np.matmul(get_rotY(angle), triangle[1])
        triangle[2] = np.matmul(get_rotY(angle), triangle[2])


        triangle = np.array([vertex / vertex[-1] for vertex in triangle])
        triangle = triangle[:, :2] * 0.1
        win.push_event(win.draw_triangle(triangle, col, fill=False))
        win.push_event(win.update())
        i += 1
    # win.push_event(win.clear())


color = np.random.randint(0, 255, (1, 3))
color = color.tolist()[0]
win.start_program()
