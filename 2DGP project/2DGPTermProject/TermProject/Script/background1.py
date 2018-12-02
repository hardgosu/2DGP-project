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

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8







class Background1:

    actions = 1
    idle = 0

    #test = {"ImageFile" : None,"IntervalX" : None,"IntervalY" : None,"Frames" : None}

    Images = []


    Test = True


    for i in range(actions):
        Images.append({"ImageFile": None, "IntervalX": None, "IntervalY": None, "Frames": None, "XRevision": None, "YRevision" : None})


    Images[idle]["IntervalX"] = 800
    Images[idle]["IntervalY"] = 300
    Images[idle]["Frames"] = 8
    Images[idle]["XRevision"] = 48
    Images[idle]["YRevision"] = 76



    def __init__(self):

        if(Background1.Images[Background1.idle]["ImageFile"] == None):
            Background1.Images[Background1.idle]["ImageFile"] = load_image('sprite/background1.png')



        self.kind = game_world.Feature

        self.land = False


        self.dir = 1
        #self.velocity = velocityX *RUN_SPEED_PPS
        self.frame = 0
        self.event_que = []


        #self.cur_state = BusterProjectile.small

        #self.cur_state.enter(self, None)
        self.imageState = Background1.idle

        self.collisionRelation = []



        self.selfGravity = False

        self.velocityY = 0



        self.boundingBoxOn = True

        self.tempGravity = 3

        self.startTimer = get_time()
        self.endTimer = 0

        #self.subject = boy
        self.scaleX = 3
        self.scaleY = 3

        self.curState = game_framework.stack[-1]


        self.windowLeft = 0
        self.windowBottom = 0

        self.canvasWidth = self.curState.screenX
        self.canvasHeight = self.curState.screenY
        self.x, self.y = self.curState.screenX //2,500

    def SetCenterObject(self, boy):
        self.centerObject = boy



    def set_direction(self):



        pass


    def destroy(self):
        game_world.remove_object(self)

        pass



    def update(self):


        self.endTimer = get_time() - self.startTimer

        self.windowLeft = clamp(0,
                                (int(self.centerObject.x) - self.canvasWidth // 2) // self.scaleX,
                                ((Background1.Images[self.imageState]["IntervalX"] - Background1.Images[self.imageState]["XRevision"]) * self.scaleX - self.curState.screenX) // self.scaleX)

                                #218)
        self.windowBottom = clamp(0,
                                  (int(self.centerObject.y) - self.canvasHeight // 2) // self.scaleY,
                                  #0)
                                  ((Background1.Images[self.imageState]["IntervalY"] - Background1.Images[self.imageState]["YRevision"]) * self.scaleY - self.curState.screenY) // self.scaleY)

        #self.set_direction()

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % Background1.Images[self.imageState]["Frames"]

        #self.x += self.velocity * self.dir * game_framework.frame_time




        pass


    def draw(self):



        if self.boundingBoxOn:
            self.draw_bb()
        #TestBack.Images[self.imageState]["ImageFile"].h = TestBack.Images[self.imageState]["ImageFile"].h * 1.5

        #if self.dir == 1:

        Background1.Images[self.imageState]["ImageFile"].clip_draw_to_origin( self.windowLeft + int(self.frame) * Background1.Images[self.imageState]["IntervalX"] , self.windowBottom, Background1.Images[self.imageState]["IntervalX"], Background1.Images[self.imageState]["IntervalY"] - (Background1.Images[self.imageState]["YRevision"] // self.scaleY),0,0,Background1.Images[self.imageState]["IntervalX"] * self.scaleX, Background1.Images[self.imageState]["IntervalY"] * self.scaleY)
            #Background1.Images[self.imageState]["ImageFile"].clip_composite_draw(int(self.frame) * Background1.Images[self.imageState]["IntervalX"] + Background1.Images[self.imageState]["XRevision"], 0, Background1.Images[self.imageState]["IntervalX"], Background1.Images[self.imageState]["IntervalY"], 0, '', self.x, self.y, Background1.Images[self.imageState]["IntervalX"] * self.scaleX, Background1.Images[self.imageState]["IntervalY"] * self.scaleY)
        #else:
            #Background1.Images[self.imageState]["ImageFile"].clip_composite_draw(int(self.frame) * Background1.Images[self.imageState]["IntervalX"] + Background1.Images[self.imageState]["XRevision"], 0, Background1.Images[self.imageState]["IntervalX"], Background1.Images[self.imageState]["IntervalY"], 0, 'h', self.x, self.y, Background1.Images[self.imageState]["IntervalX"] * self.scaleX, Background1.Images[self.imageState]["IntervalY"] * self.scaleY)



    def get_bb(self):
        return self.x - 100 , self.y - 100, self.x + 100, self.y + 100
    # fill here

    def draw_bb(self):
        if not self.curState.showBoundingBox:
            return
        draw_rectangle(*self.get_bb())

