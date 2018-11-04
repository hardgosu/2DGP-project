from pico2d import *
from ball import Ball

import game_world
import game_framework
import random

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

# Boy Event


RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SLEEP_TIMER, SPACE, LSHIFT, RSHIFT, LSHIFTUP, RSHIFTUP, JUMP_DOWN, JUMP_UP,STANDING_SHOT = range(13)


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
    (SDL_KEYUP, SDLK_d): JUMP_UP


}

# Boy States

class IdleState:
    timer = 0
    frameTime = 0

    accum = 0
    @staticmethod
    def enter(boy,event):




        boy.velocity = 0


        IdleState.timer = get_time()
        IdleState.accum = 0

        boy.imageState = Boy.idle

    @staticmethod
    def exit(boy,event):

        if(event == RSHIFT):
            pass

        if(event == SPACE):
            boy.fire_ball()
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


        if IdleState.accum >= 3:
            boy.add_event(SLEEP_TIMER)


    @staticmethod
    def draw(boy):
        if boy.dir == 1:

            boy.Images[boy.imageState]["ImageFile"].clip_draw(int(boy.frame) * Boy.Images[boy.imageState]["IntervalX"], 0, Boy.Images[boy.imageState]["IntervalX"], Boy.Images[boy.imageState]["IntervalY"], boy.x, boy.y)

        else:
            boy.Images[boy.imageState]["ImageFile"].clip_composite_draw(int(boy.frame) * Boy.Images[boy.imageState]["IntervalX"], 0, Boy.Images[boy.imageState]["IntervalX"], Boy.Images[boy.imageState]["IntervalY"], 0, 'h', boy.x , boy.y, Boy.Images[boy.imageState]["IntervalX"], Boy.Images[boy.imageState]["IntervalY"])


class RunState:

    @staticmethod
    def enter(boy, event):







        boy.imageState = Boy.walking


    @staticmethod
    def exit(boy, event):


        if(event == SPACE):
            boy.fire_ball()
        pass

    @staticmethod
    def do(boy):




        boy.set_direction()

        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % Boy.Images[boy.imageState]["Frames"]
        boy.x += boy.velocity * game_framework.frame_time
        boy.x = clamp(25, boy.x, 1600 - 25)


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


    @staticmethod
    def draw(boy):
        if boy.dir == 1:
            boy.Images[boy.imageState]["ImageFile"].clip_composite_draw(int(boy.frame) * Boy.Images[boy.imageState]["IntervalX"], 0, Boy.Images[boy.imageState]["IntervalX"], Boy.Images[boy.imageState]["IntervalY"], 0, '', boy.x , boy.y, Boy.Images[boy.imageState]["IntervalX"], Boy.Images[boy.imageState]["IntervalY"])

        else:
            #Boy.Images[boy.imageState]["ImageFile"].clip_draw(int(boy.frame) * Boy.Images[boy.imageState]["IntervalX"], 0, Boy.Images[boy.imageState]["IntervalX"], Boy.Images[boy.imageState]["IntervalY"], boy.x, boy.y)
            boy.Images[boy.imageState]["ImageFile"].clip_composite_draw(int(boy.frame) * Boy.Images[boy.imageState]["IntervalX"], 0, Boy.Images[boy.imageState]["IntervalX"], Boy.Images[boy.imageState]["IntervalY"], 0, 'h', boy.x , boy.y, Boy.Images[boy.imageState]["IntervalX"], Boy.Images[boy.imageState]["IntervalY"])


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
    dashSpeed = 5

    @staticmethod
    def enter(boy, event):
        boy.velocity = boy.dir * RUN_SPEED_PPS



        DashState.test = 0
        boy.imageState = Boy.dashStart
    @staticmethod
    def exit(boy, event):
        #boy.x -= boy.velocity * 10

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

        if(DashState.test > 60):
            DashState.exit(boy,None)
            DashState.test = 0
        elif DashState.test < 40:
            boy.imageState = Boy.dash
        elif DashState.test < 60:
            boy.imageState = Boy.dashEnd

        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % Boy.Images[boy.imageState]["Frames"]


        boy.x += boy.velocity * DashState.dashSpeed * game_framework.frame_time
        boy.x = clamp(25, boy.x, 1600 - 25)

    @staticmethod
    def draw(boy):
        if boy.dir == 1:
            boy.Images[boy.imageState]["ImageFile"].clip_composite_draw(int(boy.frame) * Boy.Images[boy.imageState]["IntervalX"], 0, Boy.Images[boy.imageState]["IntervalX"], Boy.Images[boy.imageState]["IntervalY"], 0, '', boy.x , boy.y, Boy.Images[boy.imageState]["IntervalX"], Boy.Images[boy.imageState]["IntervalY"])
        else:
            boy.Images[boy.imageState]["ImageFile"].clip_composite_draw(int(boy.frame) * Boy.Images[boy.imageState]["IntervalX"], 0, Boy.Images[boy.imageState]["IntervalX"], Boy.Images[boy.imageState]["IntervalY"], 0, 'h', boy.x , boy.y, Boy.Images[boy.imageState]["IntervalX"], Boy.Images[boy.imageState]["IntervalY"])


