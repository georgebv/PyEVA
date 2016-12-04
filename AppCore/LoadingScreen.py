import pyglet
from win32api import GetSystemMetrics
import time

animation = pyglet.image.load_animation(r'loading.gif')
sprite = pyglet.sprite.Sprite(animation)
win = pyglet.window.Window(
    width=sprite.width,
    height=sprite.height
)
win.set_location(
    int(GetSystemMetrics(0) / 2 - 400 / 2),
    int(GetSystemMetrics(1) / 2 - 300 / 2)
)
win.set_caption('Processing...')

@win.event
def on_draw():
    win.clear()
    sprite.draw()

pyglet.app.event_loop.run()
print('Here?')

