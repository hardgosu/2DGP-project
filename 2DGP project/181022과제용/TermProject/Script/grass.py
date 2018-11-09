from pico2d import *
import main_state
import game_world

class Grass:



    image = None

    imageW = 802
    imageH = 62

    def __init__(self):

        self.kind = game_world.Feature






        self.x, self.y = main_state.screenX // 2, 0


        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = None
        self.imageState = None


        self.image = load_image('good.png')

        self.boundingBoxOn = False

    def update(self):
        pass

    def draw(self):
        self.image.draw(1200, 30)
        self.image.draw(400, 30)


        if(self.boundingBoxOn):
            self.draw_bb()

    def get_bb(self):
        return self.x - 800, self.y, self.x + 800, self.y + self.image.h - 15
    # fill here

    def draw_bb(self):
        draw_rectangle(*self.get_bb())
