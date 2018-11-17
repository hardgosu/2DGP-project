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







class BusterProjectile:

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




    def __init__(self,x,y,dir,velocityX,imageState):

        if(BusterProjectile.Images[BusterProjectile.middleStart]["ImageFile"] == None):
            BusterProjectile.Images[BusterProjectile.middleStart]["ImageFile"] = load_image('middleBuster.png')

        if(BusterProjectile.Images[BusterProjectile.middle]["ImageFile"] == None):
            BusterProjectile.Images[BusterProjectile.middle]["ImageFile"] = load_image('middleBusterMoving.png')

        if(BusterProjectile.Images[BusterProjectile.big]["ImageFile"] == None):
            BusterProjectile.Images[BusterProjectile.big]["ImageFile"] = load_image('X_Big_Buster.png')





        self.kind = game_world.PlayerProjectile

        self.land = False

        self.x, self.y = x, y
        self.dir = clamp(-1,dir,1)
        self.velocity = velocityX *RUN_SPEED_PPS
        self.frame = 0
        self.event_que = []


        #self.cur_state = BusterProjectile.small

        #self.cur_state.enter(self, None)
        self.imageState = imageState

        self.collisionRelation = [game_world.Monster,game_world.Feature]



        self.selfGravity = False

        self.velocityY = 0

        self.firePositionX = PIXEL_PER_METER * 0.3
        self.firePositionY = PIXEL_PER_METER * 0.2


        self.x += self.firePositionX
        self.y += self.firePositionY

        self.boundingBoxOn = True

        self.tempGravity = 3

        self.startTimer = get_time()
        self.endTimer = 0

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
            BusterProjectile.Images[self.imageState]["ImageFile"].clip_composite_draw(int(self.frame) * BusterProjectile.Images[self.imageState]["IntervalX"] + BusterProjectile.Images[self.imageState]["XRevision"], 0, BusterProjectile.Images[self.imageState]["IntervalX"], BusterProjectile.Images[self.imageState]["IntervalY"], 0, '', self.x , self.y, BusterProjectile.Images[self.imageState]["IntervalX"], BusterProjectile.Images[self.imageState]["IntervalY"])
        else:
            BusterProjectile.Images[self.imageState]["ImageFile"].clip_composite_draw(int(self.frame) * BusterProjectile.Images[self.imageState]["IntervalX"] + BusterProjectile.Images[self.imageState]["XRevision"], 0, BusterProjectile.Images[self.imageState]["IntervalX"], BusterProjectile.Images[self.imageState]["IntervalY"], 0, 'h', self.x , self.y, BusterProjectile.Images[self.imageState]["IntervalX"], BusterProjectile.Images[self.imageState]["IntervalY"])



    def get_bb(self):
        return self.x - 12, self.y - 12, self.x + 12, self.y + 12
    # fill here

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

