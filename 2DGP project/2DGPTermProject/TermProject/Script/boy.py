from pico2d import *
from ball import Ball
from busterProjectile import BusterProjectile
from charging import Charging

import game_world
import game_framework
import random
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


gravity = 9.8


LeftRightKeylist = []
LEFT_KEY_ON_PRESS = False
RIGHT_KEY_ON_PRESS = False
DASH_KEY_ON_PRESS = False
SHOT_KEY_ON_PRESS = False







# Boy Event


RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SLEEP_TIMER, SPACE, LSHIFT, RSHIFT, LSHIFTUP, RSHIFTUP, JUMP_DOWN, JUMP_UP, SHOT_BUTTON,CHARGE_SHOT_BUTTON = range(14)


# fill here

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN,SDLK_SPACE) : SPACE,
    (SDL_KEYDOWN, SDLK_LSHIFT): LSHIFT,
    (SDL_KEYDOWN, SDLK_RSHIFT): RSHIFT,
    (SDL_KEYUP, SDLK_LSHIFT): LSHIFTUP,
    (SDL_KEYUP, SDLK_RSHIFT): RSHIFTUP,
    (SDL_KEYDOWN, SDLK_d) : JUMP_DOWN,
    (SDL_KEYUP, SDLK_d): JUMP_UP,
    (SDL_KEYDOWN, SDLK_a): SHOT_BUTTON

}


#복붙용 베이스 스테이트
class BaseState:


    @staticmethod
    def enter(boy,event):
        pass

    @staticmethod
    def exit(boy,event):
        pass
    @staticmethod
    def do(boy):
        pass
        #boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % Boy.Images[boy.imageState]["Frames"]

    @staticmethod
    def draw(boy):

        cx, cy = boy.x - boy.background.windowLeft, boy.y - boy.background.windowBottom

        if boy.dir == 1:
            boy.Images[boy.imageState]["ImageFile"].clip_composite_draw(int(boy.frame) * Boy.Images[boy.imageState]["IntervalX"] + Boy.Images[boy.imageState]["XRevision"], 0, Boy.Images[boy.imageState]["IntervalX"], Boy.Images[boy.imageState]["IntervalY"], 0, '', cx , cy + (0.5 - boy.GetNormalizedPivotY()) * Boy.Images[boy.imageState]["IntervalY"] , int(Boy.Images[boy.imageState]["IntervalX"] * boy.scale), int(Boy.Images[boy.imageState]["IntervalY"] * boy.scale))
        else:
            boy.Images[boy.imageState]["ImageFile"].clip_composite_draw(int(boy.frame) * Boy.Images[boy.imageState]["IntervalX"] + Boy.Images[boy.imageState]["XRevision"], 0, Boy.Images[boy.imageState]["IntervalX"], Boy.Images[boy.imageState]["IntervalY"], 0, 'h', cx, cy + (0.5 - boy.GetNormalizedPivotY()) * Boy.Images[boy.imageState]["IntervalY"], int(Boy.Images[boy.imageState]["IntervalX"] * boy.scale), int(Boy.Images[boy.imageState]["IntervalY"] * boy.scale))

class JumpingShotFallingState:

    decrease = 0.9* PIXEL_PER_METER



    isTimerOn = False
    startTimer = 0

    shotTimer = 0

    landSound = None


    @staticmethod
    def enter(boy,event):

        if JumpingShotFallingState.landSound == None:
            JumpingShotFallingState.landSound = load_wav('sound/XE_Land.wav')
            JumpingShotFallingState.landSound.set_volume(3)

        if(boy.imageState == boy.jump):
            boy.frame = boy.frame * 0.584

        else:
            boy.frame = 0


        boy.imageState = Boy.jumpShotFalling

        if(event == SHOT_BUTTON):
            boy.fire_ball(BusterProjectile.middle)
            JumpingShotFallingState.startTimer = get_time()

            boy.imageState = Boy.jumpShotFallingFlash

            JumpingShotFallingState.isTimerOn = True
        elif(event == CHARGE_SHOT_BUTTON):
            boy.fire_ball(BusterProjectile.big)

            JumpingShotFallingState.startTimer = get_time()

            boy.imageState = Boy.jumpShotFallingFlash

            JumpingShotFallingState.isTimerOn = True






        pass

    @staticmethod
    def exit(boy,event):

        if(event == SHOT_BUTTON):
            boy.fire_ball(BusterProjectile.middle)
            JumpingShotFallingState.startTimer = get_time()

            boy.imageState = Boy.jumpShotFallingFlash

            JumpingShotFallingState.isTimerOn = True
        elif(event == CHARGE_SHOT_BUTTON):
            boy.fire_ball(BusterProjectile.big)

            JumpingShotFallingState.startTimer = get_time()

            boy.imageState = Boy.jumpShotFallingFlash

            JumpingShotFallingState.isTimerOn = True

        pass
    @staticmethod
    def do(boy):


        if(JumpingShotFallingState.isTimerOn):
            JumpingShotFallingState.shotTimer = get_time() - JumpingShotFallingState.startTimer
            if( JumpingShotFallingState.shotTimer > 0.1):
                JumpingShotFallingState.isTimerOn = False

                boy.imageState = Boy.jumpShotFalling

        if(LEFT_KEY_ON_PRESS or RIGHT_KEY_ON_PRESS):

            if(DASH_KEY_ON_PRESS):
                if LeftRightKeylist[-1] == "LEFT_KEY_ON_PRESS":
                    boy.dir = -1
                    boy.velocity = RUN_SPEED_PPS * boy.dir * DashState.dashSpeedModulus


                elif LeftRightKeylist[-1] == "RIGHT_KEY_ON_PRESS":
                    boy.dir = 1
                    boy.velocity = RUN_SPEED_PPS * boy.dir* DashState.dashSpeedModulus


            else:

                if LeftRightKeylist[-1] == "LEFT_KEY_ON_PRESS":
                    boy.velocity = RUN_SPEED_PPS * boy.dir
                    boy.dir = -1
                    boy.velocity = RUN_SPEED_PPS * boy.dir


                elif LeftRightKeylist[-1] == "RIGHT_KEY_ON_PRESS":
                    boy.dir = 1
                    boy.velocity = RUN_SPEED_PPS * boy.dir
        else:
            boy.velocity = 0


        boy.x += boy.velocity * game_framework.frame_time
        boy.y += boy.velocityY * game_framework.frame_time

        boy.velocityY -= JumpState.decrease



        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % Boy.Images[boy.imageState]["Frames"]

        if(int(boy.frame) > 5):
            boy.frame = 6

        if( boy.land):
            if(boy.y <= boy.landingYPosition):
                JumpingShotFallingState.landSound.play(1)
                boy.y = boy.landingYPosition
                boy.cur_state = IdleState
                boy.cur_state.enter(boy,None)


        pass


    @staticmethod
    def draw(boy):

        cx, cy = boy.x - boy.background.windowLeft, boy.y - boy.background.windowBottom

        if boy.dir == 1:
            boy.Images[boy.imageState]["ImageFile"].clip_composite_draw(int(boy.frame) * Boy.Images[boy.imageState]["IntervalX"] + Boy.Images[boy.imageState]["XRevision"], 0, Boy.Images[boy.imageState]["IntervalX"], Boy.Images[boy.imageState]["IntervalY"], 0, '', cx , cy + (0.5 - boy.GetNormalizedPivotY()) * Boy.Images[boy.imageState]["IntervalY"] , int(Boy.Images[boy.imageState]["IntervalX"] * boy.scale), int(Boy.Images[boy.imageState]["IntervalY"] * boy.scale))
        else:
            boy.Images[boy.imageState]["ImageFile"].clip_composite_draw(int(boy.frame) * Boy.Images[boy.imageState]["IntervalX"] + Boy.Images[boy.imageState]["XRevision"], 0, Boy.Images[boy.imageState]["IntervalX"], Boy.Images[boy.imageState]["IntervalY"], 0, 'h', cx, cy + (0.5 - boy.GetNormalizedPivotY()) * Boy.Images[boy.imageState]["IntervalY"], int(Boy.Images[boy.imageState]["IntervalX"] * boy.scale), int(Boy.Images[boy.imageState]["IntervalY"] * boy.scale))


