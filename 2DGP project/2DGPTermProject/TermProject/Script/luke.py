from pico2d import *

import game_world
import game_framework
import random


from objectBase import ObjectBase
from busterProjectile import BusterProjectile
from explosionEffect import ExplosionEffect

from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode


from ioriExplosion import IoriExplosion

from portalBlue import PortalBlue


from icePick import IcePick


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


class Luke(ObjectBase):
    actions = 6
    idle,appear,walking,attack1,attack2,attack3 = range(actions)

    # test = {"ImageFile" : None,"IntervalX" : None,"IntervalY" : None,"Frames" : None}


    spriteSheet = None

    Images = []

    Test = True

    for i in range(actions):
        Images.append({"ImageFile": None, "IntervalX": None, "IntervalY": None, "Frames": None, "XRevision": None,"Row" : None,"Column" : None})





    Images[idle]["IntervalX"] = 300
    Images[idle]["IntervalY"] = 300
    Images[idle]["Frames"] = 6
    Images[idle]["XRevision"] = 0
    Images[idle]["Row"] = 10
    Images[idle]["Column"] = 10



    Images[appear]["IntervalX"] = 300
    Images[appear]["IntervalY"] = 300
    Images[appear]["Frames"] = 54
    Images[appear]["XRevision"] = 0
    Images[appear]["Row"] = 13
    Images[appear]["Column"] = 10


    Images[walking]["IntervalX"] = 300
    Images[walking]["IntervalY"] = 300
    Images[walking]["Frames"] = 8
    Images[walking]["XRevision"] = 0
    Images[walking]["Row"] = 3
    Images[walking]["Column"] = 10




    Images[attack1]["IntervalX"] = 300
    Images[attack1]["IntervalY"] = 300
    Images[attack1]["Frames"] = 17
    Images[attack1]["XRevision"] = 0
    Images[attack1]["Row"] = 7
    Images[attack1]["Column"] = 10



    Images[attack2]["IntervalX"] = 300
    Images[attack2]["IntervalY"] = 300
    Images[attack2]["Frames"] = 4
    Images[attack2]["XRevision"] = 0
    Images[attack2]["Row"] = 5
    Images[attack2]["Column"] = 10



    Images[attack3]["IntervalX"] = 300
    Images[attack3]["IntervalY"] = 300
    Images[attack3]["Frames"] = 8
    Images[attack3]["XRevision"] = 0
    Images[attack3]["Row"] = 4
    Images[attack3]["Column"] = 10



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

        if (Luke.spriteSheet == None):
            Luke.spriteSheet = load_image('sprite/luke2.png')

        Luke.spriteSheet.opacify(1)

        self.kind = game_world.Monster

        self.land = False


        self.dir = -1

        self.frame = 0
        self.event_que = []

        # self.cur_state = BusterProjectile.small

        # self.cur_state.enter(self, None)
        self.imageState = Luke.appear


        self.collisionRelation = [game_world.Feature]

        self.selfGravity = False


        self.velocity = 0
        self.velocityY = 0





        #바운딩 박스 출력여부를 결정한다
        self.boundingBoxOn = False

        self.tempGravity = 3

        self.startTimer = get_time()
        self.endTimer = 0

        self.hPMax = 200

        self.curHP = clamp(0, self.hPMax, self.hPMax)

        self.shallHandleCollision = True

        self.deathAnimationNumber = Luke.deathImmediately

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


        self.attack1Begin = False
        self.attack2Begin = False
        self.attack3Begin = False

        self.targetXPosition = 0
        self.targetYPosition = 0


        self.x, self.y = self.curState.screenX - 400, 250


        self.row = Luke.Images[self.imageState]["Row"] - 1
        self.check = False

    def set_direction(self):

        pass

    def DeathAnimation(self):

        self.beingDeath = True
        self.shallHandleCollision = False

        if (self.deathAnimationNumber == Luke.deathImmediately):
            self.clearness = (self.clearness + 0.3) % 1
            Luke.spriteSheet.opacify(self.clearness)
            if (int(self.deathAnimationFrame) % 3 == 0):
                explosion = ExplosionEffect(random.randint(int(self.get_bb()[0]), int(self.get_bb()[2])),
                                            random.randint(int(self.get_bb()[1]), int(self.get_bb()[3])), self.dir, 0,
                                            0)
                game_world.add_object(explosion, 1)

        pass

    def destroy(self):

        if self.curState.name == "Stage1":
            portal = PortalBlue(self)
            game_world.add_object(portal,1)



        game_world.remove_object(self)

        pass

    def update(self):


        self.endTimer = get_time() - self.startTimer



        # self.set_direction()

        if (not self.beingDeath):
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % Luke.Images[self.imageState]["Frames"]
            if(self.imageState != Luke.appear):
                self.bt.run()
            self.x += self.velocity * self.dir * game_framework.frame_time

            if (int(self.frame) == 0):
                self.row = Luke.Images[self.imageState]["Row"] - 1


            elif int(self.frame) % Luke.Images[self.imageState]["Column"] == 0:
                if (not self.check):
                    self.row -= 1
                    self.check = True
            else:
                self.check = False

            if (int(self.frame) >= Luke.Images[self.imageState]["Frames"] - 1):
                if(self.imageState == Luke.appear):
                    self.imageState = Luke.walking
                self.row = Luke.Images[self.imageState]["Row"] - 1




        else:
            if (self.deathAnimationNumber == Luke.deathImmediately):
                self.DeathAnimation()
                self.deathAnimationFrame = (
                                                       self.deathAnimationFrame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % \
                                           Luke.deathAnimations[self.deathAnimationNumber]["Frames"]

                if (self.deathAnimationFrame >= Luke.deathAnimations[self.deathAnimationNumber]["Frames"] - 1):
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
            Luke.spriteSheet.clip_composite_draw( ( int(self.frame) % Luke.Images[self.imageState]["Column"] ) * Luke.Images[self.imageState]["IntervalX"] + Luke.Images[self.imageState]["XRevision"], Luke.Images[self.imageState]["IntervalY"] * self.row, Luke.Images[self.imageState]["IntervalX"], Luke.Images[self.imageState]["IntervalY"], 0, '', self.x- self.curState.GetBackground().windowLeft, self.y- self.curState.GetBackground().windowBottom, Luke.Images[self.imageState]["IntervalX"], Luke.Images[self.imageState]["IntervalY"])
        else:
            Luke.spriteSheet.clip_composite_draw(( int(self.frame) % Luke.Images[self.imageState]["Column"] )  * Luke.Images[self.imageState]["IntervalX"] + Luke.Images[self.imageState]["XRevision"], Luke.Images[self.imageState]["IntervalY"] * self.row, Luke.Images[self.imageState]["IntervalX"], Luke.Images[self.imageState]["IntervalY"], 0, 'h', self.x- self.curState.GetBackground().windowLeft, self.y- self.curState.GetBackground().windowBottom, Luke.Images[self.imageState]["IntervalX"], Luke.Images[self.imageState]["IntervalY"])


        if self.beingDeath:
            pass


    def get_bb(self):
        return self.x - 60, self.y - 150, self.x + 60, self.y + 60

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
        self.imageState = Luke.walking


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
        self.imageState = Luke.walking


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
        self.imageState = Luke.walking


        if get_time() - self.smashRecognizeTimer > self.smashRecognizeTime:
            self.targetXPosition = boy.x
            self.targetYPosition = boy.landingYPosition
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



    def Attack1(self):

        boy = self.curState.get_boy()
        self.velocity = 0
        self.imageState = Luke.attack1
        #state change

        if(not self.attack1Begin):
            self.attack1Begin = True
            self.frame = 0
            self.targetXPosition = boy.x
            self.targetYPosition = boy.landingYPosition

        if(self.frame >= 3):

            if self.curHP > self.hPMax // 2:
                if(self.frame - int(self.frame) < 0.1):
                    ice = IcePick(self.targetXPosition ,self.targetYPosition,self.dir,self.smashDamage)
                    game_world.add_object(ice,1)
                    self.targetXPosition = boy.x
                    self.targetYPosition = boy.landingYPosition

            else:
                if(self.frame - int(self.frame) < 0.2):
                    ice = IcePick(self.targetXPosition ,self.targetYPosition,self.dir,self.smashDamage)
                    game_world.add_object(ice,1)
                    self.targetXPosition = boy.x
                    self.targetYPosition = boy.landingYPosition
                    print("우우아악악")


        if(int(self.frame) >= Luke.Images[self.imageState]["Frames"] - 1):
            self.attack1Begin = False
            return BehaviorTree.SUCCESS

        else:
            return BehaviorTree.RUNNING

        pass

#낙뢰
    def Attack2(self):

        boy = self.curState.get_boy()
        self.velocity = 0
        self.imageState = Luke.attack2
        #state change

        if(not self.attack2Begin):
            self.attack2Begin = True
            self.frame = 0
            self.targetXPosition = boy.x
            self.targetYPosition = boy.landingYPosition

        if(self.frame >= 3):

            if self.curHP > self.hPMax // 2:
                if(self.frame - int(self.frame) < 0.1):
                    ice = IcePick(self.targetXPosition ,self.targetYPosition,self.dir,self.smashDamage)
                    game_world.add_object(ice,1)
                    self.targetXPosition = boy.x
                    self.targetYPosition = boy.landingYPosition

            else:
                if(self.frame - int(self.frame) < 0.2):
                    ice = IcePick(self.targetXPosition ,self.targetYPosition,self.dir,self.smashDamage)
                    game_world.add_object(ice,1)
                    self.targetXPosition = boy.x
                    self.targetYPosition = boy.landingYPosition
                    print("우우아악악")


        if(int(self.frame) >= Luke.Images[self.imageState]["Frames"] - 1):
            self.attack2Begin = False
            return BehaviorTree.SUCCESS

        else:
            return BehaviorTree.RUNNING

        pass







    def build_behavior_tree(self):
        # fill here

        wander_node = LeafNode("Wander", self.wander)


        find_player_node = LeafNode("Find Player", self.find_player)
        move_to_player_node = LeafNode("Move to Player", self.move_to_player)
        attack1Node = LeafNode("Attack1", self.Attack1)

        chase_node = SequenceNode("Chase")
        chase_node.add_children(find_player_node, move_to_player_node)
        chase_node.add_child(attack1Node)

        wander_chase_node = SelectorNode("WanderChase")
        wander_chase_node.add_children(chase_node, wander_node)


        self.bt = BehaviorTree(wander_chase_node)

        #wander_node = LeafNode("Wander", self.wander)
        #self.bt = BehaviorTree(wander_node)
        pass