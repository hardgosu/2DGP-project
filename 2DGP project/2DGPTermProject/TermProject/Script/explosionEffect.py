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







class ExplosionEffect(ObjectBase):

    actions = 1
    basic = 0

    #test = {"ImageFile" : None,"IntervalX" : None,"IntervalY" : None,"Frames" : None}

    Images = []




    for i in range(actions):
        Images.append({"ImageFile": None, "IntervalX": None, "IntervalY": None, "Frames": None, "XRevision": None})


    Images[basic]["IntervalX"] = 100
    Images[basic]["IntervalY"] = 100
    Images[basic]["Frames"] = 20
    Images[basic]["XRevision"] = 0



    spriteSheet = None


    soundKind = 1
    soundExplosion = 0


    sounds = []

    for i in range(soundKind):
        sounds.append({"SoundFile": None,"Volume" : None})

    def __init__(self,x,y,dir,velocityX,imageState):


        if ExplosionEffect.spriteSheet == None:
            ExplosionEffect.spriteSheet = load_image('sprite/ExplosionEffect2.png')
            for i in range(ExplosionEffect.actions):
                ExplosionEffect.Images[i]["ImageFile"] = ExplosionEffect.spriteSheet
                pass

        if(ExplosionEffect.sounds[ExplosionEffect.soundExplosion]["SoundFile"] == None):
            ExplosionEffect.sounds[ExplosionEffect.soundExplosion]["SoundFile"] = load_wav("sound/E_Explosion1.wav")
            ExplosionEffect.sounds[ExplosionEffect.soundExplosion]["Volume"] = 2
            ExplosionEffect.sounds[ExplosionEffect.soundExplosion]["SoundFile"].set_volume(ExplosionEffect.sounds[ExplosionEffect.soundExplosion]["Volume"])



        self.kind = game_world.EffectAttack

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



        #0 is bottom
        self.imageRow = 0
        self.imageRowMax = 2

        ExplosionEffect.sounds[ExplosionEffect.soundExplosion]["SoundFile"].play(1)



    def update(self):


        self.endTimer = get_time() - self.startTimer





        self.set_direction()

        #self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % BusterHitEffect.Images[self.imageState]["Frames"]
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)

        #self.x += self.velocity * self.dir * game_framework.frame_time

        if(self.frame >= ExplosionEffect.Images[self.imageState]["Frames"] //2 ):
            self.imageRow = (self.imageRow + 1) % self.imageRowMax



        if(self.frame >= ExplosionEffect.Images[self.imageState]["Frames"]):
            game_world.remove_object(self)


        pass


    def draw(self):

        if self.dir == 1:

            ExplosionEffect.Images[self.imageState]["ImageFile"].clip_composite_draw(int(self.frame) * ExplosionEffect.Images[self.imageState]["IntervalX"] + ExplosionEffect.Images[self.imageState]["XRevision"], self.imageRow * 100, ExplosionEffect.Images[self.imageState]["IntervalX"], ExplosionEffect.Images[self.imageState]["IntervalY"], 0, '', self.x, self.y, ExplosionEffect.Images[self.imageState]["IntervalX"], ExplosionEffect.Images[self.imageState]["IntervalY"])
        else:
            ExplosionEffect.Images[self.imageState]["ImageFile"].clip_composite_draw(int(self.frame) * ExplosionEffect.Images[self.imageState]["IntervalX"] + ExplosionEffect.Images[self.imageState]["XRevision"], self.imageRow * 100, ExplosionEffect.Images[self.imageState]["IntervalX"], ExplosionEffect.Images[self.imageState]["IntervalY"], 0, 'h', self.x, self.y, ExplosionEffect.Images[self.imageState]["IntervalX"], ExplosionEffect.Images[self.imageState]["IntervalY"])

        if self.boundingBoxOn:
            self.draw_bb()


    def get_bb(self):
        return self.x - 12, self.y - 12, self.x + 12, self.y + 12
    # fill here

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def CollisionHandling(self,object):
        pass