class FallingState:

    decrease = 0.9* PIXEL_PER_METER


    landSound = None

    @staticmethod
    def enter(boy,event):

        if FallingState.landSound == None:
            FallingState.landSound = load_wav('sound/XE_Land.wav')
            FallingState.landSound.set_volume(3)


        if(boy.imageState != boy.jump):
            boy.frame = 17
        boy.imageState = boy.jump

        boy.velocityY = 0

        pass

    @staticmethod
    def exit(boy,event):
        pass
    @staticmethod
    def do(boy):

        if(LEFT_KEY_ON_PRESS or RIGHT_KEY_ON_PRESS):

            if(DASH_KEY_ON_PRESS):
                if LeftRightKeylist[-1] == "LEFT_KEY_ON_PRESS":
                    boy.dir = -1
                    boy.velocity = RUN_SPEED_PPS * boy.dir * DashState.dashSpeedModulus


                elif LeftRightKeylist[-1] == "RIGHT_KEY_ON_PRESS":
                    boy.dir = 1
                    boy.velocity = RUN_SPEED_PPS * boy.dir* DashState.dashSpeedModulus


            else:

                if LeftRightKeylist[-1] == "LEFT_KEY_ON_PRESS":
                    boy.velocity = RUN_SPEED_PPS * boy.dir
                    boy.dir = -1
                    boy.velocity = RUN_SPEED_PPS * boy.dir


                elif LeftRightKeylist[-1] == "RIGHT_KEY_ON_PRESS":
                    boy.dir = 1
                    boy.velocity = RUN_SPEED_PPS * boy.dir
        else:
            boy.velocity = 0


        boy.x += boy.velocity * game_framework.frame_time
        boy.y += boy.velocityY * game_framework.frame_time

        boy.velocityY -= JumpState.decrease

        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % Boy.Images[boy.imageState]["Frames"]

        if(int(boy.frame) > 20):
            boy.frame = 20

        if( boy.land):
            if(boy.y <= boy.landingYPosition):
                FallingState.landSound.play(1)
                boy.y = boy.landingYPosition
                boy.cur_state = IdleState
                boy.cur_state.enter(boy,None)


        pass


    @staticmethod
    def draw(boy):

        cx, cy = boy.x - boy.background.windowLeft, boy.y - boy.background.windowBottom

        if boy.dir == 1:
            boy.Images[boy.imageState]["ImageFile"].clip_composite_draw(int(boy.frame) * Boy.Images[boy.imageState]["IntervalX"] + Boy.Images[boy.imageState]["XRevision"], 0, Boy.Images[boy.imageState]["IntervalX"], Boy.Images[boy.imageState]["IntervalY"], 0, '', cx , cy + (0.5 - boy.GetNormalizedPivotY()) * Boy.Images[boy.imageState]["IntervalY"] , int(Boy.Images[boy.imageState]["IntervalX"] * boy.scale), int(Boy.Images[boy.imageState]["IntervalY"] * boy.scale))
        else:
            boy.Images[boy.imageState]["ImageFile"].clip_composite_draw(int(boy.frame) * Boy.Images[boy.imageState]["IntervalX"] + Boy.Images[boy.imageState]["XRevision"], 0, Boy.Images[boy.imageState]["IntervalX"], Boy.Images[boy.imageState]["IntervalY"], 0, 'h', cx, cy + (0.5 - boy.GetNormalizedPivotY()) * Boy.Images[boy.imageState]["IntervalY"], int(Boy.Images[boy.imageState]["IntervalX"] * boy.scale), int(Boy.Images[boy.imageState]["IntervalY"] * boy.scale))



# Boy States

class IdleState:
    timer = 0
    frameTime = 0

    accum = 0
    @staticmethod
    def enter(boy,event):




        boy.velocity = 0
        boy.velocityY = 0

        IdleState.timer = get_time()
        IdleState.accum = 0

        boy.imageState = Boy.idle

    @staticmethod
    def exit(boy,event):

        if(event == RSHIFT):
            pass
        if(event == SHOT_BUTTON):
            boy.fire_ball(BusterProjectile.middle)

        elif(event == CHARGE_SHOT_BUTTON):
            boy.fire_ball(BusterProjectile.big)


        pass

    @staticmethod
    def do(boy):


        if(RIGHT_KEY_ON_PRESS or LEFT_KEY_ON_PRESS):
            boy.cur_state = RunState
            boy.cur_state.enter(boy,None)



        boy.set_direction()

        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % Boy.Images[boy.imageState]["Frames"]
        IdleState.frameTime = get_time() - IdleState.timer

        IdleState.timer += IdleState.frameTime
        IdleState.accum += IdleState.frameTime

        if(not boy.land or boy.landingYPosition < boy.y):
            boy.cur_state = FallingState
            boy.cur_state.enter(boy,None)



    @staticmethod
    def draw(boy):

        cx, cy = boy.x - boy.background.windowLeft, boy.y - boy.background.windowBottom

        if boy.dir == 1:
            boy.Images[boy.imageState]["ImageFile"].clip_composite_draw(int(boy.frame) * Boy.Images[boy.imageState]["IntervalX"] + Boy.Images[boy.imageState]["XRevision"], 0, Boy.Images[boy.imageState]["IntervalX"], Boy.Images[boy.imageState]["IntervalY"], 0, '', cx , cy + (0.5 - boy.GetNormalizedPivotY()) * Boy.Images[boy.imageState]["IntervalY"] , int(Boy.Images[boy.imageState]["IntervalX"] * boy.scale), int(Boy.Images[boy.imageState]["IntervalY"] * boy.scale))
        else:
            boy.Images[boy.imageState]["ImageFile"].clip_composite_draw(int(boy.frame) * Boy.Images[boy.imageState]["IntervalX"] + Boy.Images[boy.imageState]["XRevision"], 0, Boy.Images[boy.imageState]["IntervalX"], Boy.Images[boy.imageState]["IntervalY"], 0, 'h', cx, cy + (0.5 - boy.GetNormalizedPivotY()) * Boy.Images[boy.imageState]["IntervalY"], int(Boy.Images[boy.imageState]["IntervalX"] * boy.scale), int(Boy.Images[boy.imageState]["IntervalY"] * boy.scale))



