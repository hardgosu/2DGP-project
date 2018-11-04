from pico2d import *
import game_world

class BusterProjectile:

    actions = 4
    charge1,charge2,small,middle,big = range(actions)

    #test = {"ImageFile" : None,"IntervalX" : None,"IntervalY" : None,"Frames" : None}

    Images = []


    Test = True


    for i in range(Boy.actions):
        Boy.Images.append({"ImageFile": None, "IntervalX": None, "IntervalY": None, "Frames": None, "XRevision": None})

    Boy.Images[Boy.idleShot]["ImageFile"] = load_image('X_IdleShot3.png')
    Boy.Images[Boy.idleShot]["IntervalX"] = 63
    Boy.Images[Boy.idleShot]["IntervalY"] = 45
    Boy.Images[Boy.idleShot]["Frames"] = 12
    Boy.Images[Boy.idleShot]["XRevision"] = 50

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

        self.firePositionX = 20
        self.firePositionY = 20




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

        if Boy.Test:


            if event.type == SDL_KEYDOWN and event.key == SDLK_r:
                Boy.TestIndex += 1
            if event.type == SDL_KEYDOWN and event.key == SDLK_t:
                Boy.TestIndex -= 1



            if event.type == SDL_KEYDOWN and event.key == SDLK_q:
                Boy.Images[Boy.TestIndex]["IntervalX"] += 1
                print(Boy.Images[Boy.TestIndex]["IntervalX"])

            if event.type == SDL_KEYDOWN and event.key == SDLK_e:
                Boy.Images[Boy.TestIndex]["IntervalX"] -= 1
                print(Boy.Images[Boy.TestIndex]["IntervalX"])

            if event.type == SDL_KEYDOWN and event.key == SDLK_w:
                Boy.Images[Boy.TestIndex]["XRevision"] -= 1
                print(Boy.Images[Boy.TestIndex]["XRevision"])
            if event.type == SDL_KEYDOWN and event.key == SDLK_s:
                Boy.Images[Boy.TestIndex]["XRevision"] += 1
                print(Boy.Images[Boy.TestIndex]["XRevision"])
            clamp(0,Boy.TestIndex,Boy.actions)


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

