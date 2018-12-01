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







class KaiserWave(ObjectBase):

    actions = 1
    idle = 0

    #test = {"ImageFile" : None,"IntervalX" : None,"IntervalY" : None,"Frames" : None}

    Images = []


    Test = True


    for i in range(actions):
        Images.append({"ImageFile": None, "IntervalX": None, "IntervalY": None, "Frames": None, "XRevision": None})


    Images[idle]["IntervalX"] = 200
    Images[idle]["IntervalY"] = 200
    Images[idle]["Frames"] = 6
    Images[idle]["XRevision"] = 0




    soundKind = 1
    soundBasic = 0

    sounds = []

    for i in range(soundKind):
        sounds.append({"SoundFile": None,"Volume" : None})








    def __init__(self,boy):


        if(KaiserWave.Images[KaiserWave.idle]["ImageFile"] == None):
            KaiserWave.Images[KaiserWave.idle]["ImageFile"] = load_image('sprite/KaiserWave.png')



        if(KaiserWave.sounds[KaiserWave.soundBasic]["SoundFile"] == None):
            KaiserWave.sounds[KaiserWave.soundBasic]["SoundFile"] = load_wav("sound/XE_Buster0.wav")
            KaiserWave.sounds[KaiserWave.soundBasic]["Volume"] = 5




        self.kind = game_world.EnemyProjectile

        self.land = False

        self.x, self.y = boy.x, boy.y
        self.dir = clamp(-1,boy.dir,1)
        self.velocity = boy.busterSpeed *RUN_SPEED_PPS
        self.frame = 0
        self.event_que = []


        #self.cur_state = BusterProjectile.small

        #self.cur_state.enter(self, None)
        self.imageState = KaiserWave.idle

        self.collisionRelation = [game_world.Player]



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
        self.damage = 20



        if(self.imageState == KaiserWave.idle):
            KaiserWave.sounds[KaiserWave.soundBasic]["SoundFile"].play(1)
            KaiserWave.sounds[KaiserWave.soundBasic]["SoundFile"].set_volume(KaiserWave.sounds[KaiserWave.soundBasic]["Volume"])





        self.curState = game_framework.stack[-1]
        self.subject = boy

        self.collisionHandlingOn = True



    def set_direction(self):



        pass





    def update(self):


        self.endTimer = get_time() - self.startTimer





        self.set_direction()

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % KaiserWave.Images[self.imageState]["Frames"]

        self.x += self.velocity * self.dir * game_framework.frame_time

        if(self.endTimer > 1.2):
            game_world.remove_object(self)


        pass


    def draw(self):
        if self.boundingBoxOn:
            self.draw_bb()
        if self.dir == 1:
            KaiserWave.Images[self.imageState]["ImageFile"].clip_composite_draw(int(self.frame) * KaiserWave.Images[self.imageState]["IntervalX"] + KaiserWave.Images[self.imageState]["XRevision"], 0, KaiserWave.Images[self.imageState]["IntervalX"], KaiserWave.Images[self.imageState]["IntervalY"], 0, '', self.x - self.curState.GetBackground().windowLeft, self.y - self.curState.GetBackground().windowBottom, KaiserWave.Images[self.imageState]["IntervalX"], KaiserWave.Images[self.imageState]["IntervalY"])
        else:
            KaiserWave.Images[self.imageState]["ImageFile"].clip_composite_draw(int(self.frame) * KaiserWave.Images[self.imageState]["IntervalX"] + KaiserWave.Images[self.imageState]["XRevision"], 0, KaiserWave.Images[self.imageState]["IntervalX"], KaiserWave.Images[self.imageState]["IntervalY"], 0, 'h', self.x - self.curState.GetBackground().windowLeft, self.y - self.curState.GetBackground().windowBottom, KaiserWave.Images[self.imageState]["IntervalX"], KaiserWave.Images[self.imageState]["IntervalY"])



    def get_bb(self):
        return self.x - 50, self.y - 80, self.x + 50, self.y + 50
    # fill here

    def draw_bb(self):

        left,bottom,right,top = self.get_bb()

        left -= self.curState.GetBackground().windowLeft
        bottom -= self.curState.GetBackground().windowBottom
        right -= self.curState.GetBackground().windowLeft
        top -= self.curState.GetBackground().windowBottom


        draw_rectangle(left,bottom,right,top)



    def CollisionHandling(self,object):

        pass


