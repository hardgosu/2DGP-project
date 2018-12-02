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

TIME_PER_ACTION = 0.25
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8










class BusterHitEffect(ObjectBase):

    actions = 3
    middle,big,reflection = range(actions)

    #test = {"ImageFile" : None,"IntervalX" : None,"IntervalY" : None,"Frames" : None}

    Images = []




    for i in range(actions):
        Images.append({"ImageFile": None, "IntervalX": None, "IntervalY": None, "Frames": None, "XRevision": None})


    Images[middle]["IntervalX"] = 100
    Images[middle]["IntervalY"] = 100
    Images[middle]["Frames"] = 5
    Images[middle]["XRevision"] = 0

    Images[big]["IntervalX"] = 100
    Images[big]["IntervalY"] = 100
    Images[big]["Frames"] = 5
    Images[big]["XRevision"] = 0



    Images[reflection]["IntervalX"] = 100
    Images[reflection]["IntervalY"] = 100
    Images[reflection]["Frames"] = 5
    Images[reflection]["XRevision"] = 0

    spriteSheet = None




    soundKind = 1
    soundHit = 0


    sounds = []

    for i in range(soundKind):
        sounds.append({"SoundFile": None,"Volume" : None})


    def __init__(self,x,y,dir,velocityX,imageState):


        if BusterHitEffect.spriteSheet == None:
            BusterHitEffect.spriteSheet = load_image('sprite/X_Buster_Hit_SpriteSheet.png')
            for i in range(BusterHitEffect.actions):
                BusterHitEffect.Images[i]["ImageFile"] = BusterHitEffect.spriteSheet
                pass
        if(BusterHitEffect.sounds[BusterHitEffect.soundHit]["SoundFile"] == None):
            BusterHitEffect.sounds[BusterHitEffect.soundHit]["SoundFile"] = load_wav("sound/E_BusterHit.wav")
            BusterHitEffect.sounds[BusterHitEffect.soundHit]["Volume"] = 3
            BusterHitEffect.sounds[BusterHitEffect.soundHit]["SoundFile"].set_volume(BusterHitEffect.sounds[BusterHitEffect.soundHit]["Volume"])


        self.kind = game_world.Effect

        self.land = False

        self.x, self.y = x, y
        self.dir = clamp(-1,dir,1)

        self.velocity = velocityX *RUN_SPEED_PPS
        self.frame = 0
        self.event_que = []


        #self.cur_state = BusterProjectile.small

        #self.cur_state.enter(self, None)
        self.imageState = imageState

        self.collisionRelation = []



        self.selfGravity = False

        self.velocityY = 0

        self.firePositionX = PIXEL_PER_METER * 0.3
        self.firePositionY = PIXEL_PER_METER * 0.2


        self.x += self.firePositionX
        self.y += self.firePositionY

        self.boundingBoxOn = False

        self.tempGravity = 3

        self.startTimer = get_time()
        self.endTimer = 0

        BusterHitEffect.sounds[BusterHitEffect.soundHit]["SoundFile"].play(1)



        self.curState = game_framework.stack[-1]


    def update(self):


        self.endTimer = get_time() - self.startTimer





        self.set_direction()

        #self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % BusterHitEffect.Images[self.imageState]["Frames"]
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)

        #self.x += self.velocity * self.dir * game_framework.frame_time



        if(self.frame >= BusterHitEffect.Images[self.imageState]["Frames"]):
            game_world.remove_object(self)


        pass


    def draw(self):

        if self.dir == 1:

            BusterHitEffect.Images[self.imageState]["ImageFile"].clip_composite_draw(int(self.frame) * BusterHitEffect.Images[self.imageState]["IntervalX"] + BusterHitEffect.Images[self.imageState]["XRevision"], self.imageState * 100, BusterHitEffect.Images[self.imageState]["IntervalX"], BusterHitEffect.Images[self.imageState]["IntervalY"], 0, '', self.x- self.curState.GetBackground().windowLeft, self.y- self.curState.GetBackground().windowBottom, BusterHitEffect.Images[self.imageState]["IntervalX"], BusterHitEffect.Images[self.imageState]["IntervalY"])
        else:
            BusterHitEffect.Images[self.imageState]["ImageFile"].clip_composite_draw(int(self.frame) * BusterHitEffect.Images[self.imageState]["IntervalX"] + BusterHitEffect.Images[self.imageState]["XRevision"], self.imageState * 100, BusterHitEffect.Images[self.imageState]["IntervalX"], BusterHitEffect.Images[self.imageState]["IntervalY"], 0, 'h', self.x- self.curState.GetBackground().windowLeft, self.y- self.curState.GetBackground().windowBottom, BusterHitEffect.Images[self.imageState]["IntervalX"], BusterHitEffect.Images[self.imageState]["IntervalY"])

        if self.boundingBoxOn:
            self.draw_bb()


    def get_bb(self):
        return self.x - 12, self.y - 12, self.x + 12, self.y + 12
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