class RunState:

    @staticmethod
    def enter(boy, event):







        boy.imageState = Boy.walking


    @staticmethod
    def exit(boy, event):


        if(event == SHOT_BUTTON):
            boy.fire_ball(BusterProjectile.middle)

        elif(event == CHARGE_SHOT_BUTTON):
            boy.fire_ball(BusterProjectile.big)
        pass

    @staticmethod
    def do(boy):




        boy.set_direction()

        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % Boy.Images[boy.imageState]["Frames"]
        boy.x += boy.velocity * game_framework.frame_time
        #boy.x = clamp(25, boy.x, 1600 - 25)


        if(LEFT_KEY_ON_PRESS or RIGHT_KEY_ON_PRESS):
            if LeftRightKeylist[-1] == "LEFT_KEY_ON_PRESS":
                boy.dir = -1

            elif LeftRightKeylist[-1] == "RIGHT_KEY_ON_PRESS":
                boy.dir = 1


        boy.velocity = RUN_SPEED_PPS * boy.dir



        if(boy.velocity == 0):
            boy.cur_state = IdleState
            boy.cur_state.enter(boy,None)

        elif (not (LEFT_KEY_ON_PRESS or RIGHT_KEY_ON_PRESS)):
            boy.cur_state = IdleState
            boy.cur_state.enter(boy, None)
        if boy.land == False:
            boy.cur_state = IdleState
            boy.cur_state.enter(boy,None)




    @staticmethod
    def draw(boy):

        cx, cy = boy.x - boy.background.windowLeft, boy.y - boy.background.windowBottom

        if boy.dir == 1:
            boy.Images[boy.imageState]["ImageFile"].clip_composite_draw(int(boy.frame) * Boy.Images[boy.imageState]["IntervalX"] + Boy.Images[boy.imageState]["XRevision"], 0, Boy.Images[boy.imageState]["IntervalX"], Boy.Images[boy.imageState]["IntervalY"], 0, '', cx , cy + (0.5 - boy.GetNormalizedPivotY()) * Boy.Images[boy.imageState]["IntervalY"] , int(Boy.Images[boy.imageState]["IntervalX"] * boy.scale), int(Boy.Images[boy.imageState]["IntervalY"] * boy.scale))
        else:
            boy.Images[boy.imageState]["ImageFile"].clip_composite_draw(int(boy.frame) * Boy.Images[boy.imageState]["IntervalX"] + Boy.Images[boy.imageState]["XRevision"], 0, Boy.Images[boy.imageState]["IntervalX"], Boy.Images[boy.imageState]["IntervalY"], 0, 'h', cx, cy + (0.5 - boy.GetNormalizedPivotY()) * Boy.Images[boy.imageState]["IntervalY"], int(Boy.Images[boy.imageState]["IntervalX"] * boy.scale), int(Boy.Images[boy.imageState]["IntervalY"] * boy.scale))




class SleepState:
    @staticmethod
    def enter(boy,event):
        boy.frame = 0
    @staticmethod
    def exit(boy,event):
        pass
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
    @staticmethod
    def draw(boy):
        if boy.dir == 1:
            boy.image.clip_composite_draw(int(boy.frame) * 100, 300, 100, 100, 3.141592 / 2, '', boy.x - 25, boy.y - 25, 100, 100)

        else:
            boy.image.clip_composite_draw(int(boy.frame) * 100, 200, 100, 100, -3.141592 / 2, '', boy.x + 25, boy.y - 25, 100, 100)





class DashState:

    test = 0
    level = 0
    dashSpeedModulus = 3

    dashSound = None
    dashEndSound = None

    @staticmethod
    def enter(boy, event):


        if(DashState.dashSound == None):
            DashState.dashSound = load_wav('sound/XE_Dash.wav')
            DashState.dashSound.set_volume(3)
        if(DashState.dashEndSound == None):
            DashState.dashEndSound = load_wav('sound/XE_DashEnd.wav')
            DashState.dashEndSound.set_volume(3)

        DashState.dashSound.play(1)

        boy.velocity = boy.dir * RUN_SPEED_PPS



        DashState.test = 0
        boy.imageState = Boy.dashStart
    @staticmethod
    def exit(boy, event):
        #boy.x -= boy.velocity * 10

        if(event == SHOT_BUTTON):
            boy.fire_ball(BusterProjectile.middle)

        elif(event == CHARGE_SHOT_BUTTON):
            boy.fire_ball(BusterProjectile.big)
        pass


        if(LEFT_KEY_ON_PRESS or RIGHT_KEY_ON_PRESS):
            boy.cur_state = RunState
            if(boy.dir >= 0):
                boy.cur_state.enter(boy, RIGHT_DOWN)
            else:
                boy.cur_state.enter(boy, LEFT_DOWN)


        #대쉬중에 뭔가 다른키가 눌리면 탈출.. 그러나 나중에는 특정키만 누르면 탈출하도록..
        else:
            boy.cur_state = IdleState
            boy.cur_state.enter(boy, event)




        pass

    @staticmethod
    def do(boy):

        boy.set_direction()

        DashState.test +=1

        if(DashState.test > 20):
            DashState.dashEndSound.play(1)
            DashState.exit(boy,None)
            DashState.test = 0

        elif DashState.test < 13:
            boy.imageState = Boy.dash
        elif DashState.test < 20:
            boy.imageState = Boy.dashEnd

        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % Boy.Images[boy.imageState]["Frames"]


        boy.x += boy.velocity * DashState.dashSpeedModulus * game_framework.frame_time
        #boy.x = clamp(25, boy.x, 1600 - 25)

        if boy.land == False:
            boy.cur_state = IdleState
            boy.cur_state.enter(boy,None)

    @staticmethod
    def draw(boy):

        cx, cy = boy.x - boy.background.windowLeft, boy.y - boy.background.windowBottom

        if boy.dir == 1:
            boy.Images[boy.imageState]["ImageFile"].clip_composite_draw(int(boy.frame) * Boy.Images[boy.imageState]["IntervalX"] + Boy.Images[boy.imageState]["XRevision"], 0, Boy.Images[boy.imageState]["IntervalX"], Boy.Images[boy.imageState]["IntervalY"], 0, '', cx , cy + (0.5 - boy.GetNormalizedPivotY()) * Boy.Images[boy.imageState]["IntervalY"] , int(Boy.Images[boy.imageState]["IntervalX"] * boy.scale), int(Boy.Images[boy.imageState]["IntervalY"] * boy.scale))
        else:
            boy.Images[boy.imageState]["ImageFile"].clip_composite_draw(int(boy.frame) * Boy.Images[boy.imageState]["IntervalX"] + Boy.Images[boy.imageState]["XRevision"], 0, Boy.Images[boy.imageState]["IntervalX"], Boy.Images[boy.imageState]["IntervalY"], 0, 'h', cx, cy + (0.5 - boy.GetNormalizedPivotY()) * Boy.Images[boy.imageState]["IntervalY"], int(Boy.Images[boy.imageState]["IntervalX"] * boy.scale), int(Boy.Images[boy.imageState]["IntervalY"] * boy.scale))




