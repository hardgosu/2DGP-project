from pico2d import *

import game_world
import game_framework
import main_state
import random


from objectBase import ObjectBase
from busterProjectile import BusterProjectile
from explosionEffect import ExplosionEffect


# Boy Run Speed
# fill expressions correctly
PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


# Boy Action Speed
# fill expressions correctly

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8







class EnemyTest(ObjectBase):

    actions = 1
    idle = 0

    #test = {"ImageFile" : None,"IntervalX" : None,"IntervalY" : None,"Frames" : None}

    Images = []


    Test = True


    for i in range(actions):
        Images.append({"ImageFile": None, "IntervalX": None, "IntervalY": None, "Frames": None, "XRevision": None})


    Images[idle]["IntervalX"] = 172
    Images[idle]["IntervalY"] = 207
    Images[idle]["Frames"] = 16
    Images[idle]["XRevision"] = 171



    deathAnimationActions = 3

    defaultDeathAnimation, deathImmediately, specialDeathAnimation = range(deathAnimationActions)

    deathAnimations = []

    for i in range(deathAnimationActions):
        deathAnimations.append({"ImageFile": None, "IntervalX": None, "IntervalY": None, "Frames": None, "XRevision": None})




    deathAnimations[deathImmediately]["IntervalX"] = 100
    deathAnimations[deathImmediately]["IntervalY"] = 100
    deathAnimations[deathImmediately]["Frames"] = 20
    deathAnimations[deathImmediately]["XRevision"] = 0







    def __init__(self):

        if(EnemyTest.Images[EnemyTest.idle]["ImageFile"] == None):
            EnemyTest.Images[EnemyTest.idle]["ImageFile"] = load_image('testBoss.png')



        self.kind = game_world.Monster

        self.land = False

        self.x, self.y = main_state.screenX - 180,90
        self.dir = 1
        #self.velocity = velocityX *RUN_SPEED_PPS
        self.frame = 0
        self.event_que = []


        #self.cur_state = BusterProjectile.small

        #self.cur_state.enter(self, None)
        self.imageState = EnemyTest.idle

        self.collisionRelation = [game_world.Feature]



        self.selfGravity = False

        self.velocityY = 0

        self.firePositionX = PIXEL_PER_METER * 0.3
        self.firePositionY = PIXEL_PER_METER * 0.2


        self.x += self.firePositionX
        self.y += self.firePositionY

        self.boundingBoxOn = True

        self.tempGravity = 3

        self.startTimer = get_time()
        self.endTimer = 0

        self.hPMax = 100

        self.curHP = clamp(0,self.hPMax,self.hPMax)

        self.shallHandleCollision = True


        self.deathAnimationNumber = EnemyTest.deathImmediately

        self.beingDeath = False
        self.deathAnimationFrame = 0

        self.clearness = 1



        #self.subject = boy

    def set_direction(self):



        pass

    def DeathAnimation(self):

        self.beingDeath = True
        self.shallHandleCollision = False

        if( self.deathAnimationNumber == EnemyTest.deathImmediately):
            self.clearness = (self.clearness + 0.3) % 1
            EnemyTest.Images[self.imageState]["ImageFile"].opacify(self.clearness)
            if(int(self.deathAnimationFrame) % 3 == 0):
                explosion = ExplosionEffect(random.randint( int(self.get_bb()[0]) , int(self.get_bb()[2]) ),random.randint( int(self.get_bb()[1]) , int(self.get_bb()[3]) ),self.dir,0,0)
                game_world.add_object(explosion,1)
                pass

            pass


        pass

    def destroy(self):
        game_world.remove_object(self)


        pass



    def update(self):


        self.endTimer = get_time() - self.startTimer



        #self.set_direction()

        if(not self.beingDeath):
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % EnemyTest.Images[self.imageState]["Frames"]

        else:
            if(self.deathAnimationNumber == EnemyTest.deathImmediately):
                self.DeathAnimation()
                self.deathAnimationFrame = (self.deathAnimationFrame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % EnemyTest.deathAnimations[self.deathAnimationNumber]["Frames"]

                if (self.deathAnimationFrame >= EnemyTest.deathAnimations[self.deathAnimationNumber]["Frames"] - 1):
                    self.destroy()




        #self.x += self.velocity * self.dir * game_framework.frame_time



        pass


    def draw(self):
        if self.boundingBoxOn:
            self.draw_bb()

        if self.dir == 1:
            EnemyTest.Images[self.imageState]["ImageFile"].clip_composite_draw(int(self.frame) * EnemyTest.Images[self.imageState]["IntervalX"] + EnemyTest.Images[self.imageState]["XRevision"], 0, EnemyTest.Images[self.imageState]["IntervalX"], EnemyTest.Images[self.imageState]["IntervalY"], 0, '', self.x, self.y, EnemyTest.Images[self.imageState]["IntervalX"], EnemyTest.Images[self.imageState]["IntervalY"])
        else:
            EnemyTest.Images[self.imageState]["ImageFile"].clip_composite_draw(int(self.frame) * EnemyTest.Images[self.imageState]["IntervalX"] + EnemyTest.Images[self.imageState]["XRevision"], 0, EnemyTest.Images[self.imageState]["IntervalX"], EnemyTest.Images[self.imageState]["IntervalY"], 0, 'h', self.x, self.y, EnemyTest.Images[self.imageState]["IntervalX"], EnemyTest.Images[self.imageState]["IntervalY"])

        if self.beingDeath:
            pass



    def get_bb(self):
        return self.x - 87, self.y - 95, self.x + 87, self.y + 95
    # fill here

    def draw_bb(self):
        draw_rectangle(*self.get_bb())
    
    def CollisionHandling(self,object):

        if(not self.shallHandleCollision):
            return

        self.curHP -= object.damage
        if(self.curHP <= 0):
            self.DeathAnimation()


