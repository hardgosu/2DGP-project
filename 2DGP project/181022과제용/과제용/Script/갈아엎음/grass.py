import random

from pico2d import *
import objectBase

class Grass:
    def __init__(self):

        self.x, self.y = 400, 30
        self.image = load_image('grass.png')

    def draw(self):

        self.image.draw(self.x,self.y)


    def get_bb(self):
        return self.x - 400, self.y - 30, self.x + 400, self.y + 20

    def draw_bb(self):
        draw_rectangle(*self.get_bb())


    # fill here
    def collide(self , b):
        left_a, bottom_a, right_a, top_a = self.get_bb()
        left_b, bottom_b, right_b, top_b = b.get_bb()

        if left_a > right_b:
            return False
        if right_a < left_b:
            return False
        if top_a < bottom_b:
            return False
        if bottom_a > top_b:
            return False
        return True
    def update(self):



        pass

