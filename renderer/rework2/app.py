from rework2.camera import *
from rework2.window import *
pygame.font.init()

class application:
    def __init__(self, win_width, win_height):
        self.window = Window(win_width, win_height)
        self.camera = Camera

        pygame.mouse.set_pos(win_width/2, win_height/2)
        self.mouse_sen = 1/100

        self.running = False


    def setCamera(self, obj_camera):
        if type(obj_camera) == Camera:
            self.camera = obj_camera
        else:
            raise TypeError("obj_camera argument must be a Camera Object!")

    def setWindow(self, win):
        if type(win) == Window:
            self.window = win
        else:
            raise TypeError("win argument must be a Window Object!")

    def onUserUpdate(self):
        self.window.update()
        self.window.clear()

    def start(self):
        self.running = True
        self.onUserUpdate()

    def render_debug(self):
        font = pygame.font.SysFont("Comic Sans MS", 20)
        surf = font.render("Position: {}, direction: {}".format(self.camera.camera_position, self.camera.forward_vec), False, (255, 255, 255), self.window.col_clear)
        self.window.window.blit(surf, (0, 0))

    @staticmethod
    def get_mouse_pos():
        return pygame.mouse.get_pos()

    def setMouseSensitivity(self, val):
        self.mouse_sen = val

    # noinspection PyArgumentList
    def get_keyboard_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.camera.camera_position = self.camera.camera_position - self.camera.camera_speed * self.camera.forward_vec
            elif event.key == pygame.K_s:
                self.camera.camera_position = self.camera.camera_position + self.camera.camera_speed * self.camera.forward_vec
            elif event.key == pygame.K_d:
                self.camera.camera_position = self.camera.camera_position + self.camera.camera_speed * norm(np.cross(self.camera.forward_vec, self.camera.up_vec))
            elif event.key == pygame.K_a:
                self.camera.camera_position = self.camera.camera_position - self.camera.camera_speed * norm(np.cross(self.camera.forward_vec, self.camera.up_vec))
            elif event.key == pygame.K_z:
                self.camera.view_angle += 10
            elif event.key == pygame.K_c:
                self.camera.view_angle -= 10

        if self.camera.view_angle <= 20:
            self.camera.view_angle = 20

        self.camera.updateProjection()
        self.camera.updateView()
        # self.window.update()

