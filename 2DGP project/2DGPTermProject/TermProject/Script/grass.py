from pico2d import *
import main_state
import game_world
import game_framework

class Grass:



    image = None

    imageW = 802
    imageH = 62

    def __init__(self):

        self.kind = game_world.Feature


        self.collisionRelation = [game_world.Monster,game_world.Player]



        self.x, self.y = main_state.screenX // 2, 0


        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = None
        self.imageState = None


        self.image = load_image('good.png')

        self.boundingBoxOn = True

        self.curState = game_framework.stack[-1]

    def update(self):
        pass

    def draw(self):
        self.image.draw(1200- self.curState.GetBackground().windowLeft, 30- self.curState.GetBackground().windowBottom)
        self.image.draw(400- self.curState.GetBackground().windowLeft, 30- self.curState.GetBackground().windowBottom)


        if(self.boundingBoxOn):
            self.draw_bb()

    def get_bb(self):

        return self.x - 800, self.y, self.x + 940, self.y + self.image.h - 10
    # fill here

    def draw_bb(self):
        left,bottom,right,top = self.get_bb()

        left -= self.curState.GetBackground().windowLeft
        bottom -= self.curState.GetBackground().windowBottom
        right -= self.curState.GetBackground().windowLeft
        top -= self.curState.GetBackground().windowBottom


        draw_rectangle(left,bottom,right,top)
