from pico2d import *
import game_world
import game_framework
import main_state


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







class TestBack:

    actions = 1
    idle = 0

    #test = {"ImageFile" : None,"IntervalX" : None,"IntervalY" : None,"Frames" : None}

    Images = []


    Test = True


    for i in range(actions):
        Images.append({"ImageFile": None, "IntervalX": None, "IntervalY": None, "Frames": None, "XRevision": None})


    Images[idle]["IntervalX"] = 745
    Images[idle]["IntervalY"] = 600
    Images[idle]["Frames"] = 8
    Images[idle]["XRevision"] = 0




    def __init__(self):

        if(TestBack.Images[TestBack.idle]["ImageFile"] == None):
            TestBack.Images[TestBack.idle]["ImageFile"] = load_image('TestBack3.png')



        self.kind = game_world.Monster

        self.land = False

        self.x, self.y = main_state.screenX //2,300
        self.dir = 1
        #self.velocity = velocityX *RUN_SPEED_PPS
        self.frame = 0
        self.event_que = []


        #self.cur_state = BusterProjectile.small

        #self.cur_state.enter(self, None)
        self.imageState = TestBack.idle

        self.collisionRelation = [game_world.EnemyProjectile,game_world.Feature]



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

        #self.subject = boy



    def set_direction(self):



        pass


    def destroy(self):
        game_world.remove_object(self)

        pass



    def update(self):


        self.endTimer = get_time() - self.startTimer



        #self.set_direction()

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % TestBack.Images[self.imageState]["Frames"]

        #self.x += self.velocity * self.dir * game_framework.frame_time



        pass


    def draw(self):


        TestBack.Images[self.imageState]["ImageFile"].draw(800,300,1600,600)
        if self.boundingBoxOn:
            self.draw_bb()
        #TestBack.Images[self.imageState]["ImageFile"].h = TestBack.Images[self.imageState]["ImageFile"].h * 1.5

        #if self.dir == 1:



            #TestBack.Images[self.imageState]["ImageFile"].clip_composite_draw(int(self.frame) * TestBack.Images[self.imageState]["IntervalX"] + TestBack.Images[self.imageState]["XRevision"], 0, TestBack.Images[self.imageState]["IntervalX"], TestBack.Images[self.imageState]["IntervalY"], 0, '', self.x, self.y, TestBack.Images[self.imageState]["IntervalX"], TestBack.Images[self.imageState]["IntervalY"])
        #else:
            #TestBack.Images[self.imageState]["ImageFile"].clip_composite_draw(int(self.frame) * TestBack.Images[self.imageState]["IntervalX"] + TestBack.Images[self.imageState]["XRevision"], 0, TestBack.Images[self.imageState]["IntervalX"], TestBack.Images[self.imageState]["IntervalY"], 0, 'h', self.x, self.y, TestBack.Images[self.imageState]["IntervalX"], TestBack.Images[self.imageState]["IntervalY"])



    def get_bb(self):
        return self.x - 100 , self.y - 100, self.x + 100, self.y + 100
    # fill here

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

