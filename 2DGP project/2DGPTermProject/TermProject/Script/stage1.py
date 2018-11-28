import random
import json
import os

from pico2d import *
import game_framework
import game_world

from boy import Boy
from grass import Grass
from ball import Ball
from testBack import TestBack

from boy import FallingState
from boy import JumpingShotFallingState

from enemyTest import EnemyTest
from busterProjectile import BusterProjectile

from towBeast import TowBeast

from footBoard import FootBoard


from ioriExplosion import IoriExplosion

screenX = 1600
screenY = 600


name = "MainState"

boy = None
grass = None


enemyTest = None

backGround = None


collisionCount = 0



#기본 스테이지
def enter():
    global boy, grass , enemyTest , testBack
    boy = Boy()
    grass = Grass()
    enemyTest = EnemyTest()
    testBack = TestBack()
    towBeast = TowBeast()


    footBoard = FootBoard()

    footBoard2 = FootBoard()
    footBoard2.SetPosition(500,300)

    footBoard3 = FootBoard()
    footBoard3.SetPosition(300,180)


    ioriExplosion = IoriExplosion(towBeast.x,towBeast.y,towBeast.dir,100)



    game_world.add_object(testBack,0)

    game_world.add_object(grass, 0)

    game_world.add_object(footBoard, 0)
    game_world.add_object(footBoard2, 0)
    game_world.add_object(footBoard3, 0)


    game_world.add_object(boy, 1)
    game_world.add_object(enemyTest,1)
    game_world.add_object(towBeast,1)

    game_world.add_object(ioriExplosion,1)

def exit():
    global boy, grass
    del boy
    del grass
    game_world.clear()

def pause():
    pass


def resume():
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
    if abs(bottom_a - top_b) < 10:
        return True

    return False

    pass


def get_boy():
    return boy
