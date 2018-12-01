from pico2d import *
import game_world
import game_framework

from objectBase import ObjectBase


# Boy Run Speed
# fill expressions correctly
PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


# Boy Action Speed
# fill expressions correctly

TIME_PER_ACTION = 0.4
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8







class IoriExplosion(ObjectBase):

    actions = 2
    explosion1, explosion2, = range(actions)

    #test = {"ImageFile" : None,"IntervalX" : None,"IntervalY" : None,"Frames" : None}

    Images = []


    Test = True


    for i in range(actions):
        Images.append({"ImageFile": None, "IntervalX": None, "IntervalY": None, "Frames": None, "XRevision": None,"Row" : None,"Column" : None})


    Images[explosion1]["IntervalX"] = 200
    Images[explosion1]["IntervalY"] = 400
    Images[explosion1]["Frames"] = 18
    Images[explosion1]["XRevision"] = 0
    Images[explosion1]["Row"] = 2
    Images[explosion1]["Column"] = 10


    Images[explosion2]["IntervalX"] = 24
    Images[explosion2]["IntervalY"] = 24
    Images[explosion2]["Frames"] = 4
    Images[explosion2]["XRevision"] = 19



    soundKind = 2
    soundExplosion1, soundExplosion2 = range(soundKind)

    sounds = []

    for i in range(soundKind):
        sounds.append({"SoundFile": None,"Volume" : None})

    def __init__(self,x,y,dir,damage):

        if (IoriExplosion.Images[IoriExplosion.explosion1]["ImageFile"] == None):
                IoriExplosion.Images[IoriExplosion.explosion1]["ImageFile"] = load_image('sprite/ioriEffect1.png')

        if (IoriExplosion.Images[IoriExplosion.explosion2]["ImageFile"] == None):
                IoriExplosion.Images[IoriExplosion.explosion2]["ImageFile"] = load_image('sprite/ioriEffect2.png')

        if (IoriExplosion.sounds[IoriExplosion.soundExplosion2]["SoundFile"] == None):
                IoriExplosion.sounds[IoriExplosion.soundExplosion2]["SoundFile"] = load_wav("sound/FireExplosion.wav")
                IoriExplosion.sounds[IoriExplosion.soundExplosion2]["Volume"] = 5
        if (IoriExplosion.sounds[IoriExplosion.soundExplosion1]["SoundFile"] == None):
                IoriExplosion.sounds[IoriExplosion.soundExplosion1]["SoundFile"] = load_wav("sound/FireExplosion2.wav")
                IoriExplosion.sounds[IoriExplosion.soundExplosion1]["Volume"] = 5

        self.kind = game_world.EffectAttack

        self.land = False

        self.x, self.y = x,y



        self.dir = clamp(-1, dir, 1)
        # self.velocity = velocityX *RUN_SPEED_PPS
        self.frame = 0
        self.event_que = []

        # self.cur_state = BusterProjectile.small

        # self.cur_state.enter(self, None)
        self.imageState = IoriExplosion.explosion1

        self.collisionRelation = [game_world.EnemyProjectile, game_world.Feature]

        self.selfGravity = False

        self.velocityY = 0

        self.boundingBoxOn = False

        self.tempGravity = 3

        self.startTimer = get_time()
        self.endTimer = 0



        self.row = IoriExplosion.Images[self.imageState]["Row"] - 1


        IoriExplosion.sounds[IoriExplosion.soundExplosion2]["SoundFile"].play(1)
        IoriExplosion.sounds[IoriExplosion.soundExplosion2]["SoundFile"].set_volume(
            IoriExplosion.sounds[IoriExplosion.soundExplosion2]["Volume"])


        self.check = False
        self.damage = damage


        self.curState = game_framework.stack[-1]

    def set_direction(self):



        pass


    def destroy(self):
        game_world.remove_object(self)

        pass



    def update(self):


        self.endTimer = get_time() - self.startTimer

        #피코투디..Wav의 구간 반복 재생이 안되는것인가..
        """"
        if(self.endTimer >= 2):
            if not IoriExplosion.sounds[IoriExplosion.soundExplosion1]["SoundFile"] == None:
                IoriExplosion.sounds[IoriExplosion.soundExplosion1]["SoundFile"] = None
                IoriExplosion.sounds[IoriExplosion.soundExplosion2]["SoundFile"].repeat_play()
                IoriExplosion.sounds[IoriExplosion.soundExplosion2]["SoundFile"].set_volume(IoriExplosion.sounds[IoriExplosion.soundExplosion2]["Volume"])
        """""
        #self.x ,self.y = self.subject.x + self.chargingPositionX ,self.subject.y + self.chargingPositionY


        #self.set_direction()



        if(int(self.frame) == 0):
            self.row = IoriExplosion.Images[self.imageState]["Row"] - 1


        elif int(self.frame) % IoriExplosion.Images[self.imageState]["Column"]  == 0:
            if(not self.check):
                self.row -= 1
                self.check = True
        else:
            self.check = False


        if(int(self.frame) >= IoriExplosion.Images[self.imageState]["Frames"] - 1):
            self.destroy()



        #self.x += self.velocity * self.dir * game_framework.frame_time

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % IoriExplosion.Images[self.imageState]["Frames"]
        #self.x += self.velocity * self.dir * game_framework.frame_time




        pass


    def draw(self):
        self.boundingBoxOn = True
        if self.boundingBoxOn:
            self.draw_bb()
        if self.dir == 1:
            IoriExplosion.Images[self.imageState]["ImageFile"].clip_composite_draw( ( int(self.frame) % IoriExplosion.Images[self.imageState]["Column"] ) * IoriExplosion.Images[self.imageState]["IntervalX"] + IoriExplosion.Images[self.imageState]["XRevision"], IoriExplosion.Images[self.imageState]["IntervalY"] * self.row, IoriExplosion.Images[self.imageState]["IntervalX"], IoriExplosion.Images[self.imageState]["IntervalY"], 0, '', self.x- self.curState.GetBackground().windowLeft, self.y- self.curState.GetBackground().windowBottom, IoriExplosion.Images[self.imageState]["IntervalX"], IoriExplosion.Images[self.imageState]["IntervalY"])
        else:
            IoriExplosion.Images[self.imageState]["ImageFile"].clip_composite_draw(( int(self.frame) % IoriExplosion.Images[self.imageState]["Column"] )  * IoriExplosion.Images[self.imageState]["IntervalX"] + IoriExplosion.Images[self.imageState]["XRevision"], IoriExplosion.Images[self.imageState]["IntervalY"] * self.row, IoriExplosion.Images[self.imageState]["IntervalX"], IoriExplosion.Images[self.imageState]["IntervalY"], 0, 'h', self.x- self.curState.GetBackground().windowLeft, self.y- self.curState.GetBackground().windowBottom, IoriExplosion.Images[self.imageState]["IntervalX"], IoriExplosion.Images[self.imageState]["IntervalY"])



    def get_bb(self):
        return self.x - 20, self.y - 200, self.x + 30, self.y + 30
    # fill here

    def draw_bb(self):

        left,bottom,right,top = self.get_bb()

        left -= self.curState.GetBackground().windowLeft
        bottom -= self.curState.GetBackground().windowBottom
        right -= self.curState.GetBackground().windowLeft
        top -= self.curState.GetBackground().windowBottom


        draw_rectangle(left,bottom,right,top)