class JumpState:


    #점프 시작 속도
    jumpSpeed = 20 * PIXEL_PER_METER
    #매 시간단위로 감소하는 속력
    decrease = 0.9* PIXEL_PER_METER

    accum = 0

    jumpSound = None
    jumpVoice = None

    @staticmethod
    def enter(boy,event):

        if(JumpState.jumpSound == None):
            JumpState.jumpSound = load_wav('sound/XE_Jump.wav')
            JumpState.jumpSound.set_volume(3)
        if(JumpState.jumpVoice == None):
            JumpState.jumpVoice = load_wav('sound/XV_Jump.wav')
            JumpState.jumpVoice.set_volume(3)



        JumpState.jumpSound.play(1)
        if(random.randint(0,1) == 1):
            JumpState.jumpVoice.play(1)


        boy.velocityY = JumpState.jumpSpeed
        JumpState.accum = 0

        boy.frame = 0
        boy.imageState = Boy.jump



    @staticmethod
    def exit(boy,event):

        if(event == SHOT_BUTTON):
            boy.fire_ball(BusterProjectile.middle)
        elif(event == CHARGE_SHOT_BUTTON):
            boy.fire_ball(BusterProjectile.big)



        pass

    @staticmethod
    def do(boy):


        if(LEFT_KEY_ON_PRESS or RIGHT_KEY_ON_PRESS):

            if(DASH_KEY_ON_PRESS):
                if LeftRightKeylist[-1] == "LEFT_KEY_ON_PRESS":
                    boy.dir = -1
                    boy.velocity = RUN_SPEED_PPS * boy.dir * DashState.dashSpeedModulus


                elif LeftRightKeylist[-1] == "RIGHT_KEY_ON_PRESS":
                    boy.dir = 1
                    boy.velocity = RUN_SPEED_PPS * boy.dir* DashState.dashSpeedModulus


            else:

                if LeftRightKeylist[-1] == "LEFT_KEY_ON_PRESS":
                    boy.velocity = RUN_SPEED_PPS * boy.dir
                    boy.dir = -1
                    boy.velocity = RUN_SPEED_PPS * boy.dir


                elif LeftRightKeylist[-1] == "RIGHT_KEY_ON_PRESS":
                    boy.dir = 1
                    boy.velocity = RUN_SPEED_PPS * boy.dir
        else:
            boy.velocity = 0



        if(int(boy.frame) > 20):
            boy.frame = 20


        if boy.velocityY < 0:
            boy.cur_state = FallingState
            boy.cur_state.enter(boy,None)


        #if JumpState.up:
        #    print("Jumping")

        #if JumpState.falling:
        #    print("Falling")

        boy.x += boy.velocity * game_framework.frame_time
        boy.y += boy.velocityY * game_framework.frame_time

        boy.velocityY -= JumpState.decrease


        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % Boy.Images[boy.imageState]["Frames"]
        





    @staticmethod
    def draw(boy):

        cx, cy = boy.x - boy.background.windowLeft, boy.y - boy.background.windowBottom

        if boy.dir == 1:
            boy.Images[boy.imageState]["ImageFile"].clip_composite_draw(int(boy.frame) * Boy.Images[boy.imageState]["IntervalX"] + Boy.Images[boy.imageState]["XRevision"], 0, Boy.Images[boy.imageState]["IntervalX"], Boy.Images[boy.imageState]["IntervalY"], 0, '', cx , cy + (0.5 - boy.GetNormalizedPivotY()) * Boy.Images[boy.imageState]["IntervalY"] , int(Boy.Images[boy.imageState]["IntervalX"] * boy.scale), int(Boy.Images[boy.imageState]["IntervalY"] * boy.scale))
        else:
            boy.Images[boy.imageState]["ImageFile"].clip_composite_draw(int(boy.frame) * Boy.Images[boy.imageState]["IntervalX"] + Boy.Images[boy.imageState]["XRevision"], 0, Boy.Images[boy.imageState]["IntervalX"], Boy.Images[boy.imageState]["IntervalY"], 0, 'h', cx, cy + (0.5 - boy.GetNormalizedPivotY()) * Boy.Images[boy.imageState]["IntervalY"], int(Boy.Images[boy.imageState]["IntervalX"] * boy.scale), int(Boy.Images[boy.imageState]["IntervalY"] * boy.scale))


#복붙용 베이스 스테이트
class IdleShotState:


    @staticmethod
    def enter(boy,event):

        boy.frame = 0

        boy.imageState = boy.idleShot

        pass

    @staticmethod
    def exit(boy,event):

        if(event == SHOT_BUTTON):
            boy.fire_ball(BusterProjectile.middle)

        elif(event == CHARGE_SHOT_BUTTON):
            boy.fire_ball(BusterProjectile.big)
        pass
    @staticmethod
    def do(boy):

        if(boy.frame >= Boy.Images[boy.imageState]["Frames"] - 1):
            boy.cur_state = IdleState
            boy.cur_state.enter(boy,None)


        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % Boy.Images[boy.imageState]["Frames"]



        pass


    @staticmethod
    def draw(boy):

        cx, cy = boy.x - boy.background.windowLeft, boy.y - boy.background.windowBottom

        if boy.dir == 1:
            boy.Images[boy.imageState]["ImageFile"].clip_composite_draw(int(boy.frame) * Boy.Images[boy.imageState]["IntervalX"] + Boy.Images[boy.imageState]["XRevision"], 0, Boy.Images[boy.imageState]["IntervalX"], Boy.Images[boy.imageState]["IntervalY"], 0, '', cx , cy + (0.5 - boy.GetNormalizedPivotY()) * Boy.Images[boy.imageState]["IntervalY"] , int(Boy.Images[boy.imageState]["IntervalX"] * boy.scale), int(Boy.Images[boy.imageState]["IntervalY"] * boy.scale))
        else:
            boy.Images[boy.imageState]["ImageFile"].clip_composite_draw(int(boy.frame) * Boy.Images[boy.imageState]["IntervalX"] + Boy.Images[boy.imageState]["XRevision"], 0, Boy.Images[boy.imageState]["IntervalX"], Boy.Images[boy.imageState]["IntervalY"], 0, 'h', cx, cy + (0.5 - boy.GetNormalizedPivotY()) * Boy.Images[boy.imageState]["IntervalY"], int(Boy.Images[boy.imageState]["IntervalX"] * boy.scale), int(Boy.Images[boy.imageState]["IntervalY"] * boy.scale))




