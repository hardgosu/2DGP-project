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







class GigadeathBullet(ObjectBase):

    actions = 1
    idle = 0

    #test = {"ImageFile" : None,"IntervalX" : None,"IntervalY" : None,"Frames" : None}

    Images = []


    Test = True


    for i in range(actions):
        Images.append({"ImageFile": None, "IntervalX": None, "IntervalY": None, "Frames": None, "XRevision": None,"YRevision": None})


    Images[idle]["IntervalX"] = 100
    Images[idle]["IntervalY"] = 100
    Images[idle]["Frames"] = 4
    Images[idle]["XRevision"] = 0
    Images[idle]["YRevision"] = 0



    soundKind = 1
    soundRun = 0
    #soundRun = range(soundKind)

    sounds = []

    for i in range(soundKind):
        sounds.append({"SoundFile": None,"Volume" : None})








    def __init__(self, subject):

        if(GigadeathBullet.Images[GigadeathBullet.idle]["ImageFile"] == None):
            GigadeathBullet.Images[GigadeathBullet.idle]["ImageFile"] = load_image('sprite/GigadeathBullet.png')


        if(GigadeathBullet.sounds[GigadeathBullet.soundRun]["SoundFile"] == None):
            GigadeathBullet.sounds[GigadeathBullet.soundRun]["SoundFile"] = load_wav("sound/XE_Buster0.wav")
            GigadeathBullet.sounds[GigadeathBullet.soundRun]["Volume"] = 1




        self.kind = game_world.EnemyProjectile

        self.land = False

        self.x, self.y = subject.x, subject.y
        self.dir = clamp(-1, subject.dir, 1)
        self.velocity = subject.busterSpeed * RUN_SPEED_PPS
        self.frame = 0
        self.event_que = []


        #self.cur_state = BusterProjectile.small

        #self.cur_state.enter(self, None)
        self.imageState = GigadeathBullet.idle

        self.collisionRelation = [game_world.Player]



        self.selfGravity = False

        self.velocityY = 0

        self.firePositionX = PIXEL_PER_METER * subject.firePositionX
        self.firePositionY = PIXEL_PER_METER * subject.firePositionY


        self.x += self.firePositionX
        self.y += self.firePositionY

        self.boundingBoxOn = True

        self.tempGravity = 3

        self.startTimer = get_time()
        self.endTimer = 0


        #버스터 충돌효과 이펙트
        self.hitEffect = None
        self.damage = 8


        if(self.imageState == GigadeathBullet.idle):
            GigadeathBullet.sounds[GigadeathBullet.soundRun]["SoundFile"].play(1)
            GigadeathBullet.sounds[GigadeathBullet.soundRun]["SoundFile"].set_volume(GigadeathBullet.sounds[GigadeathBullet.soundRun]["Volume"])



        self.curState = game_framework.stack[-1]
        self.subject = subject

        self.collisionHandlingOn = True

    def set_direction(self):



        pass





    def update(self):


        self.endTimer = get_time() - self.startTimer





        self.set_direction()

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % GigadeathBullet.Images[self.imageState]["Frames"]

        self.x += self.velocity * self.dir * game_framework.frame_time

        if(self.endTimer > 1.2):
            game_world.remove_object(self)


        pass


    def draw(self):
        if self.boundingBoxOn:
            self.draw_bb()
        if self.dir == 1:
            GigadeathBullet.Images[self.imageState]["ImageFile"].clip_composite_draw(int(self.frame) * GigadeathBullet.Images[self.imageState]["IntervalX"] + GigadeathBullet.Images[self.imageState]["XRevision"], 0, GigadeathBullet.Images[self.imageState]["IntervalX"], GigadeathBullet.Images[self.imageState]["IntervalY"], 0, 'h', self.x - self.curState.GetBackground().windowLeft, self.y - self.curState.GetBackground().windowBottom, GigadeathBullet.Images[self.imageState]["IntervalX"], GigadeathBullet.Images[self.imageState]["IntervalY"])
        else:
            GigadeathBullet.Images[self.imageState]["ImageFile"].clip_composite_draw(int(self.frame) * GigadeathBullet.Images[self.imageState]["IntervalX"] + GigadeathBullet.Images[self.imageState]["XRevision"], 0, GigadeathBullet.Images[self.imageState]["IntervalX"], GigadeathBullet.Images[self.imageState]["IntervalY"], 0, '0', self.x - self.curState.GetBackground().windowLeft, self.y - self.curState.GetBackground().windowBottom, GigadeathBullet.Images[self.imageState]["IntervalX"], GigadeathBullet.Images[self.imageState]["IntervalY"])



    def get_bb(self):
        return self.x - 12, self.y - 50, self.x + 12, self.y -30
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

        pass