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
from thunder import Thunder
from kaiserWave import KaiserWave

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


class Rozen(ObjectBase):
    actions = 5
    capeIdle,unCape,idle,walking,attack1 = range(actions)

    # test = {"ImageFile" : None,"IntervalX" : None,"IntervalY" : None,"Frames" : None}


    spriteSheet = None

    Images = []

    Test = True

    for i in range(actions):
        Images.append({"ImageFile": None, "IntervalX": None, "IntervalY": None, "Frames": None, "XRevision": None,"Row" : None,"Column" : None})





    Images[idle]["IntervalX"] = 300
    Images[idle]["IntervalY"] = 300
    Images[idle]["Frames"] = 10
    Images[idle]["XRevision"] = 0
    Images[idle]["Row"] = 5
    Images[idle]["Column"] = 10

    Images[capeIdle]["IntervalX"] = 300
    Images[capeIdle]["IntervalY"] = 300
    Images[capeIdle]["Frames"] = 13
    Images[capeIdle]["XRevision"] = 0
    Images[capeIdle]["Row"] = 9
    Images[capeIdle]["Column"] = 10



    Images[walking]["IntervalX"] = 300
    Images[walking]["IntervalY"] = 300
    Images[walking]["Frames"] = 8
    Images[walking]["XRevision"] = 0
    Images[walking]["Row"] = 3
    Images[walking]["Column"] = 10




    Images[attack1]["IntervalX"] = 300
    Images[attack1]["IntervalY"] = 300
    Images[attack1]["Frames"] = 18
    Images[attack1]["XRevision"] = 0
    Images[attack1]["Row"] = 2
    Images[attack1]["Column"] = 10



    Images[unCape]["IntervalX"] = 300
    Images[unCape]["IntervalY"] = 300
    Images[unCape]["Frames"] = 13
    Images[unCape]["XRevision"] = 0
    Images[unCape]["Row"] = 7
    Images[unCape]["Column"] = 10






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



    hPBarImage = None
    hPBarImageX = 100
    hPBarImageY = 20

    def __init__(self):

        if (Rozen.spriteSheet == None):
            Rozen.spriteSheet = load_image('sprite/rozen2.png')

        Rozen.spriteSheet.opacify(1)

        self.kind = game_world.Monster

        self.land = False


        self.dir = -1

        self.frame = 0
        self.event_que = []

        # self.cur_state = BusterProjectile.small

        # self.cur_state.enter(self, None)
        self.imageState = Rozen.capeIdle


        self.collisionRelation = [game_world.Feature]

        self.selfGravity = False


        self.velocity = 0
        self.velocityY = 0





        #바운딩 박스 출력여부를 결정한다
        self.boundingBoxOn = False

        self.tempGravity = 3

        self.startTimer = get_time()
        self.endTimer = 0

        self.hPMax = 2125

        self.curHP = clamp(0, self.hPMax, self.hPMax)

        self.shallHandleCollision = True

        self.deathAnimationNumber = Rozen.deathImmediately

        self.beingDeath = False
        self.deathAnimationFrame = 0

        self.clearness = 1



        self.speed = 0

        self.timer = 1.0  # change direction every 1 sec when wandering

        self.build_behavior_tree()

        self.recognizeRange = 100
        self.smashRecognizeTime = 0.5
        self.smashRange = 20
        self.smashRecognizeTimer = 0


        #damage 필드
        self.thunderDamage = 15
        self.icePickDamage = 12


        #KaiserWave 관련
        self.busterSpeed = 10
        self.firePositionX = 0.4
        self.firePositionY = -0.9


        # self.subject = boy


        self.curState = game_framework.stack[-1]

        self.moneyToGive = 10000


        self.attack1Begin = False
        self.attack2Begin = False
        self.attack3Begin = False

        self.targetXPosition = 0
        self.targetYPosition = 0


        self.x, self.y = self.curState.screenX - 400, 250


        self.row = Rozen.Images[self.imageState]["Row"] - 1
        self.check = False


        self.showHPBar = True
        if Rozen.hPBarImage == None:
            Rozen.hPBarImage = load_image('sprite/UI/HPBar.png')




    def set_direction(self):

        pass

    def DeathAnimation(self):

        self.beingDeath = True
        self.shallHandleCollision = False

        if (self.deathAnimationNumber == Rozen.deathImmediately):
            self.clearness = (self.clearness + 0.3) % 1
            Rozen.spriteSheet.opacify(self.clearness)
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

        if self.curState.name == "Stage2":
            portal = PortalBlue(self)
            game_world.add_object(portal,1)
        if self.curState.name == "Stage3":
            portal = PortalBlue(self)
            game_world.add_object(portal,1)

        game_world.remove_object(self)

        pass

    def update(self):


        self.endTimer = get_time() - self.startTimer



        # self.set_direction()

        if (not self.beingDeath):
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % Rozen.Images[self.imageState]["Frames"]
            if(self.imageState != Rozen.capeIdle):
                if( self.imageState != Rozen.unCape):
                    self.bt.run()
            self.x += self.velocity * self.dir * game_framework.frame_time

            if (int(self.frame) == 0):
                self.row = Rozen.Images[self.imageState]["Row"] - 1


            elif int(self.frame) % Rozen.Images[self.imageState]["Column"] == 0:
                if (not self.check):
                    self.row -= 1
                    self.check = True
            else:
                self.check = False

            if (int(self.frame) >= Rozen.Images[self.imageState]["Frames"] - 1):
                if(self.imageState == Rozen.capeIdle):
                    self.imageState = Rozen.unCape
                elif (self.imageState == Rozen.unCape):
                    self.imageState = Rozen.walking
                self.row = Rozen.Images[self.imageState]["Row"] - 1
                self.frame = 0



        else:
            if (self.deathAnimationNumber == Rozen.deathImmediately):
                self.DeathAnimation()
                self.deathAnimationFrame = (
                                                       self.deathAnimationFrame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % \
                                           Rozen.deathAnimations[self.deathAnimationNumber]["Frames"]

                if (self.deathAnimationFrame >= Rozen.deathAnimations[self.deathAnimationNumber]["Frames"] - 1):
                    self.destroy()



        self.x = clamp(0, self.x, 1600)
        self.y = clamp(0, self.y, 1000)




        pass

    def draw(self):
        if self.curState.showBoundingBox:
            self.draw_bb()
        elif self.boundingBoxOn:
            self.draw_bb()

        self.DisplayHPBar()


        if self.dir == 1:
            Rozen.spriteSheet.clip_composite_draw((int(self.frame) % Rozen.Images[self.imageState]["Column"]) * Rozen.Images[self.imageState]["IntervalX"] + Rozen.Images[self.imageState]["XRevision"], Rozen.Images[self.imageState]["IntervalY"] * self.row, Rozen.Images[self.imageState]["IntervalX"], Rozen.Images[self.imageState]["IntervalY"], 0, '', self.x - self.curState.GetBackground().windowLeft, self.y - self.curState.GetBackground().windowBottom, Rozen.Images[self.imageState]["IntervalX"], Rozen.Images[self.imageState]["IntervalY"])
        else:
            Rozen.spriteSheet.clip_composite_draw((int(self.frame) % Rozen.Images[self.imageState]["Column"]) * Rozen.Images[self.imageState]["IntervalX"] + Rozen.Images[self.imageState]["XRevision"], Rozen.Images[self.imageState]["IntervalY"] * self.row, Rozen.Images[self.imageState]["IntervalX"], Rozen.Images[self.imageState]["IntervalY"], 0, 'h', self.x - self.curState.GetBackground().windowLeft, self.y - self.curState.GetBackground().windowBottom, Rozen.Images[self.imageState]["IntervalX"], Rozen.Images[self.imageState]["IntervalY"])


        if self.beingDeath:
            pass


    def get_bb(self):
        return self.x - 60, self.y - 150, self.x + 30, self.y + 60

    # fill here

    def draw_bb(self):
        if not self.curState.showBoundingBox:
            return
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


    def DisplayHPBar(self):

        if(not self.showHPBar):
            return

        Rozen.hPBarImage.draw(self.x - self.curState.GetBackground().windowLeft + 0, self.y + 80 - self.curState.GetBackground().windowBottom, int(Rozen.hPBarImageX * (self.curHP / self.hPMax)), Rozen.hPBarImageY)


        pass






#인공지능 추가

    def wander(self):
        # fill here

        #state change
        self.imageState = Rozen.walking


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
        self.imageState = Rozen.walking


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

    def move_to_player(self):
        # fill here

        boy = self.curState.get_boy()

        self.velocity = RUN_SPEED_PPS


        #state change
        self.imageState = Rozen.walking


        if get_time() - self.smashRecognizeTimer > self.smashRecognizeTime:
            self.targetXPosition = boy.x
            self.targetYPosition = boy.landingYPosition
            self.smashRecognizeTimer = get_time()



        if(boy.x - self.x < 0):
            self.dir = -1
        else:
            self.dir = 1



        distance = (boy.x - self.x) ** 2
        if distance < (PIXEL_PER_METER * (self.smashRange)) ** 2:



            return BehaviorTree.SUCCESS

        if distance >=(PIXEL_PER_METER * self.recognizeRange) ** 2:



            return BehaviorTree.FAIL

        else:

            return BehaviorTree.RUNNING



    def Attack1(self):


        if random.randint(0,1) == 0:
            if(not self.attack1Begin):
                return BehaviorTree.FAIL

        boy = self.curState.get_boy()
        self.velocity = 0
        self.imageState = Rozen.attack1
        #state change

        if(not self.attack1Begin):
            self.attack1Begin = True
            self.frame = 0
            self.targetXPosition = boy.x
            self.targetYPosition = boy.landingYPosition

        if(self.frame >= 3):

            if self.curHP > self.hPMax // 2:
                if(self.frame - int(self.frame) < 0.1):
                    ice = IcePick(self.targetXPosition, self.targetYPosition, self.dir, self.icePickDamage)
                    game_world.add_object(ice,1)
                    self.targetXPosition = boy.x
                    self.targetYPosition = boy.landingYPosition

            else:
                if(self.frame - int(self.frame) < 0.2):
                    ice = IcePick(self.targetXPosition, self.targetYPosition, self.dir, self.icePickDamage)
                    game_world.add_object(ice,1)
                    self.targetXPosition = boy.x
                    self.targetYPosition = boy.landingYPosition



        if(int(self.frame) >= Rozen.Images[self.imageState]["Frames"] - 1):
            self.attack1Begin = False
            self.frame = 0
            return BehaviorTree.SUCCESS

        else:
            return BehaviorTree.RUNNING

        pass

#낙뢰
    def Attack2(self):

        if random.randint(0,1) == 0:
            if(not self.attack2Begin):
                return BehaviorTree.FAIL

        boy = self.curState.get_boy()
        self.velocity = 0
        self.imageState = Rozen.attack1
        #state change

        if(not self.attack2Begin):
            self.attack2Begin = True
            self.frame = 0
            self.targetXPosition = boy.x
            self.targetYPosition = boy.landingYPosition + 100

        if(self.frame >= 2):

            if self.curHP > self.hPMax // 2:
                thunder = Thunder(self.targetXPosition, self.targetYPosition, self.dir, self.thunderDamage)
                game_world.add_object(thunder,1)
                self.targetXPosition = boy.x
                self.targetYPosition = boy.landingYPosition + thunder.get_bb()[1]

            else:

                thunder = Thunder(self.targetXPosition, self.targetYPosition, self.dir, self.thunderDamage)
                game_world.add_object(thunder,1)
                self.targetXPosition = boy.x
                self.targetYPosition = boy.landingYPosition + thunder.get_bb()[1]



        if(int(self.frame) >= Rozen.Images[self.imageState]["Frames"] - 1):
            self.attack2Begin = False
            self.frame = 0
            return BehaviorTree.SUCCESS

        else:
            return BehaviorTree.RUNNING

        pass
#폭발
    def Attack3(self):

        boy = self.curState.get_boy()
        self.velocity = 0
        self.imageState = Rozen.attack1
        #state change

        if(not self.attack3Begin):
            self.attack3Begin = True
            self.frame = 0
            self.targetXPosition = boy.x
            self.targetYPosition = boy.landingYPosition + 100

        if(self.frame >= 7):

            if self.curHP > self.hPMax // 2:
                kaiser = KaiserWave(self)
                game_world.add_object(kaiser,1)
                self.attack3Begin = False
                return BehaviorTree.SUCCESS

        elif (self.frame >= 3):
            if self.curHP <= self.hPMax // 2:
                kaiser = KaiserWave(self)
                game_world.add_object(kaiser,1)



        if(int(self.frame) >= Rozen.Images[self.imageState]["Frames"] - 1):
            self.attack3Begin = False
            self.frame = 0
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
        attack2Node = LeafNode("Attack2", self.Attack2)
        attack3Node = LeafNode("Attack3", self.Attack3)

        randomPatternNode = SelectorNode("IceThunderExplosion")


        chase_node = SequenceNode("Chase")
        chase_node.add_children(find_player_node, move_to_player_node)
        chase_node.add_child(randomPatternNode)

        randomPatternNode.add_children(attack2Node,attack1Node)
        randomPatternNode.add_child(attack3Node)

        wander_chase_node = SelectorNode("WanderChase")
        wander_chase_node.add_children(chase_node, wander_node)


        self.bt = BehaviorTree(wander_chase_node)

        #wander_node = LeafNode("Wander", self.wander)
        #self.bt = BehaviorTree(wander_node)
        pass