from pico2d import *

import game_world
import game_framework
import random

from objectBase import ObjectBase
from busterProjectile import BusterProjectile
from explosionEffect import ExplosionEffect

from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode


from ioriExplosion import IoriExplosion
from gigadeathBullet import GigadeathBullet



# Boy Run Speed
# fill expressions correctly
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
# fill expressions correctly

TIME_PER_ACTION = 0.75
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class Gigadeath(ObjectBase):
    actions = 2
    idle = 0

    # test = {"ImageFile" : None,"IntervalX" : None,"IntervalY" : None,"Frames" : None}


    spriteSheet = None

    Images = []

    Test = True

    for i in range(actions):
        Images.append({"ImageFile": None, "IntervalX": None, "IntervalY": None, "Frames": None, "XRevision": None,"Row" : None,"Column" : None})

    Images[idle]["IntervalX"] = 100
    Images[idle]["IntervalY"] = 100
    Images[idle]["Frames"] = 4
    Images[idle]["XRevision"] = 0
    Images[idle]["Row"] = 1
    Images[idle]["Column"] = 10




    deathAnimationActions = 3

    defaultDeathAnimation, deathImmediately, specialDeathAnimation = range(deathAnimationActions)

    deathAnimations = []

    for i in range(deathAnimationActions):
        deathAnimations.append(
            {"ImageFile": None, "IntervalX": None, "IntervalY": None, "Frames": None, "XRevision": None,"YRevision": None})

    deathAnimations[deathImmediately]["IntervalX"] = 100
    deathAnimations[deathImmediately]["IntervalY"] = 100
    deathAnimations[deathImmediately]["Frames"] = 1
    deathAnimations[deathImmediately]["XRevision"] = 0

    def __init__(self):

        if (Gigadeath.spriteSheet == None):
            Gigadeath.spriteSheet = load_image('sprite/GigadeathIdle.png')

        self.kind = game_world.Monster

        self.land = False

        self.curState = game_framework.stack[-1]

        self.x, self.y = self.curState.screenX//2, 250
        self.dir = -1

        self.frame = 0
        self.event_que = []

        # self.cur_state = BusterProjectile.small

        # self.cur_state.enter(self, None)
        self.imageState = Gigadeath.idle


        self.collisionRelation = [game_world.Feature]

        self.selfGravity = False


        self.velocity = 0
        self.velocityY = 0

        self.firePositionX = PIXEL_PER_METER * 0.3
        self.firePositionY = PIXEL_PER_METER * 0.2

        self.x += self.firePositionX
        self.y += self.firePositionY

        #바운딩 박스 출력여부를 결정한다
        self.boundingBoxOn = False

        self.tempGravity = 3

        self.startTimer = get_time()
        self.endTimer = 0

        self.hPMax = 10

        self.curHP = clamp(0, self.hPMax, self.hPMax)

        self.shallHandleCollision = True

        self.deathAnimationNumber = Gigadeath.deathImmediately

        self.beingDeath = False
        self.deathAnimationFrame = 0

        self.clearness = 1



        self.speed = 0

        self.timer = 1.0  # change direction every 1 sec when wandering

        self.build_behavior_tree()

        self.recognizeRange = 100
        self.smashRange = 20


        self.smashDamage = 100

        # self.subject = boy

        #GigadeathBullet관련
        self.busterSpeed = 5
        self.firePositionX = 0.8
        self.firePositionY = 0.45
        self.busterDelay = 1.0


        self.moneyToGive = 200
        self.attackBegin1 = False

        print(self.clearness)

    def set_direction(self):

        pass

    def DeathAnimation(self):

        self.beingDeath = True
        self.shallHandleCollision = False

        if (self.deathAnimationNumber == Gigadeath.deathImmediately):

            if (int(self.deathAnimationFrame) % 3 == 0):
                explosion = ExplosionEffect(random.randint(int(self.get_bb()[0]), int(self.get_bb()[2])),
                                            random.randint(int(self.get_bb()[1]), int(self.get_bb()[3])), self.dir, 0,
                                            0)
                game_world.add_object(explosion, 1)

        pass

    def destroy(self):
        game_world.remove_object(self)

        pass

    def update(self):

        self.endTimer = get_time() - self.startTimer

        if self.endTimer > self.busterDelay:
            if self.attackBegin1:
                self.startTimer = get_time()
                self.attackBegin1 = False


        # self.set_direction()

        if (not self.beingDeath):
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % Gigadeath.Images[self.imageState]["Frames"]
            self.bt.run()
            self.x += self.velocity * self.dir * game_framework.frame_time

        else:
            if (self.deathAnimationNumber == Gigadeath.deathImmediately):
                self.DeathAnimation()
                self.deathAnimationFrame = (
                                                       self.deathAnimationFrame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % \
                                           Gigadeath.deathAnimations[self.deathAnimationNumber]["Frames"]

                if (self.deathAnimationFrame >= Gigadeath.deathAnimations[self.deathAnimationNumber]["Frames"] - 1):
                    self.destroy()



        self.x = clamp(0, self.x, 1600)
        self.y = clamp(0, self.y, 1000)


        pass

    def draw(self):
        if self.curState.showBoundingBox:
            self.draw_bb()
        elif self.boundingBoxOn:
            self.draw_bb()


        if self.dir == 1:
            Gigadeath.spriteSheet.clip_composite_draw(int(self.frame) * Gigadeath.Images[self.imageState]["IntervalX"] + Gigadeath.Images[self.imageState]["XRevision"], Gigadeath.Images[self.imageState]["IntervalY"] * self.imageState, Gigadeath.Images[self.imageState]["IntervalX"],
                                                      Gigadeath.Images[self.imageState]["IntervalY"], 0, 'h', self.x - self.curState.GetBackground().windowLeft, self.y - self.curState.GetBackground().windowBottom, Gigadeath.Images[self.imageState]["IntervalX"], Gigadeath.Images[self.imageState]["IntervalY"])
        else:
            Gigadeath.spriteSheet.clip_composite_draw(int(self.frame) * Gigadeath.Images[self.imageState]["IntervalX"] + Gigadeath.Images[self.imageState]["XRevision"], Gigadeath.Images[self.imageState]["IntervalY"] * self.imageState, Gigadeath.Images[self.imageState]["IntervalX"],
                                                      Gigadeath.Images[self.imageState]["IntervalY"], 0, '', self.x - self.curState.GetBackground().windowLeft, self.y - self.curState.GetBackground().windowBottom, Gigadeath.Images[self.imageState]["IntervalX"], Gigadeath.Images[self.imageState]["IntervalY"])

        if self.beingDeath:
            pass


    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 40, self.y + 20

    # fill here

    def draw_bb(self):
        left,bottom,right,top = self.get_bb()

        left -= self.curState.GetBackground().windowLeft
        bottom -= self.curState.GetBackground().windowBottom
        right -= self.curState.GetBackground().windowLeft
        top -= self.curState.GetBackground().windowBottom


        draw_rectangle(left,bottom,right,top)

    def CollisionHandling(self, object):

        if (not self.shallHandleCollision):
            return

        self.curHP -= object.damage
        if (self.curHP <= 0):
            self.DeathAnimation()
            if(object != None):
                object.subject.money += self.moneyToGive

    def SetPosition(self,x,y):


        self.x = x
        self.y = y

        pass



#인공지능 추가



    def find_player(self):
        # fill here
        #state change
        self.imageState = Gigadeath.idle


        boy = self.curState.get_boy()

        if (boy.x - self.x < 0):
            self.dir = -1
        else:
            self.dir = 1

        distance = (boy.x - self.x) ** 2
        if distance < (PIXEL_PER_METER * self.recognizeRange) ** 2:


            return BehaviorTree.SUCCESS
        else:
            self.velocity = 0
            return BehaviorTree.FAIL
        pass







        pass


    def FireBullet(self):

        boy = self.curState.get_boy()
        self.velocity = 0

        #state change
        self.imageState = Gigadeath.idle

        if not self.attackBegin1:

            bullet = GigadeathBullet(self)
            game_world.add_object(bullet,1)
            self.attackBegin1 = True


        return BehaviorTree.SUCCESS

        pass


    def build_behavior_tree(self):
        # fill here




        find_player_node = LeafNode("Find Player", self.find_player)


        fireBulletNode = LeafNode("Fire Bullet", self.FireBullet)

        findAndFireNode = SequenceNode("Fire")
        findAndFireNode.add_children(find_player_node, fireBulletNode)





        self.bt = BehaviorTree(findAndFireNode)

        #wander_node = LeafNode("Wander", self.wander)
        #self.bt = BehaviorTree(wander_node)
        pass