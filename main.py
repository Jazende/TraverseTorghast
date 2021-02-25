import pyglet
from pyglet.gl import *

from game import Game

class Screen(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        glClearColor(1, 1, 1, 1)
        pyglet.clock.schedule_interval(self.update, 1.0 / 60)
        
        self.game = Game()

    def update(self, dt):
        self.game.update(dt)

    def on_draw(self):
        self.clear()
        self.set_2d()
        self.game.on_draw()

    def set_2d(self):
        width, height = self.get_size()
        glDisable(GL_DEPTH_TEST)
        viewport = self.get_viewport_size()
        glViewport(0, 0, max(1, viewport[0]), max(1, viewport[1]))
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, max(1, width), 0, max(1, height), -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def on_mouse_motion(self, mouse_x, mouse_y, delta_x, delta_y):
        self.game.on_mouse_motion(mouse_x, mouse_y, delta_x, delta_y)

    def on_mouse_drag(self, mouse_x, mouse_y, delta_x, delta_y, button, modifiers):
        self.game.on_mouse_drag(mouse_x, mouse_y, delta_x, delta_y, button, modifiers)

    def on_mouse_press(self, mouse_x, mouse_y, button, modifiers):
        self.game.on_mouse_press(mouse_x, mouse_y, button, modifiers)

    def on_mouse_release(self, mouse_x, mouse_y, button, modifiers):
        self.game.on_mouse_release(mouse_x, mouse_y, button, modifiers)

def main():
    screen = Screen(width=800, height=640)
    pyglet.app.run()

if __name__ == '__main__':
    main()
