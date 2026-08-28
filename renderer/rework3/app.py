from rework3.application import *
from rework3.parseobj import *
from rework2.parseFile import *


class app_main(app):
    def onUserUpdate(self):
        # Variables here
        c = 0
        pygame.mouse.set_pos(width/2, height/2)
        self.gui.camera.update_view()
        scale = get_scale_mat([0.2, 0.2, 0.2])

        while self.running:
            self.gui.render_debug()
            self.gui.update()
            self.gui.clear()

            # Rendering Pipeline
            if not self.pause:
                for triangle in primitives:
                    tri_world = np.matmul(scale, triangle)
                    tri_MVP = self.gui.camera.MVP(tri_world)
                    if tri_MVP is not None:
                        tri_screen = self.gui.toScreenCoords(tri_MVP)
                        self.gui.renderer.render(tri_screen, (255, 255, 255))

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: c += 1
                    else: self.gui.camera.key_callback(event.key)
                    c %= 2
                    self.pause = bool(c)

                elif event.type == pygame.MOUSEMOTION:
                    self.gui.camera.mouse_callback(mouse_pos=pygame.mouse.get_pos())
                self.gui.camera.update_view()
                if event.type == pygame.QUIT:
                    self.running = False


            if self.pause:
                self.gui.clear()
                self.gui.show_text((self.gui.win_dim/2 - 40).flatten().tolist(), "Paused", "Consolas", 30, (255, 255, 255))




file = open(create_Filtered_file("mesh_objects/teapot_filtered.obj"), "r")
info = file.readlines()
primitives = create_primitive_array(get_vertices(info), get_indices(info))


vertices = getVertexArray(info)
indices = getIndexArray(info)
tris = createTriangles(vertices, indices)
file.close()


width, height = 800, 600
camera_pos = np.array([0, 0, 3])
camera_target = np.array([0, 0, -1])
near, far, fov = 10, 1000, 60
mouse_sens = 0.01

cam = Camera([width, height], width/height, fov, near, far, eye=camera_pos, at=camera_target)
cam.sensitivity = mouse_sens
Application = app_main(width, height)
Application.set_camera(cam)


Application.start()
