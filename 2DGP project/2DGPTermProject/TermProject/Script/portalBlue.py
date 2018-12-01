from pico2d import *
import game_world
import game_framework



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







class PortalBlue:

    actions = 1
    charge1 = 0

    #test = {"ImageFile" : None,"IntervalX" : None,"IntervalY" : None,"Frames" : None}

    Images = []


    Test = True


    for i in range(actions):
        Images.append({"ImageFile": None, "IntervalX": None, "IntervalY": None, "Frames": None, "XRevision": None,"YRevision": None})


    Images[charge1]["IntervalX"] = 200
    Images[charge1]["IntervalY"] = 200
    Images[charge1]["Frames"] = 7
    Images[charge1]["XRevision"] = 0
    Images[charge1]["YRevision"] = 0




    soundKind = 2
    soundOpen, soundEnter = range(soundKind)

    sounds = []

    for i in range(soundKind):
        sounds.append({"SoundFile": None,"Volume" : None})

    def __init__(self,boy):

        if(PortalBlue.Images[PortalBlue.charge1]["ImageFile"] == None):
            PortalBlue.Images[PortalBlue.charge1]["ImageFile"] = load_image('sprite/PortalBlue.png')

        if(PortalBlue.sounds[PortalBlue.soundEnter]["SoundFile"] == None):
            PortalBlue.sounds[PortalBlue.soundEnter]["SoundFile"] = load_wav("sound/Diablo2PortalEnter.wav")
            PortalBlue.sounds[PortalBlue.soundEnter]["Volume"] = 8
        if(PortalBlue.sounds[PortalBlue.soundOpen]["SoundFile"] == None):
            PortalBlue.sounds[PortalBlue.soundOpen]["SoundFile"] = load_wav("sound/Diablo2PortalOpen.wav")
            PortalBlue.sounds[PortalBlue.soundOpen]["Volume"] = 8



        self.kind = game_world.Effect


        self.land = False

        self.x, self.y = boy.x,boy.y



        self.dir = clamp(-1,boy.dir,1)
        #self.velocity = velocityX *RUN_SPEED_PPS
        self.frame = 0
        self.event_que = []


        #self.cur_state = BusterProjectile.small

        #self.cur_state.enter(self, None)
        self.imageState = PortalBlue.charge1

        self.collisionRelation = [game_world.EnemyProjectile,game_world.Feature]



        self.selfGravity = False

        self.velocityY = 0






        self.boundingBoxOn = False

        self.tempGravity = 3

        self.startTimer = get_time()
        self.endTimer = 0

        self.subject = boy



        self.soundPlayOnce = False


        self.curState = game_framework.stack[-1]


    def set_direction(self):



        pass


    def destroy(self):
        game_world.remove_object(self)

        pass



    def update(self):

        if(not self.soundPlayOnce):
            PortalBlue.sounds[PortalBlue.soundOpen]["SoundFile"].play(1)
            PortalBlue.sounds[PortalBlue.soundOpen]["SoundFile"].set_volume( PortalBlue.sounds[PortalBlue.soundOpen]["Volume"])
            self.soundPlayOnce = True


        self.endTimer = get_time() - self.startTimer


        #self.set_direction()

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % PortalBlue.Images[self.imageState]["Frames"]

        #self.x += self.velocity * self.dir * game_framework.frame_time



        pass


    def draw(self):
        if self.boundingBoxOn:
            self.draw_bb()
        if self.dir == 1:
            PortalBlue.Images[self.imageState]["ImageFile"].clip_composite_draw(int(self.frame) * PortalBlue.Images[self.imageState]["IntervalX"] + PortalBlue.Images[self.imageState]["XRevision"], 0, PortalBlue.Images[self.imageState]["IntervalX"], PortalBlue.Images[self.imageState]["IntervalY"], 0, '', self.x - self.curState.GetBackground().windowLeft, self.y - self.curState.GetBackground().windowBottom, PortalBlue.Images[self.imageState]["IntervalX"], PortalBlue.Images[self.imageState]["IntervalY"])
        else:
            PortalBlue.Images[self.imageState]["ImageFile"].clip_composite_draw(int(self.frame) * PortalBlue.Images[self.imageState]["IntervalX"] + PortalBlue.Images[self.imageState]["XRevision"], 0, PortalBlue.Images[self.imageState]["IntervalX"], PortalBlue.Images[self.imageState]["IntervalY"], 0, 'h', self.x - self.curState.GetBackground().windowLeft, self.y - self.curState.GetBackground().windowBottom, PortalBlue.Images[self.imageState]["IntervalX"], PortalBlue.Images[self.imageState]["IntervalY"])



    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20
    # fill here

    def draw_bb(self):

        left,bottom,right,top = self.get_bb()

        left -= self.curState.GetBackground().windowLeft
        bottom -= self.curState.GetBackground().windowBottom
        right -= self.curState.GetBackground().windowLeft
        top -= self.curState.GetBackground().windowBottom


        draw_rectangle(left,bottom,right,top)


    def SetPosition(self,x,y):


        self.x = x
        self.y = y

        pass