class WalkingShotState:


    startTimer = 0

    shotTimer = 0




    @staticmethod
    def enter(boy,event):

        if(event != SHOT_BUTTON or WalkingShotState.shotTimer == 0):
            boy.frame = 0


        boy.imageState = boy.walkingShot

        WalkingShotState.startTimer = get_time()


        WalkingShotState.shotTimer = 0

        pass

    @staticmethod
    def exit(boy,event):


        if(event == SHOT_BUTTON):
            boy.fire_ball(BusterProjectile.middle)


    @staticmethod
    def do(boy):

        WalkingShotState.shotTimer = get_time() - WalkingShotState.startTimer


        if WalkingShotState.shotTimer >= 0.4:
            boy.cur_state = RunState
            boy.cur_state.enter(boy,None)
            WalkingShotState.shotTimer = 0

        boy.set_direction()

        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % Boy.Images[boy.imageState]["Frames"]
        boy.x += boy.velocity * game_framework.frame_time
        #boy.x = clamp(25, boy.x, 1600 - 25)


        if(LEFT_KEY_ON_PRESS or RIGHT_KEY_ON_PRESS):
            if LeftRightKeylist[-1] == "LEFT_KEY_ON_PRESS":
                boy.dir = -1

            elif LeftRightKeylist[-1] == "RIGHT_KEY_ON_PRESS":
                boy.dir = 1


        boy.velocity = RUN_SPEED_PPS * boy.dir



        if(boy.velocity == 0):
            boy.cur_state = IdleState
            boy.cur_state.enter(boy,None)

        elif (not (LEFT_KEY_ON_PRESS or RIGHT_KEY_ON_PRESS)):
            boy.cur_state = IdleState
            boy.cur_state.enter(boy, None)

        if boy.land == False:
            boy.cur_state = IdleState
            boy.cur_state.enter(boy,None)

        #boy.x += boy.velocity * game_framework.frame_time


        pass
        #boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % Boy.Images[boy.imageState]["Frames"]

    @staticmethod
    def draw(boy):

        cx, cy = boy.x - boy.background.windowLeft, boy.y - boy.background.windowBottom

        if boy.dir == 1:
            boy.Images[boy.imageState]["ImageFile"].clip_composite_draw(int(boy.frame) * Boy.Images[boy.imageState]["IntervalX"] + Boy.Images[boy.imageState]["XRevision"], 0, Boy.Images[boy.imageState]["IntervalX"], Boy.Images[boy.imageState]["IntervalY"], 0, '', cx , cy + (0.5 - boy.GetNormalizedPivotY()) * Boy.Images[boy.imageState]["IntervalY"] , int(Boy.Images[boy.imageState]["IntervalX"] * boy.scale), int(Boy.Images[boy.imageState]["IntervalY"] * boy.scale))
        else:
            boy.Images[boy.imageState]["ImageFile"].clip_composite_draw(int(boy.frame) * Boy.Images[boy.imageState]["IntervalX"] + Boy.Images[boy.imageState]["XRevision"], 0, Boy.Images[boy.imageState]["IntervalX"], Boy.Images[boy.imageState]["IntervalY"], 0, 'h', cx, cy + (0.5 - boy.GetNormalizedPivotY()) * Boy.Images[boy.imageState]["IntervalY"], int(Boy.Images[boy.imageState]["IntervalX"] * boy.scale), int(Boy.Images[boy.imageState]["IntervalY"] * boy.scale))



#복붙용 베이스 스테이트
class JumpingShotState:

    #점프 시작 속도
    jumpSpeed = 20 * PIXEL_PER_METER
    #매 시간단위로 감소하는 속력
    decrease = 0.3* PIXEL_PER_METER



    isTimerOn = False
    startTimer = 0

    shotTimer = 0





    @staticmethod
    def enter(boy,event):


        #프레임 동기화
        boy.frame = boy.frame * 0.5384
        boy.imageState = Boy.jumpShotBegin

        if(event == SHOT_BUTTON):
            boy.fire_ball(BusterProjectile.middle)
            JumpingShotState.startTimer = get_time()

            boy.imageState = Boy.jumpShotBeginFlash

            JumpingShotState.isTimerOn = True
        elif(event == CHARGE_SHOT_BUTTON):
            boy.fire_ball(BusterProjectile.big)

            JumpingShotState.startTimer = get_time()

            boy.imageState = Boy.jumpShotBeginFlash

            JumpingShotState.isTimerOn = True


        pass

    @staticmethod
    def exit(boy,event):

        if(event == SHOT_BUTTON):
            boy.fire_ball(BusterProjectile.middle)
            JumpingShotState.startTimer = get_time()

            boy.imageState = Boy.jumpShotBeginFlash

            JumpingShotState.isTimerOn = True
        elif(event == CHARGE_SHOT_BUTTON):
            boy.fire_ball(BusterProjectile.big)

            JumpingShotState.startTimer = get_time()

            boy.imageState = Boy.jumpShotBeginFlash

            JumpingShotState.isTimerOn = True

        pass
    @staticmethod
    def do(boy):


        if(JumpingShotState.isTimerOn):
            JumpingShotState.shotTimer = get_time() - JumpingShotState.startTimer
            if( JumpingShotState.shotTimer > 0.1):
                JumpingShotState.isTimerOn = False

                boy.imageState = Boy.jumpShotBegin




        if (LEFT_KEY_ON_PRESS or RIGHT_KEY_ON_PRESS):

            if (DASH_KEY_ON_PRESS):
                if LeftRightKeylist[-1] == "LEFT_KEY_ON_PRESS":
                    boy.dir = -1
                    boy.velocity = RUN_SPEED_PPS * boy.dir * DashState.dashSpeedModulus


                elif LeftRightKeylist[-1] == "RIGHT_KEY_ON_PRESS":
                    boy.dir = 1
                    boy.velocity = RUN_SPEED_PPS * boy.dir * DashState.dashSpeedModulus


            else:

                if LeftRightKeylist[-1] == "LEFT_KEY_ON_PRESS":
                    boy.velocity = RUN_SPEED_PPS * boy.dir
                    boy.dir = -1
                    boy.velocity = RUN_SPEED_PPS * boy.dir


                elif LeftRightKeylist[-1] == "RIGHT_KEY_ON_PRESS":
                    boy.dir = 1
                    boy.velocity = RUN_SPEED_PPS * boy.dir
        else:
            boy.velocity = 0


        if boy.velocityY <= 0:
            boy.cur_state = JumpingShotFallingState
            boy.cur_state.enter(boy,None)



        # if JumpState.up:
        #    print("Jumping")

        # if JumpState.falling:
        #    print("Falling")

        boy.x += boy.velocity * game_framework.frame_time
        boy.y += boy.velocityY * game_framework.frame_time

        boy.velocityY -= JumpState.decrease

        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % Boy.Images[boy.imageState]["Frames"]

        # 임시로 프레임 고정




        if (int(boy.frame) > 11):
            boy.frame = 11



        # 착지위치 설정. 당연히 추후에 수정..
        if boy.y < boy.landingYPosition:
            boy.y = boy.landingYPosition
            boy.cur_state = IdleState
            boy.cur_state.enter(boy, None)

        pass


    @staticmethod
    def draw(boy):

        cx, cy = boy.x - boy.background.windowLeft, boy.y - boy.background.windowBottom

        if boy.dir == 1:
            boy.Images[boy.imageState]["ImageFile"].clip_composite_draw(int(boy.frame) * Boy.Images[boy.imageState]["IntervalX"] + Boy.Images[boy.imageState]["XRevision"], 0, Boy.Images[boy.imageState]["IntervalX"], Boy.Images[boy.imageState]["IntervalY"], 0, '', cx , cy + (0.5 - boy.GetNormalizedPivotY()) * Boy.Images[boy.imageState]["IntervalY"] , int(Boy.Images[boy.imageState]["IntervalX"] * boy.scale), int(Boy.Images[boy.imageState]["IntervalY"] * boy.scale))
        else:
            boy.Images[boy.imageState]["ImageFile"].clip_composite_draw(int(boy.frame) * Boy.Images[boy.imageState]["IntervalX"] + Boy.Images[boy.imageState]["XRevision"], 0, Boy.Images[boy.imageState]["IntervalX"], Boy.Images[boy.imageState]["IntervalY"], 0, 'h', cx, cy + (0.5 - boy.GetNormalizedPivotY()) * Boy.Images[boy.imageState]["IntervalY"], int(Boy.Images[boy.imageState]["IntervalX"] * boy.scale), int(Boy.Images[boy.imageState]["IntervalY"] * boy.scale))




