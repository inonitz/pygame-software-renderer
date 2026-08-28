import numpy as np
import pyglet as pg
from pyglet.window import key, mouse
from numpy import random as rand

win = pg.window.Window(width=600, height=400, resizable=True, style=pg.window.Window.WINDOW_STYLE_DEFAULT,
                       caption='homosex')

# ic1 = pg.image.load('29986_serial_experiments_lain_iwakura_lain.jpg')
# win.set_icon(ic1)
# image = pg.resource.image('29986_serial_experiments_lain_iwakura_lain.jpg')


def normalize(arg, multiplier):
    return tuple(np.multiply(np.array(arg), multiplier))


cube = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0], [1, 0, 1], [0, 1, 1], [1, 1, 1]]
square = normalize((0, 0, 0, 1, 1, 0, 1, 1), 450)
print(square)

# @win.event
# def key_press(symbol, modifiers):
#     if symbol == key.ENTER:
#         draw_obj(cube)


def wob():
    g = rand.randint(0, 2)
    if g == 1:
        return 255, 255, 255
    else:
        return 0, 0, 0


@win.event
def on_draw():
    # pg.graphics.draw(4, pg.gl.GL_POINTS,
    #                  ('v2i', square),
    #                  ('c3B', (255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0)))
    for i in range(int(win.width/4)):
        for j in range(int(win.height)):
            pg.graphics.draw(1, pg.gl.GL_POINTS,
                                ('v2i', (i, j)),
                                ('c3B', (wob()))
                                )


pg.app.run()
