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







class Charging:

    actions = 2
    charge1,charge2, = range(actions)

    #test = {"ImageFile" : None,"IntervalX" : None,"IntervalY" : None,"Frames" : None}

    Images = []


    Test = True


    for i in range(actions):
        Images.append({"ImageFile": None, "IntervalX": None, "IntervalY": None, "Frames": None, "XRevision": None})


    Images[charge1]["IntervalX"] = 92
    Images[charge1]["IntervalY"] = 90
    Images[charge1]["Frames"] = 10
    Images[charge1]["XRevision"] = 88

    Images[charge2]["IntervalX"] = 24
    Images[charge2]["IntervalY"] = 24
    Images[charge2]["Frames"] = 4
    Images[charge2]["XRevision"] = 19





    def __init__(self,boy):

        if(Charging.Images[Charging.charge1]["ImageFile"] == None):
            Charging.Images[Charging.charge1]["ImageFile"] = load_image('X_Charge_Effect_1.png')

        if(Charging.Images[Charging.charge2]["ImageFile"] == None):
            Charging.Images[Charging.charge2]["ImageFile"] = load_image('middleBusterMoving.png')

        self.kind = game_world.Effect


        self.land = False

        self.x, self.y = boy.x,boy.y


        self.chargingPositionX = PIXEL_PER_METER * boy.chargingPositionX
        self.chargingPositionY = PIXEL_PER_METER * boy.chargingPositionY

        self.dir = clamp(-1,boy.dir,1)
        #self.velocity = velocityX *RUN_SPEED_PPS
        self.frame = 0
        self.event_que = []


        #self.cur_state = BusterProjectile.small

        #self.cur_state.enter(self, None)
        self.imageState = Charging.charge1

        self.collisionRelation = [game_world.EnemyProjectile,game_world.Feature]



        self.selfGravity = False

        self.velocityY = 0






        self.boundingBoxOn = False

        self.tempGravity = 3

        self.startTimer = get_time()
        self.endTimer = 0

        self.subject = boy

    def set_direction(self):



        pass


    def destroy(self):
        game_world.remove_object(self)

        pass



    def update(self):


        self.endTimer = get_time() - self.startTimer


        self.x ,self.y = self.subject.x + self.chargingPositionX ,self.subject.y + self.chargingPositionY


        #self.set_direction()

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % Charging.Images[self.imageState]["Frames"]

        #self.x += self.velocity * self.dir * game_framework.frame_time



        pass


    def draw(self):
        if self.boundingBoxOn:
            self.draw_bb()
        if self.dir == 1:
            Charging.Images[self.imageState]["ImageFile"].clip_composite_draw(int(self.frame) * Charging.Images[self.imageState]["IntervalX"] + Charging.Images[self.imageState]["XRevision"], 0, Charging.Images[self.imageState]["IntervalX"], Charging.Images[self.imageState]["IntervalY"], 0, '', self.x , self.y, Charging.Images[self.imageState]["IntervalX"], Charging.Images[self.imageState]["IntervalY"])
        else:
            Charging.Images[self.imageState]["ImageFile"].clip_composite_draw(int(self.frame) * Charging.Images[self.imageState]["IntervalX"] + Charging.Images[self.imageState]["XRevision"], 0, Charging.Images[self.imageState]["IntervalX"], Charging.Images[self.imageState]["IntervalY"], 0, 'h', self.x , self.y, Charging.Images[self.imageState]["IntervalX"], Charging.Images[self.imageState]["IntervalY"])



    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20
    # fill here

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