class JumpState:


    #점프 시작 속도
    jumpSpeed = 20 * PIXEL_PER_METER
    #매 시간단위로 감소하는 속력
    decrease = 0.3* PIXEL_PER_METER

    accum = 0
    up = False
    falling = False

    @staticmethod
    def enter(boy,event):



        if(not JumpState.up and not JumpState.falling):
            boy.velocityY = JumpState.jumpSpeed
            JumpState.accum = 0

            boy.frame = 0
            boy.imageState = Boy.jump

        if(event == JUMP_UP):
            if(JumpState.up):
                boy.velocityY = 0

    @staticmethod
    def exit(boy,event):
        pass
    @staticmethod
    def do(boy):


        if(LEFT_KEY_ON_PRESS or RIGHT_KEY_ON_PRESS):

            if(DASH_KEY_ON_PRESS):
                if LeftRightKeylist[-1] == "LEFT_KEY_ON_PRESS":
                    boy.dir = -1
                    boy.velocity = RUN_SPEED_PPS * boy.dir * DashState.dashSpeed


                elif LeftRightKeylist[-1] == "RIGHT_KEY_ON_PRESS":
                    boy.dir = 1
                    boy.velocity = RUN_SPEED_PPS * boy.dir* DashState.dashSpeed


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





        if boy.velocityY > 0:
            JumpState.up = True
            JumpState.falling = False
        elif boy.velocityY < 0:
            JumpState.up = False
            JumpState.falling = True


        #if JumpState.up:
        #    print("Jumping")

        #if JumpState.falling:
        #    print("Falling")

        boy.x += boy.velocity * game_framework.frame_time
        boy.y += boy.velocityY * game_framework.frame_time

        boy.velocityY -= JumpState.decrease


        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % Boy.Images[boy.imageState]["Frames"]


        #착지위치 설정. 당연히 추후에 수정..
        if boy.y < 90:
            boy.y = 90
            boy.cur_state = IdleState
            boy.cur_state.enter(boy,None)
            JumpState.falling = False
            JumpState.up = False

    @staticmethod
    def draw(boy):
        if boy.dir == 1:
            boy.Images[boy.imageState]["ImageFile"].clip_composite_draw(int(boy.frame) * Boy.Images[boy.imageState]["IntervalX"], 0, Boy.Images[boy.imageState]["IntervalX"], Boy.Images[boy.imageState]["IntervalY"], 0, '', boy.x , boy.y, Boy.Images[boy.imageState]["IntervalX"], Boy.Images[boy.imageState]["IntervalY"])
        else:
            boy.Images[boy.imageState]["ImageFile"].clip_composite_draw(int(boy.frame) * Boy.Images[boy.imageState]["IntervalX"], 0, Boy.Images[boy.imageState]["IntervalX"], Boy.Images[boy.imageState]["IntervalY"], 0, 'h', boy.x , boy.y, Boy.Images[boy.imageState]["IntervalX"], Boy.Images[boy.imageState]["IntervalY"])


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
                SPACE: IdleState, LSHIFT : DashState, RSHIFT : DashState, JUMP_DOWN : JumpState},
    RunState: {RIGHT_UP : IdleState, LEFT_UP: IdleState, LEFT_DOWN: RunState, RIGHT_DOWN : RunState,
               SPACE: RunState, LSHIFT : DashState, RSHIFT : DashState, LSHIFTUP:RunState, RSHIFTUP:RunState, JUMP_DOWN : JumpState},

    SleepState:  { LEFT_DOWN: RunState, RIGHT_DOWN :RunState, LEFT_UP: RunState, RIGHT_UP: RunState,SPACE: IdleState},

    DashState: { LEFT_DOWN: IdleState, RIGHT_DOWN :IdleState, LEFT_UP: IdleState, RIGHT_UP: IdleState,LSHIFT : IdleState, RSHIFT : IdleState,LSHIFTUP : IdleState,RSHIFTUP : IdleState},

    JumpState: { JUMP_UP : JumpState}
}



