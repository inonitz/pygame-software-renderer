from rework3.camera import *
from rework3.gui import *
import time


class app:
    def __init__(self, w_width, w_height):
        self.gui = gui(w_width, w_height)
        self.running = bool
        self.pause = False

    def set_camera(self, cam):
        self.gui.camera = cam

    # def callback(self, key, dt):
    #     self.gui.camera.key_callback(key, dt)
    #     self.gui.camera.mouse_callback(pygame.mouse.get_pos())
    #     self.gui.camera.update_view()

    def onUserUpdate(self):
        # Variables here
        c = 1

        while self.running:
            self.gui.update()
            self.gui.clear()

            # Rendering Pipeline


            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause = bool(c)
                        c += 1
                        c %= 2
                    else:
                        self.gui.camera.key_callback(event, time.time())

                elif event.type == pygame.MOUSEMOTION:
                    self.gui.camera.mouse_callback(mouse_pos=pygame.mouse.get_pos())
                self.gui.camera.update_view()

                if event.type == pygame.QUIT:
                    self.running = False

            if self.pause:
                self.gui.clear()
                self.gui.show_text((self.gui.win_dim/2 - 40).flatten().tolist(), "Paused", "Consolas", 30, (255, 255, 255))
            else:
                self.gui.clear()

    def start(self):
        self.running = True
        self.onUserUpdate()
