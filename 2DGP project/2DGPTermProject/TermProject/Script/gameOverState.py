import game_framework
from pico2d import *

import random
import titleState


name = "GameOverState"
image = None
font = None
blackImage = None
opacity = 1

def enter():
    global  image, font,blackImage
    image = load_image('sprite/titleLogo/gameOver.png')
    blackImage = load_image('sprite/titleLogo/black.png')
    font = load_font('ENCR10B.TTF')

def exit():
    global  image
    del(image)


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type,event.key) ==(SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(titleState)

def draw():
    global opacity
    clear_canvas()
    image.draw(titleState.screenX // 2,titleState.screenY // 2, titleState.screenX, titleState.screenY)
    if(opacity>0):
        blackImage.clip_draw(0,0,800, 800,titleState.screenX // 2,titleState.screenY // 2 ,titleState.screenX, titleState.screenY)
    blackImage.opacify(0)
    if(opacity > 0):
        opacity -= 0.1

    font.draw(titleState.screenX // 2 * 0.7, titleState.screenY * 0.2, 'Press Space Button To TitleScreen', (random.randint(222, 255), random.randint(155, 255), random.randint(255, 255)))
    update_canvas()








def update():
    pass


def pause():
    pass


def resume():
    pass