#복붙용 베이스 스테이트
class IdleChargeShotState:


    @staticmethod
    def enter(boy,event):

        boy.imageState = Boy.idleChargeShot

        boy.frame = 0

        pass

    @staticmethod
    def exit(boy,event):
        pass
    @staticmethod
    def do(boy):

        if(boy.frame >=Boy.Images[boy.imageState]["Frames"] - 1):
            boy.cur_state = IdleState
            boy.cur_state.enter(boy,None)


        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % Boy.Images[boy.imageState]["Frames"]



        pass
        #boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % Boy.Images[boy.imageState]["Frames"]

    @staticmethod
    def draw(boy):

        cx, cy = boy.x - boy.background.windowLeft, boy.y - boy.background.windowBottom

        if boy.dir == 1:
            boy.Images[boy.imageState]["ImageFile"].clip_composite_draw(int(boy.frame) * Boy.Images[boy.imageState]["IntervalX"] + Boy.Images[boy.imageState]["XRevision"], 0, Boy.Images[boy.imageState]["IntervalX"], Boy.Images[boy.imageState]["IntervalY"], 0, '', cx , cy + (0.5 - boy.GetNormalizedPivotY()) * Boy.Images[boy.imageState]["IntervalY"] , int(Boy.Images[boy.imageState]["IntervalX"] * boy.scale), int(Boy.Images[boy.imageState]["IntervalY"] * boy.scale))
        else:
            boy.Images[boy.imageState]["ImageFile"].clip_composite_draw(int(boy.frame) * Boy.Images[boy.imageState]["IntervalX"] + Boy.Images[boy.imageState]["XRevision"], 0, Boy.Images[boy.imageState]["IntervalX"], Boy.Images[boy.imageState]["IntervalY"], 0, 'h', cx, cy + (0.5 - boy.GetNormalizedPivotY()) * Boy.Images[boy.imageState]["IntervalY"], int(Boy.Images[boy.imageState]["IntervalX"] * boy.scale), int(Boy.Images[boy.imageState]["IntervalY"] * boy.scale))





"""원본

next_state_table = {
# fill here
    IdleState: { RIGHT_UP : RunState, LEFT_UP : RunState, RIGHT_DOWN : RunState, LEFT_DOWN: RunState, SLEEP_TIMER: SleepState,
                 SPACE: IdleState,LSHIFT : IdleState, RSHIFT : IdleState,LSHIFTUP : IdleState,RSHIFTUP : IdleState},
    RunState: { RIGHT_UP : IdleState,LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN : IdleState,
                SPACE: RunState, LSHIFT : DashState, RSHIFT : DashState,LSHIFTUP:RunState,RSHIFTUP:RunState},

    SleepState:  { LEFT_DOWN: RunState, RIGHT_DOWN :RunState, LEFT_UP: RunState, RIGHT_UP: RunState,SPACE: IdleState},

    DashState: { LEFT_DOWN: IdleState, RIGHT_DOWN :IdleState, LEFT_UP: IdleState, RIGHT_UP: IdleState,LSHIFT : IdleState, RSHIFT : IdleState}
}
"""



""" 저장용
next_state_table = {
# fill here
    IdleState: { LEFT_UP : IdleState,RIGHT_UP : IdleState,RIGHT_DOWN : RunState, LEFT_DOWN: RunState, SLEEP_TIMER: SleepState,
                 SPACE: IdleState,LSHIFT : DashState, RSHIFT : DashState},
    RunState: { RIGHT_UP : IdleState,LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN : IdleState,
                SPACE: RunState, LSHIFT : DashState, RSHIFT : DashState,LSHIFTUP:RunState,RSHIFTUP:RunState},

    SleepState:  { LEFT_DOWN: RunState, RIGHT_DOWN :RunState, LEFT_UP: RunState, RIGHT_UP: RunState,SPACE: IdleState},

    DashState: { LEFT_DOWN: IdleState, RIGHT_DOWN :IdleState, LEFT_UP: IdleState, RIGHT_UP: IdleState,LSHIFTUP : RunState, RSHIFTUP : RunState},

    JumpState: {LEFT_UP : RunState}
}
"""

next_state_table = {
# fill here
    IdleState: {RIGHT_UP : RunState, LEFT_UP : RunState, RIGHT_DOWN : RunState, LEFT_DOWN: RunState, SLEEP_TIMER: SleepState,
                SPACE: IdleState, LSHIFT : DashState, RSHIFT : DashState, JUMP_DOWN : JumpState , SHOT_BUTTON : IdleShotState , CHARGE_SHOT_BUTTON : IdleChargeShotState},
    RunState: {RIGHT_UP : IdleState, LEFT_UP: IdleState, LEFT_DOWN: RunState, RIGHT_DOWN : RunState,
               SPACE: RunState, LSHIFT : DashState, RSHIFT : DashState, JUMP_DOWN : JumpState , SHOT_BUTTON : WalkingShotState , CHARGE_SHOT_BUTTON : WalkingShotState},

    DashState: { LEFT_DOWN: IdleState, RIGHT_DOWN :IdleState, LEFT_UP: IdleState, RIGHT_UP: IdleState,LSHIFT : IdleState, RSHIFT : IdleState,LSHIFTUP : IdleState,RSHIFTUP : IdleState},

    JumpState: { JUMP_UP : FallingState , SHOT_BUTTON : JumpingShotState,CHARGE_SHOT_BUTTON : JumpingShotState},

    IdleShotState : {SHOT_BUTTON : IdleShotState,LEFT_DOWN: RunState, RIGHT_DOWN :RunState ,  JUMP_DOWN : JumpState},

    WalkingShotState : {SHOT_BUTTON : WalkingShotState,LSHIFT : DashState, RSHIFT : DashState , JUMP_DOWN : JumpState},

    JumpingShotState : {},

    IdleChargeShotState : { RIGHT_DOWN : RunState, LEFT_DOWN: RunState},

    FallingState : {SHOT_BUTTON : JumpingShotFallingState,CHARGE_SHOT_BUTTON : JumpingShotFallingState},

    JumpingShotFallingState : {}
}



