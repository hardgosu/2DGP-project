from pico2d import *

import game_world
import game_framework
import main_state
import random


from objectBase import ObjectBase
from busterProjectile import BusterProjectile
from explosionEffect import ExplosionEffect

from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode


from ioriExplosion import IoriExplosion

from portalBlue import PortalBlue



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


class TowBeast(ObjectBase):
    actions = 6
    death,shouting,smashing,headButt,walking,idle = range(6)

    # test = {"ImageFile" : None,"IntervalX" : None,"IntervalY" : None,"Frames" : None}


    spriteSheet = None

    Images = []

    Test = True

    for i in range(actions):
        Images.append({"ImageFile": None, "IntervalX": None, "IntervalY": None, "Frames": None, "XRevision": None})

    Images[idle]["IntervalX"] = 400
    Images[idle]["IntervalY"] = 400
    Images[idle]["Frames"] = 1
    Images[idle]["XRevision"] = 0

    Images[walking]["IntervalX"] = 400
    Images[walking]["IntervalY"] = 400
    Images[walking]["Frames"] = 8
    Images[walking]["XRevision"] = 0

    Images[headButt]["IntervalX"] = 400
    Images[headButt]["IntervalY"] = 400
    Images[headButt]["Frames"] = 6
    Images[headButt]["XRevision"] = 0


    Images[smashing]["IntervalX"] = 400
    Images[smashing]["IntervalY"] = 400
    Images[smashing]["Frames"] = 6
    Images[smashing]["XRevision"] = 0


    Images[shouting]["IntervalX"] = 400
    Images[shouting]["IntervalY"] = 400
    Images[shouting]["Frames"] = 4
    Images[shouting]["XRevision"] = 0




    deathAnimationActions = 3

    defaultDeathAnimation, deathImmediately, specialDeathAnimation = range(deathAnimationActions)

    deathAnimations = []

    for i in range(deathAnimationActions):
        deathAnimations.append(
            {"ImageFile": None, "IntervalX": None, "IntervalY": None, "Frames": None, "XRevision": None})

    deathAnimations[deathImmediately]["IntervalX"] = 100
    deathAnimations[deathImmediately]["IntervalY"] = 100
    deathAnimations[deathImmediately]["Frames"] = 20
    deathAnimations[deathImmediately]["XRevision"] = 0

    def __init__(self):

        if (TowBeast.spriteSheet == None):
            TowBeast.spriteSheet = load_image('sprite/towBeast.png')

        TowBeast.spriteSheet.opacify(1)

        self.kind = game_world.Monster

        self.land = False

        self.x, self.y = main_state.screenX - 400, 250
        self.dir = -1

        self.frame = 0
        self.event_que = []

        # self.cur_state = BusterProjectile.small

        # self.cur_state.enter(self, None)
        self.imageState = TowBeast.idle


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

        self.hPMax = 200

        self.curHP = clamp(0, self.hPMax, self.hPMax)

        self.shallHandleCollision = True

        self.deathAnimationNumber = TowBeast.deathImmediately

        self.beingDeath = False
        self.deathAnimationFrame = 0

        self.clearness = 1



        self.speed = 0

        self.timer = 1.0  # change direction every 1 sec when wandering

        self.build_behavior_tree()

        self.recognizeRange = 100
        self.smashRecognizeTime = 0.5
        self.smashRange = 15
        self.smashRecognizeTimer = 0


        #damage 필드
        self.smashDamage = 10

        # self.subject = boy


        self.curState = game_framework.stack[-1]

        self.moneyToGive = 5000


        self.smashBegin = False

        self.targetXPosition = 0
        self.targetYPosition = 0

    def set_direction(self):

        pass

    def DeathAnimation(self):

        self.beingDeath = True
        self.shallHandleCollision = False

        if (self.deathAnimationNumber == TowBeast.deathImmediately):
            self.clearness = (self.clearness + 0.3) % 1
            TowBeast.spriteSheet.opacify(self.clearness)
            if (int(self.deathAnimationFrame) % 3 == 0):
                explosion = ExplosionEffect(random.randint(int(self.get_bb()[0]), int(self.get_bb()[2])),
                                            random.randint(int(self.get_bb()[1]), int(self.get_bb()[3])), self.dir, 0,
                                            0)
                game_world.add_object(explosion, 1)

        pass

    def destroy(self):

        if self.curState.name == "Stage1":
            self.curState.genPortalSwitch = True



        game_world.remove_object(self)

        pass

    def update(self):


        self.endTimer = get_time() - self.startTimer



        # self.set_direction()

        if (not self.beingDeath):
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % TowBeast.Images[self.imageState]["Frames"]
            self.bt.run()
            self.x += self.velocity * self.dir * game_framework.frame_time

        else:
            if (self.deathAnimationNumber == TowBeast.deathImmediately):
                self.DeathAnimation()
                self.deathAnimationFrame = (
                                                       self.deathAnimationFrame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % \
                                           TowBeast.deathAnimations[self.deathAnimationNumber]["Frames"]

                if (self.deathAnimationFrame >= TowBeast.deathAnimations[self.deathAnimationNumber]["Frames"] - 1):
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
            TowBeast.spriteSheet.clip_composite_draw(int(self.frame) * TowBeast.Images[self.imageState]["IntervalX"] + TowBeast.Images[self.imageState]["XRevision"], TowBeast.Images[self.imageState]["IntervalY"] * self.imageState, TowBeast.Images[self.imageState]["IntervalX"],
                TowBeast.Images[self.imageState]["IntervalY"], 0, '', self.x - self.curState.GetBackground().windowLeft, self.y - self.curState.GetBackground().windowBottom,TowBeast.Images[self.imageState]["IntervalX"], TowBeast.Images[self.imageState]["IntervalY"])
        else:
            TowBeast.spriteSheet.clip_composite_draw(int(self.frame) * TowBeast.Images[self.imageState]["IntervalX"] + TowBeast.Images[self.imageState]["XRevision"], TowBeast.Images[self.imageState]["IntervalY"] * self.imageState, TowBeast.Images[self.imageState]["IntervalX"],
                TowBeast.Images[self.imageState]["IntervalY"], 0, 'h', self.x - self.curState.GetBackground().windowLeft, self.y - self.curState.GetBackground().windowBottom,TowBeast.Images[self.imageState]["IntervalX"], TowBeast.Images[self.imageState]["IntervalY"])

        if self.beingDeath:
            pass


    def get_bb(self):
        return self.x - 90, self.y - 200, self.x + 50, self.y + 60

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

    def wander(self):
        # fill here

        #state change
        self.imageState = TowBeast.walking


        self.velocity = RUN_SPEED_PPS
        self.timer -= game_framework.frame_time
        if self.timer < 0:
            self.timer += 1.0
            self.dir = random.randint(-1,0)
            if(self.dir == 0):
                self.dir = 1
        return BehaviorTree.SUCCESS

        pass

    def find_player(self):
        # fill here
        #state change
        self.imageState = TowBeast.walking


        boy = self.curState.get_boy()

        distance = (boy.x - self.x) ** 2
        if distance < (PIXEL_PER_METER * self.recognizeRange) ** 2:

            if(boy.x - self.x < 0):
                self.dir = -1
            else:
                self.dir = 1

            return BehaviorTree.SUCCESS
        else:
            self.velocity = 0
            return BehaviorTree.FAIL
        pass

    def move_to_player(self):
        # fill here

        boy = self.curState.get_boy()

        self.velocity = RUN_SPEED_PPS


        #state change
        self.imageState = TowBeast.walking


        if get_time() - self.smashRecognizeTimer > self.smashRecognizeTime:
            self.targetXPosition = boy.x
            self.smashRecognizeTimer = get_time()







        distance = (boy.x - self.x) ** 2
        if distance < (PIXEL_PER_METER * (self.smashRange)) ** 2:

            if(boy.x - self.x < 0):
                self.dir = -1
            else:
                self.dir = 1

            return BehaviorTree.SUCCESS

        if distance >=(PIXEL_PER_METER * self.recognizeRange) ** 2:

            if(boy.x - self.x < 0):
                self.dir = -1
            else:
                self.dir = 1


            return BehaviorTree.FAIL

        else:

            return BehaviorTree.RUNNING






        pass


    def SmashAttack(self):

        boy = self.curState.get_boy()
        self.velocity = 0
        self.imageState = TowBeast.smashing
        #state change

        if(not self.smashBegin):
            self.smashBegin = True
            self.frame = 0
            self.targetXPosition = boy.x


        if(self.frame >= 3):

            if self.curHP > self.hPMax // 2:
                if(self.frame - int(self.frame) < 0.1):
                    explosion = IoriExplosion(self.targetXPosition ,self.y,-self.dir,self.smashDamage)
                    game_world.add_object(explosion,1)
                    self.targetXPosition = boy.x

            else:
                if(self.frame - int(self.frame) < 0.2):
                    explosion = IoriExplosion(self.targetXPosition ,self.y,-self.dir,self.smashDamage)
                    game_world.add_object(explosion,1)
                    self.targetXPosition = boy.x
                    print("우우아악")


        if(int(self.frame) >= TowBeast.Images[self.imageState]["Frames"] - 1):
            self.smashBegin = False
            return BehaviorTree.SUCCESS

        else:
            return BehaviorTree.RUNNING

        pass


    def build_behavior_tree(self):
        # fill here

        wander_node = LeafNode("Wander", self.wander)


        find_player_node = LeafNode("Find Player", self.find_player)
        move_to_player_node = LeafNode("Move to Player", self.move_to_player)
        SmashAttckNode = LeafNode("Smash Attck",self.SmashAttack)

        chase_node = SequenceNode("Chase")
        chase_node.add_children(find_player_node, move_to_player_node)
        chase_node.add_child(SmashAttckNode)

        wander_chase_node = SelectorNode("WanderChase")
        wander_chase_node.add_children(chase_node, wander_node)


        self.bt = BehaviorTree(wander_chase_node)

        #wander_node = LeafNode("Wander", self.wander)
        #self.bt = BehaviorTree(wander_node)
        pass