class Boy:

    actions = 7
    idle, walking, dashStart, dash, dashEnd, jump, idleShot =range(actions)

    #test = {"ImageFile" : None,"IntervalX" : None,"IntervalY" : None,"Frames" : None}

    Images = []





    def __init__(self):
        self.kind = game_world.Player

        self.land = False

        self.x, self.y = 1600 // 2, 90
        self.image = load_image('animation_sheet.png')
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.imageState = Boy.idle

        self.collisionRelation = [game_world.EnemyProjectile,game_world.Feature]

        self.font = load_font('ENCR10B.TTF', 16)

        self.selfGravity = False

        self.velocityY = 0


        for i in range(Boy.actions):
            Boy.Images.append({"ImageFile" : None,"IntervalX" : None,"IntervalY" : None,"Frames" : None})

        Boy.Images[Boy.idleShot]["ImageFile"] = load_image('X_IdleShot.png')
        Boy.Images[Boy.idleShot]["IntervalX"] = 70
        Boy.Images[Boy.idleShot]["IntervalY"] = 46
        Boy.Images[Boy.idleShot]["Frames"] = 12



        Boy.Images[Boy.idle]["ImageFile"] = load_image('X_Idle2.png')
        Boy.Images[Boy.idle]["IntervalX"] = 36
        Boy.Images[Boy.idle]["IntervalY"] = 46
        Boy.Images[Boy.idle]["Frames"] = 73

        Boy.Images[Boy.walking]["ImageFile"] = load_image('X_Right_Walking.png')
        Boy.Images[Boy.walking]["IntervalX"] = 71
        Boy.Images[Boy.walking]["IntervalY"] = 47
        Boy.Images[Boy.walking]["Frames"] = 14

        Boy.Images[Boy.dashStart]["ImageFile"] = load_image('X_DashBegin.png')
        Boy.Images[Boy.dashStart]["IntervalX"] = 50
        Boy.Images[Boy.dashStart]["IntervalY"] = 46
        Boy.Images[Boy.dashStart]["Frames"] = 3

        Boy.Images[Boy.dashEnd]["ImageFile"] = load_image('X_DashEnd.png')
        Boy.Images[Boy.dashEnd]["IntervalX"] = 70
        Boy.Images[Boy.dashEnd]["IntervalY"] = 47
        Boy.Images[Boy.dashEnd]["Frames"] = 9

        Boy.Images[Boy.dash]["ImageFile"] = load_image('X_Dash.png')
        Boy.Images[Boy.dash]["IntervalX"] = 70
        Boy.Images[Boy.dash]["IntervalY"] = 46
        Boy.Images[Boy.dash]["Frames"] = 3

        Boy.Images[Boy.jump]["ImageFile"] = load_image('X_jump.png')
        Boy.Images[Boy.jump]["IntervalX"] = 36
        Boy.Images[Boy.jump]["IntervalY"] = 58
        Boy.Images[Boy.jump]["Frames"] = 24





        self.tempGravity = 3

    def set_direction(self):
        if(self.velocity > 0):
            self.dir =  1
        elif(self.velocity <0):
            self.dir = -1


        pass


        pass
    def fire_ball(self):
        ball = Ball(self.x, self.y, self.dir * 3)
        game_world.add_object(ball, 1)
        pass

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



        self.SelfGravity()
        self.cur_state.do(self)




        if len(self.event_que) > 0:
            event = self.event_que.pop()


            self.cur_state.exit(self, event)
            if(event in next_state_table[self.cur_state].keys()):
                print("있는키")
                self.cur_state = next_state_table[self.cur_state][event]
                self.cur_state.enter(self, event)
            else:
                print("없는키")


    def draw(self):
        self.cur_state.draw(self)
        self.draw_bb()
        self.font.draw(self.x - 60, self.y + 50, '(Time: %3.2f)' % get_time(), (255, 255, 0))

    def handle_event(self, event):
        global LEFT_KEY_ON_PRESS,RIGHT_KEY_ON_PRESS,DASH_KEY_ON_PRESS
        if event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            LEFT_KEY_ON_PRESS = True
        if event.type == SDL_KEYUP and event.key == SDLK_LEFT:
            LEFT_KEY_ON_PRESS = False

        if event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            RIGHT_KEY_ON_PRESS = True
        if event.type == SDL_KEYUP and event.key == SDLK_RIGHT:
            RIGHT_KEY_ON_PRESS = False

        if event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            RIGHT_KEY_ON_PRESS = True
        if event.type == SDL_KEYUP and event.key == SDLK_RIGHT:
            RIGHT_KEY_ON_PRESS = False

        if event.type == SDL_KEYDOWN and event.key == SDLK_LSHIFT:
            DASH_KEY_ON_PRESS = True
        if event.type == SDL_KEYUP and event.key == SDLK_LSHIFT:
            DASH_KEY_ON_PRESS = False







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
        return self.x - 10, self.y - 25, self.x + 10, self.y + 25
    # fill here

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