class Boy(ObjectBase):

    actions = 13
    idle, walking, dashStart, dash, dashEnd, jump, idleShot, walkingShot, jumpShotBegin, jumpShotFalling, jumpShotBeginFlash, jumpShotFallingFlash, idleChargeShot =range(actions)

    #test = {"ImageFile" : None,"IntervalX" : None,"IntervalY" : None,"Frames" : None}

    Images = []


    Test = False
    TestIndex = idleChargeShot

    def __init__(self):
        self.kind = game_world.Player




        self.landingYPosition = 90
        self.land = False

        self.x, self.y = 1600 // 2, 200

        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.imageState = Boy.idle

        self.collisionRelation = [game_world.EnemyProjectile,game_world.Feature,game_world.FootBoard]

        self.font = load_font('ENCR10B.TTF', 16)

        self.selfGravity = False

        self.velocityY = 0

        self.firePositionX = 0.4
        self.firePositionY = 0.9

        self.chargingPositionX = 0
        self.chargingPositionY = 0.7

        self.busterSpeed = 7

        self.boundingBoxOn = True

        self.chargeTimeLimit = 0.5

        # 차지샷 관련 필드
        self.canChargeShot = False
        self.chargeStartTimer = 0
        self.chargeTimer = 0
        self.chargeBlocked = False
        self.beginCharge = False

        self.curState = game_framework.stack[-1]

        # 차지 효과 이펙트를 보관한다
        self.charging = None

        self.scale = 1




        for i in range(Boy.actions):
            Boy.Images.append({"ImageFile" : None,"IntervalX" : None,"IntervalY" : None,"Frames" : None , "XRevision" : None , "PivotY" : 0})

        Boy.Images[Boy.idleShot]["ImageFile"] = load_image('X_IdleShot3.png')
        Boy.Images[Boy.idleShot]["IntervalX"] = 63
        Boy.Images[Boy.idleShot]["IntervalY"] = 45
        Boy.Images[Boy.idleShot]["Frames"] = 12
        Boy.Images[Boy.idleShot]["XRevision"] = 51


        Boy.Images[Boy.idle]["ImageFile"] = load_image('X_Idle2.png')
        Boy.Images[Boy.idle]["IntervalX"] = 36
        Boy.Images[Boy.idle]["IntervalY"] = 46
        Boy.Images[Boy.idle]["Frames"] = 73
        Boy.Images[Boy.idle]["XRevision"] = 0


        Boy.Images[Boy.walking]["ImageFile"] = load_image('X_Right_Walking2.png')
        Boy.Images[Boy.walking]["IntervalX"] = 63
        Boy.Images[Boy.walking]["IntervalY"] = 47
        Boy.Images[Boy.walking]["Frames"] = 14
        Boy.Images[Boy.walking]["XRevision"] = 50

        Boy.Images[Boy.dashStart]["ImageFile"] = load_image('X_DashBegin.png')
        Boy.Images[Boy.dashStart]["IntervalX"] = 50
        Boy.Images[Boy.dashStart]["IntervalY"] = 46
        Boy.Images[Boy.dashStart]["Frames"] = 3
        Boy.Images[Boy.dashStart]["XRevision"] = 0


        Boy.Images[Boy.dashEnd]["ImageFile"] = load_image('X_DashEnd.png')
        Boy.Images[Boy.dashEnd]["IntervalX"] = 70
        Boy.Images[Boy.dashEnd]["IntervalY"] = 47
        Boy.Images[Boy.dashEnd]["Frames"] = 9
        Boy.Images[Boy.dashEnd]["XRevision"] = 0


        Boy.Images[Boy.dash]["ImageFile"] = load_image('X_Dash.png')
        Boy.Images[Boy.dash]["IntervalX"] = 70
        Boy.Images[Boy.dash]["IntervalY"] = 46
        Boy.Images[Boy.dash]["Frames"] = 3
        Boy.Images[Boy.dash]["XRevision"] = 0


        Boy.Images[Boy.jump]["ImageFile"] = load_image('X_jump.png')
        Boy.Images[Boy.jump]["IntervalX"] = 36
        Boy.Images[Boy.jump]["IntervalY"] = 58
        Boy.Images[Boy.jump]["Frames"] = 24
        Boy.Images[Boy.jump]["XRevision"] = 0


        Boy.Images[Boy.walkingShot]["ImageFile"] = load_image('X_Walking_Shot3.png')
        Boy.Images[Boy.walkingShot]["IntervalX"] = 63
        Boy.Images[Boy.walkingShot]["IntervalY"] = 47
        Boy.Images[Boy.walkingShot]["Frames"] = 16
        Boy.Images[Boy.walkingShot]["XRevision"] = 48

        Boy.Images[Boy.jumpShotBegin]["ImageFile"] = load_image('X_Jumping_Shot_Begin.png')
        Boy.Images[Boy.jumpShotBegin]["IntervalX"] = 63
        Boy.Images[Boy.jumpShotBegin]["IntervalY"] = 57
        Boy.Images[Boy.jumpShotBegin]["Frames"] = 14
        Boy.Images[Boy.jumpShotBegin]["XRevision"] = 48


        Boy.Images[Boy.jumpShotFalling]["ImageFile"] = load_image('X_Jumping_Shot_Falling.png')
        Boy.Images[Boy.jumpShotFalling]["IntervalX"] = 63
        Boy.Images[Boy.jumpShotFalling]["IntervalY"] = 56
        Boy.Images[Boy.jumpShotFalling]["Frames"] = 7
        Boy.Images[Boy.jumpShotFalling]["XRevision"] = 42


        Boy.Images[Boy.jumpShotBeginFlash]["ImageFile"] = load_image('X_Jumping_Shot_Begin_Flash.png')
        Boy.Images[Boy.jumpShotBeginFlash]["IntervalX"] = 63
        Boy.Images[Boy.jumpShotBeginFlash]["IntervalY"] = 57
        Boy.Images[Boy.jumpShotBeginFlash]["Frames"] = 14
        Boy.Images[Boy.jumpShotBeginFlash]["XRevision"] = 48


        Boy.Images[Boy.jumpShotFallingFlash]["ImageFile"] = load_image('X_Jumping_Shot_Falling_Flash.png')
        Boy.Images[Boy.jumpShotFallingFlash]["IntervalX"] = 63
        Boy.Images[Boy.jumpShotFallingFlash]["IntervalY"] = 56
        Boy.Images[Boy.jumpShotFallingFlash]["Frames"] = 7
        Boy.Images[Boy.jumpShotFallingFlash]["XRevision"] = 42

        Boy.Images[Boy.idleChargeShot]["ImageFile"] = load_image('X_Idle_Charge_Shot2.png')
        Boy.Images[Boy.idleChargeShot]["IntervalX"] = 81
        Boy.Images[Boy.idleChargeShot]["IntervalY"] = 78
        Boy.Images[Boy.idleChargeShot]["Frames"] = 16
        Boy.Images[Boy.idleChargeShot]["XRevision"] = 58
        Boy.Images[Boy.idleChargeShot]["PivotY"] = 7

        self.tempGravity = 3

        self.collisionCount = False

        self.money = 0


    def GetBusterStartPosition(self):


        return 0

    def GetNormalizedPivotY(self):


        return Boy.Images[self.imageState]["PivotY"] / Boy.Images[self.imageState]["IntervalY"]


    def set_direction(self):
        if(self.velocity > 0):
            self.dir =  1
        elif(self.velocity <0):
            self.dir = -1


        pass


    def shot_charging_effect(self):


        self.charging = Charging(self)

        game_world.add_object(self.charging,1)

        pass

    def fire_ball(self,imageState):



        projectile = BusterProjectile(self,imageState)

        game_world.add_object(projectile, 1)

        pass


    def SetBackground(self,background):
        self.background = background

    def SelfGravity(self):
        if(self.selfGravity == False):
            return

        if(self.land == False):
            self.y -= 100 * game_framework.frame_time


    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        #print(LeftRightKeylist.count(LEFT_KEY_ON_PRESS))
        #print(self.cur_state)
        #print(LeftRightKeylist)
        #print(game_world.objects)

        #print(self.land)


        #self.SelfGravity()
        self.cur_state.do(self)

        if(SHOT_KEY_ON_PRESS):
            if(self.beginCharge):
                self.chargeTimer = get_time() - self.chargeStartTimer
                if (self.charging == None):
                    if(self.chargeTimer > self.chargeTimeLimit / 5):
                        self.shot_charging_effect()

                #print("차지중")
                #print(self.chargeTimer)

            elif(not self.beginCharge):
                self.chargeStartTimer = get_time()
                self.beginCharge = True



        elif(not SHOT_KEY_ON_PRESS and self.beginCharge):
            if(self.chargeTimer >= self.chargeTimeLimit):
                self.add_event(CHARGE_SHOT_BUTTON)
            
            #print("차치중아님")
            self.chargeTimer = 0
            self.beginCharge = False
            if(self.charging != None):
                self.charging.destroy()
                self.charging = None


        if len(self.event_que) > 0:
            event = self.event_que.pop()


            self.cur_state.exit(self, event)
            if(event in next_state_table[self.cur_state].keys()):
                self.cur_state = next_state_table[self.cur_state][event]
                self.cur_state.enter(self, event)







    def draw(self):

        self.cur_state.draw(self)

        if(self.boundingBoxOn):
            self.draw_bb()
        self.font.draw(self.x - 60 - self.background.windowLeft, self.y + 50 - self.background.windowBottom, '(money : %d)' % self.money, (0, 255, 255))

    def handle_event(self, event):
        global LEFT_KEY_ON_PRESS,RIGHT_KEY_ON_PRESS,DASH_KEY_ON_PRESS, SHOT_KEY_ON_PRESS

        """""

        if(event.type == SDL_KEYDOWN and event.key == SDLK_q):

            if(self.charging != None):
                self.charging.Images[Charging.charge1]["IntervalX"] += 1
                print(self.charging.Images[Charging.charge1]["IntervalX"])
        if(event.type == SDL_KEYDOWN and event.key == SDLK_w):
            if(self.charging != None):
                self.charging.Images[Charging.charge1]["IntervalX"] -= 1
                print(self.charging.Images[Charging.charge1]["IntervalX"])

        if(event.type == SDL_KEYDOWN and event.key == SDLK_e):

            if(self.charging != None):
                self.charging.Images[Charging.charge1]["XRevision"] += 1
                print(self.charging.Images[Charging.charge1]["XRevision"])
        if(event.type == SDL_KEYDOWN and event.key == SDLK_r):
            if(self.charging != None):
                self.charging.Images[Charging.charge1]["XRevision"] -= 1
                print(self.charging.Images[Charging.charge1]["XRevision"])
        """""



        if event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            LEFT_KEY_ON_PRESS = True
        elif event.type == SDL_KEYUP and event.key == SDLK_LEFT:
            LEFT_KEY_ON_PRESS = False

        elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            RIGHT_KEY_ON_PRESS = True
        elif event.type == SDL_KEYUP and event.key == SDLK_RIGHT:
            RIGHT_KEY_ON_PRESS = False

        elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            RIGHT_KEY_ON_PRESS = True
        elif event.type == SDL_KEYUP and event.key == SDLK_RIGHT:
            RIGHT_KEY_ON_PRESS = False

        elif event.type == SDL_KEYDOWN and event.key == SDLK_LSHIFT:
            DASH_KEY_ON_PRESS = True
        elif event.type == SDL_KEYUP and event.key == SDLK_LSHIFT:
            DASH_KEY_ON_PRESS = False

        elif event.type == SDL_KEYDOWN and event.key == SDLK_a:
            SHOT_KEY_ON_PRESS = True
        elif event.type == SDL_KEYUP and event.key == SDLK_a:
            SHOT_KEY_ON_PRESS = False






        if not "LEFT_KEY_ON_PRESS" in LeftRightKeylist:
            if LEFT_KEY_ON_PRESS == True:
                LeftRightKeylist.append("LEFT_KEY_ON_PRESS")

        if not "RIGHT_KEY_ON_PRESS" in LeftRightKeylist:
            if RIGHT_KEY_ON_PRESS == True:
                LeftRightKeylist.append("RIGHT_KEY_ON_PRESS")



        if "LEFT_KEY_ON_PRESS" in LeftRightKeylist:
            if LEFT_KEY_ON_PRESS == False:
                LeftRightKeylist.remove("LEFT_KEY_ON_PRESS")

        if "RIGHT_KEY_ON_PRESS" in LeftRightKeylist:
            if RIGHT_KEY_ON_PRESS == False:
                LeftRightKeylist.remove("RIGHT_KEY_ON_PRESS")






        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def get_bb(self):
        return self.x - 10,self.y ,self.x  + 10,self.y  + 40

    # fill here

    def draw_bb(self):
        left,bottom,right,top = self.get_bb()

        left -= self.background.windowLeft
        bottom -= self.background.windowBottom
        right -= self.background.windowLeft
        top -= self.background.windowBottom


        draw_rectangle(left,bottom,right,top)

    def SetPosition(self,x,y):
        self.x = x
        self.y = y

    def GetDamage(self):
        pass