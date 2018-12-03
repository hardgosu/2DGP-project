from pico2d import *
import game_world
import game_framework

from objectBase import ObjectBase
from busterHitEffect import BusterHitEffect

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







class BusterProjectile(ObjectBase):

    actions = 6
    small,middleStart,middle,big,charge1,charge2, = range(actions)

    #test = {"ImageFile" : None,"IntervalX" : None,"IntervalY" : None,"Frames" : None}

    Images = []


    Test = True


    for i in range(actions):
        Images.append({"ImageFile": None, "IntervalX": None, "IntervalY": None, "Frames": None, "XRevision": None})


    Images[middle]["IntervalX"] = 24
    Images[middle]["IntervalY"] = 14
    Images[middle]["Frames"] = 4
    Images[middle]["XRevision"] = 25

    Images[middleStart]["IntervalX"] = 24
    Images[middleStart]["IntervalY"] = 24
    Images[middleStart]["Frames"] = 4
    Images[middleStart]["XRevision"] = 19



    Images[big]["IntervalX"] = 62
    Images[big]["IntervalY"] = 30
    Images[big]["Frames"] = 3
    Images[big]["XRevision"] = 62


    soundKind = 2
    soundMiddle,soundBig = range(soundKind)

    sounds = []

    for i in range(soundKind):
        sounds.append({"SoundFile": None,"Volume" : None})








    def __init__(self,boy,imageState):

        if(BusterProjectile.Images[BusterProjectile.middleStart]["ImageFile"] == None):
            BusterProjectile.Images[BusterProjectile.middleStart]["ImageFile"] = load_image('sprite/middleBuster.png')

        if(BusterProjectile.Images[BusterProjectile.middle]["ImageFile"] == None):
            BusterProjectile.Images[BusterProjectile.middle]["ImageFile"] = load_image('sprite/middleBusterMoving.png')

        if(BusterProjectile.Images[BusterProjectile.big]["ImageFile"] == None):
            BusterProjectile.Images[BusterProjectile.big]["ImageFile"] = load_image('sprite/X_Big_Buster.png')

        if(BusterProjectile.sounds[BusterProjectile.soundMiddle]["SoundFile"] == None):
            BusterProjectile.sounds[BusterProjectile.soundMiddle]["SoundFile"] = load_wav("sound/XE_Buster0.wav")
            BusterProjectile.sounds[BusterProjectile.soundMiddle]["Volume"] = 5
        if(BusterProjectile.sounds[BusterProjectile.soundBig]["SoundFile"] == None):
            BusterProjectile.sounds[BusterProjectile.soundBig]["SoundFile"] = load_wav("sound/XE_Buster2.wav")
            BusterProjectile.sounds[BusterProjectile.soundBig]["Volume"] = 5



        self.kind = game_world.PlayerProjectile

        self.land = False

        self.x, self.y = boy.x, boy.y
        self.dir = clamp(-1,boy.dir,1)
        self.velocity = boy.busterSpeed *RUN_SPEED_PPS
        self.frame = 0
        self.event_que = []


        #self.cur_state = BusterProjectile.small

        #self.cur_state.enter(self, None)
        self.imageState = imageState

        self.collisionRelation = [game_world.Monster]



        self.selfGravity = False

        self.velocityY = 0

        self.firePositionX = PIXEL_PER_METER * boy.firePositionX
        self.firePositionY = PIXEL_PER_METER * boy.firePositionY


        self.x += self.firePositionX
        self.y += self.firePositionY

        self.boundingBoxOn = True

        self.tempGravity = 3

        self.startTimer = get_time()
        self.endTimer = 0


        #버스터 충돌효과 이펙트
        self.hitEffect = None
        self.damage = 4

        if(self.imageState == BusterProjectile.big):
            self.damage *=5

        if(self.imageState == BusterProjectile.middle):
            BusterProjectile.sounds[BusterProjectile.soundMiddle]["SoundFile"].play(1)
            BusterProjectile.sounds[BusterProjectile.soundMiddle]["SoundFile"].set_volume(BusterProjectile.sounds[BusterProjectile.soundMiddle]["Volume"])


        elif(self.imageState == BusterProjectile.big):
            BusterProjectile.sounds[BusterProjectile.soundBig]["SoundFile"].play(1)
            BusterProjectile.sounds[BusterProjectile.soundBig]["SoundFile"].set_volume(BusterProjectile.sounds[BusterProjectile.soundMiddle]["Volume"])


        self.curState = game_framework.stack[-1]
        self.subject = boy

        self.collisionHandlingOn = True

    def set_direction(self):



        pass





    def update(self):


        self.endTimer = get_time() - self.startTimer





        self.set_direction()

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % BusterProjectile.Images[self.imageState]["Frames"]

        self.x += self.velocity * self.dir * game_framework.frame_time

        if(self.endTimer > 1.2):
            game_world.remove_object(self)


        pass


    def draw(self):
        if self.boundingBoxOn:
            self.draw_bb()
        if self.dir == 1:
            BusterProjectile.Images[self.imageState]["ImageFile"].clip_composite_draw(int(self.frame) * BusterProjectile.Images[self.imageState]["IntervalX"] + BusterProjectile.Images[self.imageState]["XRevision"], 0, BusterProjectile.Images[self.imageState]["IntervalX"], BusterProjectile.Images[self.imageState]["IntervalY"], 0, '', self.x  - self.curState.GetBackground().windowLeft, self.y - self.curState.GetBackground().windowBottom, BusterProjectile.Images[self.imageState]["IntervalX"], BusterProjectile.Images[self.imageState]["IntervalY"])
        else:
            BusterProjectile.Images[self.imageState]["ImageFile"].clip_composite_draw(int(self.frame) * BusterProjectile.Images[self.imageState]["IntervalX"] + BusterProjectile.Images[self.imageState]["XRevision"], 0, BusterProjectile.Images[self.imageState]["IntervalX"], BusterProjectile.Images[self.imageState]["IntervalY"], 0, 'h', self.x  - self.curState.GetBackground().windowLeft, self.y - self.curState.GetBackground().windowBottom, BusterProjectile.Images[self.imageState]["IntervalX"], BusterProjectile.Images[self.imageState]["IntervalY"])



    def get_bb(self):
        return self.x - 12, self.y - 12, self.x + 12, self.y + 12
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



    def CollisionHandling(self,object):

        busterHitEffect = BusterHitEffect(self.x,self.y,self.dir,self.velocity,2)
        game_world.add_object(busterHitEffect, 1)
        self.subject.AddBoosterGauge(1)
        game_world.remove_object(self)


