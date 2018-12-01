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
    idle = 0

    #test = {"ImageFile" : None,"IntervalX" : None,"IntervalY" : None,"Frames" : None}

    Images = []


    Test = True


    for i in range(actions):
        Images.append({"ImageFile": None, "IntervalX": None, "IntervalY": None, "Frames": None, "XRevision": None,"YRevision": None})


    Images[idle]["IntervalX"] = 200
    Images[idle]["IntervalY"] = 200
    Images[idle]["Frames"] = 7
    Images[idle]["XRevision"] = 0
    Images[idle]["YRevision"] = 0




    soundKind = 2
    soundOpen, soundEnter = range(soundKind)

    sounds = []

    for i in range(soundKind):
        sounds.append({"SoundFile": None,"Volume" : None})

    def __init__(self,boy):

        if(PortalBlue.Images[PortalBlue.idle]["ImageFile"] == None):
            PortalBlue.Images[PortalBlue.idle]["ImageFile"] = load_image('sprite/PortalBlue.png')

        if(PortalBlue.sounds[PortalBlue.soundEnter]["SoundFile"] == None):
            PortalBlue.sounds[PortalBlue.soundEnter]["SoundFile"] = load_wav("sound/Diablo2PortalEnter.wav")
            PortalBlue.sounds[PortalBlue.soundEnter]["Volume"] = 8
        if(PortalBlue.sounds[PortalBlue.soundOpen]["SoundFile"] == None):
            PortalBlue.sounds[PortalBlue.soundOpen]["SoundFile"] = load_wav("sound/Diablo2PortalOpen.wav")
            PortalBlue.sounds[PortalBlue.soundOpen]["Volume"] = 8



        self.kind = game_world.Portal


        self.land = False


        if boy != None:

            self.x, self.y = boy.x,boy.y
            self.dir = clamp(-1, boy.dir, 1)
        else:
            self.x,self.y = 800,90
            self.dir = clamp(-1,1,1)


        #self.velocity = velocityX *RUN_SPEED_PPS
        self.frame = 0
        self.event_que = []


        #self.cur_state = BusterProjectile.small

        #self.cur_state.enter(self, None)
        self.imageState = PortalBlue.idle

        self.collisionRelation = [game_world.Player]



        self.selfGravity = False

        self.velocityY = 0






        self.boundingBoxOn = True

        self.tempGravity = 3

        self.startTimer = get_time()
        self.endTimer = 0


        self.subject = boy






        self.curState = game_framework.stack[-1]

        PortalBlue.sounds[PortalBlue.soundOpen]["SoundFile"].play(1)
        PortalBlue.sounds[PortalBlue.soundOpen]["SoundFile"].set_volume(PortalBlue.sounds[PortalBlue.soundOpen]["Volume"])



    def set_direction(self):



        pass


    def destroy(self):
        game_world.remove_object(self)

        pass



    def update(self):




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
        return self.x - 50, self.y - 90, self.x + 50, self.y + 40
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

    def CollisionHandling(self,object):

        PortalBlue.sounds[PortalBlue.soundEnter]["SoundFile"].play(1)
        PortalBlue.sounds[PortalBlue.soundEnter]["SoundFile"].set_volume(PortalBlue.sounds[PortalBlue.soundEnter]["Volume"])


        pass