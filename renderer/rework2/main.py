from rework2.app import *
from rework2.camera import *
from rework2.window import *
from rework2.parseFile import *

class app(application):

    def onUserUpdate(self):
        self.window.setFill((100, 100, 100))
        self.camera.setSpeed(1)
        self.camera.update_direction_vec()
        self.camera.updateProjection()
        local_to_world0 = get_TRS([0.2, 0.2, 0.2], [0, -2, -2], 0, axis='y')
        local_to_world1 = get_TRS([1.5, 1.5, 1.5], [5, 0, 2], 45, axis='y')

        while self.running:
            last_pos = self.get_mouse_pos()
            self.render_debug()
            self.window.update()
            self.window.clear()

            #  Rendering pipeline
            for triangle in tris:
                tri_world = np.matmul(local_to_world0, triangle)
                tri_MVP = self.camera.MVP(tri_world).reshape(3, 2).tolist()
                tri_screen = self.window.normToScreen(tri_MVP)
                self.window.draw_triangle(tri_screen, fill=False)


            for triangle in tris2:
                tri_world = np.matmul(local_to_world1, triangle)
                tri_MVP = self.camera.MVP(tri_world).reshape(3, 2).tolist()
                tri_screen = self.window.normToScreen(tri_MVP)
                self.window.draw_triangle(tri_screen, fill=False)

            # Draw Origin Vectors (RGB)!
            axis_mvp = self.camera.MVP(Axis).reshape(3, 2).tolist()
            axis_xyz_screen = self.window.normToScreen(axis_mvp)
            origin = self.camera.MVP(np.array([np.array([0, 0, 0, 1]).reshape(4, 1), np.ones((4, 1)), np.ones((4, 1))]))
            origin_norm = self.window.normToScreenVec(origin[0].tolist())
            print(origin_norm, axis_xyz_screen)
            [pygame.draw.line(self.window.window, col_xyz[i], axis_xyz_screen[i], origin_norm, 5) for i in range(3)]

            for event in pygame.event.get():
                self.get_keyboard_input(event)
                if event.type == pygame.QUIT:
                    self.running = False

            mouse_pos = self.get_mouse_pos()
            self.camera.update_angles(mouse_pos, last_pos, self.mouse_sen)
            self.camera.update_direction_vec()
            print(self.camera.up_vec)
            # self.camera.debug_info()




width, height = 800, 600
fov = 60
near, far = 10, 1000
pos, target, up = [0, 0, 3], [0, 0, -1], [0, 1, 0]

cam = Camera(pos, target, up, fov, width/height, near, far)

file = open("rework2/mesh_objects/teapot.obj", "r")
info = file.readlines()
vertices = getVertexArray(info)
indices = getIndexArray(info)
tris = createTriangles(vertices, indices)
file.close()

file = open("rework2/mesh_objects/cow.obj", "r")
info = file.readlines()
vertices = getVertexArray(info)
indices = getIndexArray(info)
tris2 = createTriangles(vertices, indices)
file.close()

# Making axis' vectors for drawing the origin vectors
Axis = [np.array([1, 0, 0, 1]), np.array([0, 1, 0, 1]), np.array([0, 0, -1, 1])]
Axis = [a.reshape(4, 1) for a in Axis]

col_xyz = [[255, 0, 0], [0, 255, 0], [0, 0, 255]]


a = app(int(1.5*width), int(1.5*height))
a.setCamera(cam)
print(a.camera.matrix_dict)

print("triangles: {}".format(tris.shape))
a.start()
