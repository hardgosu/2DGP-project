import random
import json
import os

from pico2d import *
import game_framework
import game_world
import gameOverState

from boy import Boy
from grass import Grass


from boy import FallingState
from boy import JumpingShotFallingState

from enemyTest import EnemyTest
from busterProjectile import BusterProjectile

from towBeast import TowBeast

from footBoard import FootBoard


from ioriExplosion import IoriExplosion

from background4 import Background4

from gigadeath import Gigadeath

from portalBlue import PortalBlue

from luke import Luke
from rozen import Rozen




screenX = 1600
screenY = 600


name = "Stage3"

boy = None
grass = None


enemyTest = None

background = None

towBeast = None

collisionCount = 0

bgm = None

gigadeath = None


gigadeathLimit = 4
gigadeathTimer = 0
gigadeathTimerSwitch = False



gigadeathLimit2 = 2
gigadeathTimer2 = 0
gigadeathTimerSwitch2 = False


showBoundingBox = False


footBoard = None
footBoard2 = None
footBoard3 = None
footBoard4 = None
footBoard5 = None
footBoard6 = None
footBoard7 = None
footBoard8 = None


footBoardList = []


genPortalTimer = 0
genPortalTimerLimit = 0.5
genPortalSwitch = False


lowestLandingPositionY = 180
deadLineBottom = -1500


#기본 스테이지
def enter():
    global boy, grass , enemyTest , background , towBeast

    global footBoard,footBoard2,footBoard3,footBoard4,footBoard5,footBoard7,footBoard6,footBoard8

    global bgm
    boy = Boy()


    boy.SetPosition(140,600)

    grass = Grass()




    rozen = Rozen()
    rozen.SetPosition(screenX//2,210)

    footBoard = FootBoard()


    footBoard2 = FootBoard()
    footBoard2.SetPosition(500,250)


    footBoard3 = FootBoard()
    footBoard3.SetPosition(300,180)


    footBoard4 = FootBoard()
    footBoard4.SetPosition(1700,180)


    footBoard5 = FootBoard()
    footBoard5.SetPosition(200,350)



    footBoard6= FootBoard()
    footBoard6.SetPosition(800,180)


    footBoard7 = FootBoard()
    footBoard7.SetPosition(1100,300)


    footBoard8 = FootBoard()
    footBoard8.SetPosition(1500,250)




    background = Background4()

    background.SetCenterObject(boy)
    boy.SetBackground(background)






    #순서 중요
    game_world.add_object(background, 0)


    game_world.add_object(grass, 0)



    game_world.add_object(footBoard, 0)
    game_world.add_object(footBoard2, 0)
    game_world.add_object(footBoard3, 0)
    game_world.add_object(footBoard4,0)
    game_world.add_object(footBoard5,0)

    game_world.add_object(footBoard6,0)
    game_world.add_object(footBoard7,0)
    game_world.add_object(footBoard8,0)

    game_world.add_object(boy, 1)



    game_world.add_object(rozen,1)





    bgm = load_music("sound/music/rozenBGM.mp3")

    bgm.repeat_play()
    bgm.set_volume(45)

def exit():
    global boy, grass,background,bgm


    game_world.clear()

    bgm = None

def pause():
    pass


def resume():
    pass



def GenMonster():

    global gigadeathTimer,gigadeathTimerSwitch,gigadeathLimit

    gigadeathCount = 0
    rand = random.randint(0,4)

    for o in game_world.all_objects():
        if type(o) == Gigadeath:
            gigadeathCount += 1
    if gigadeathCount < gigadeathLimit:
        if not gigadeathTimerSwitch :
            gigadeathTimer = get_time()
            gigadeathTimerSwitch = True

        if  get_time() - gigadeathTimer  >= 2:
            gigadeathTimerSwitch = False
            global footBoard3,footBoard2,footBoard4,footBoard8
            while gigadeathCount < gigadeathLimit:
                rand = random.randint(0, 4)
                gigadeath = Gigadeath()
                if rand == 0:
                    gigadeath.SetPosition(random.randint(footBoard3.get_bb()[0],footBoard3.get_bb()[2]),footBoard3.get_bb()[3] + 50)
                elif rand == 1:
                    gigadeath.SetPosition(random.randint(footBoard2.get_bb()[0],footBoard2.get_bb()[2]),footBoard2.get_bb()[3] + 50)
                elif rand == 2:
                    gigadeath.SetPosition(random.randint(footBoard4.get_bb()[0],footBoard4.get_bb()[2]),footBoard4.get_bb()[3] + 50)
                else:
                    gigadeath.SetPosition(random.randint(footBoard8.get_bb()[0],footBoard8.get_bb()[2]),footBoard8.get_bb()[3] + 50)

                game_world.add_object(gigadeath, 1)
                gigadeathCount += 1







    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        else:
            boy.handle_event(event)


def update():

    GenMonster()
    PlayerFallingDeathCheck()



    for game_object in game_world.all_objects():

        game_object.update()

        for game_object_b in game_world.all_objects():

            if(game_object_b != game_object):
                for relation in game_object_b.collisionRelation:
                    if relation == game_object.kind:
                        if (game_object_b.kind == game_world.PlayerProjectile):
                            if (collide(game_object_b, game_object)):
                                game_object_b.CollisionHandling(None)
                                if (game_object.kind == game_world.Monster):
                                    game_object.CollisionHandling(game_object_b)
                        elif (game_object_b.kind == game_world.Feature):
                            if (collide(game_object_b, game_object)):
                                game_object.land = True
                                game_object.landingYPosition = game_object_b.get_bb()[3]
                                if type(game_object) == Boy:
                                    game_object.collisionCount = True

                        elif (game_object_b.kind == game_world.FootBoard):
                            if (BottomAndTopCollide(game_object, game_object_b)):
                                if type(game_object) == Boy:

                                    game_object.land = True
                                    game_object.landingYPosition = game_object_b.get_bb()[3]
                                    game_object.collisionCount = True
                        elif (game_object.kind == game_world.EffectAttack):
                            if (collide(game_object, game_object_b)):
                                if type(game_object_b) == Boy:
                                    game_object_b.CollisionHandling(game_object)
                        elif (game_object_b.kind == game_world.Portal):
                            if (collide(game_object, game_object_b)):
                                game_object_b.CollisionHandling(game_object)
                        elif (game_object_b.kind == game_world.EnemyProjectile):
                            if (collide(game_object,game_object_b)):
                                game_object.CollisionHandling(game_object_b)




        if type(game_object) == Boy:

            if(not game_object.collisionCount):
                game_object.land = False
            game_object.collisionCount = False







def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b:
        return False
    if right_a < left_b:
        return False
    if top_a < bottom_b:
        return False
    if bottom_a > top_b:
        return False
    return True
    # fill here
    pass


def BottomAndTopCollide(a,b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()



    if left_a > right_b:
        return False
    if right_a < left_b:
        return False
    if abs(bottom_a - top_b) <  10:

        return True

    return False

    pass


def get_boy():
    return boy
def GetBackground():
    return background


def ChangeState():
    game_framework.change_state(gameOverState)


def GenPortal():
    global genPortalSwitch,genPortalTimer,genPortalTimerLimit

    if not genPortalSwitch:
        return False

    genPortalTimer = get_time()

    while get_time() - genPortalTimer < 1.0:
        yield False

    else:
        genPortalSwitch = False
        yield True



def PlayerFallingDeathCheck():
    global deadLineBottom
    if(boy.y < deadLineBottom):
        boy.SetPosition(screenX//2,screenY + 100)