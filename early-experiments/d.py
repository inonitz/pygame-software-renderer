import numpy as np
import pyglet as pg
from pyglet.window import key, mouse
from numpy import random as rand

win = pg.window.Window(width=600, height=400, resizable=True)
square = (100, 200), (100, 100), (200, 100), (200, 200)


@win.event
def on_draw():
    # for i in range(3):
    #     pg.graphics.draw(2, pg.gl.GL_LINES,
    #                      ('v2i', square[i]+square[i + 1]),
    #                      ('c3B', (255, 255, 255) * 2)
    #                      )
    for i in range(3):
        print(square[i] + square[i + 1])
        pg.graphics.draw(2, pg.gl.GL_LINES,
                         ('v2i', square[i] + square[i + 1]),
                         ('c3B', (255, 255, 255) * 2))
    pg.graphics.draw(2, pg.gl.GL_LINES,
                     ('v2i', square[3] + square[0]),
                     ('c3B', (255, 255, 255) * 2))
    # pg.graphics.draw(4, pg.gl.GL_LINES,
    #                  ('v2i', (250, 50, 250, 250, 50, 250, 50, 50)),
    #                  ('c3B', (255, 255, 255) * 4))


pg.app.run()
