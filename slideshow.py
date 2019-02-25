#!/usr/bin/env python
#
#  Copyright (c) 2019, hmisty Evan Liu 
#
#  Dev: https://github.com/hmisty/py-slideshow
#  License: GPLv3


import argparse
import random
import os

import pyglet
from pyglet.window import key

class bidirectional_iterator(object):
    def __init__(self, collection):
        self.collection = collection
        self.index = -1

    def __next__(self):
        if self.index + 1 < len(self.collection):
            self.index += 1
            result = self.collection[self.index]
            return result
        else:
            raise StopIteration

    def prev(self):
        if self.index > 0:
            self.index -= 1
            result = self.collection[self.index]
            return result
        else:
            raise StopIteration

    def __iter__(self):
        return self


def prev_image(dt):
    img = pyglet.image.load(image_paths_iter.prev())
    sprite.image = img
    sprite.scale = scale = get_scale(window, img)
    sprite.x = float(window.width - img.width * sprite.scale)/2
    sprite.y = float(window.height - img.height * sprite.scale)/2
    window.clear()

def next_image(dt):
    img = pyglet.image.load(next(image_paths_iter))
    sprite.image = img
    sprite.scale = scale = get_scale(window, img)
    sprite.x = float(window.width - img.width * sprite.scale)/2
    sprite.y = float(window.height - img.height * sprite.scale)/2
    window.clear()

def get_image_paths(input_dir='.'):
    paths = []
    for root, dirs, files in os.walk(input_dir, topdown=True):
        for file in sorted(files):
            if file.endswith(('jpeg', 'jpg', 'png', 'gif')):
                path = os.path.abspath(os.path.join(root, file))
                paths.append(path)
    return paths

def get_scale(window, image):
    factor = 0.8
    if image.width > image.height:
        scale = float(window.width) / image.width * factor
    else:
        scale = float(window.height) / image.height * factor
    return scale


window = pyglet.window.Window(fullscreen=True)

@window.event
def on_draw():
    sprite.draw()

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.RIGHT or symbol == key.DOWN:
        next_image(0)
    elif symbol == key.LEFT or symbol == key.UP:
        prev_image(0)
    elif symbol == key.Q: # quit
        pyglet.app.exit()
    elif symbol == key.W: # white background
        pyglet.gl.glClearColor(*[255,255,255,0])
        window.clear()
    elif symbol == key.B: # black background
        pyglet.gl.glClearColor(*[0,0,0,0])
        window.clear()

    # otherwise, do nothing

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='directory of images',
                        nargs='?', default=os.getcwd())
    args = parser.parse_args()

    image_paths = get_image_paths(args.dir)
    image_paths_iter = bidirectional_iterator(image_paths)
    img = pyglet.image.load(next(image_paths_iter))
    sprite = pyglet.sprite.Sprite(img)
    sprite.scale = get_scale(window, img)
    sprite.x = float(window.width - img.width * sprite.scale)/2
    sprite.y = float(window.height - img.height * sprite.scale)/2

    pyglet.app.run()
