from pico2d import *
import game_framework
import game_world

class ObjectBase:

    actions = 1
    idle = range(actions)

    #test = {"ImageFile" : None,"IntervalX" : None,"IntervalY" : None,"Frames" : None}

    Images = []


    for i in range(actions):
        Images.append({"ImageFile": None, "IntervalX": None, "IntervalY": None, "Frames": None, "XRevision": None})



    def __init__(self):
        self.kind = None
        self.x, self.y = 0,0
        self.dir = 1

        self.frame = 0
        self.imageState = ObjectBase.idle

        self.collisionRelation = [game_world.EnemyProjectile,game_world.Feature]

        self.selfGravity = False

        self.velocity = 0
        self.velocityY = 0


        self.boundingBoxOn = True


        self.tempGravity = 3

        self.subject = None
        self.hPMax = 1
        self.curHP = 1
        self.damage = 0



        self.deathAnimation = {"ImageFile" : None,"IntervalX" : None,"IntervalY" : None,"Frames" : None}
        self.beingDeath = False


        self.shallHandleCollision = False
        self.immortal = True

    def Destroy(self):
        pass
    def DeathAnimation(self):
        pass

    def set_direction(self):


        pass


    def SelfGravity(self):
        pass


    def add_event(self, event):
        pass

    def update(self):
        pass


    def draw(self):
        pass


    def get_bb(self):
        pass
        #return self.x - 10, self.y - 25, self.x + 10, self.y + 25
    # fill here

    def draw_bb(self):
        pass
        #draw_rectangle(*self.get_bb())


    def CollisionHandling(self,object):
        pass