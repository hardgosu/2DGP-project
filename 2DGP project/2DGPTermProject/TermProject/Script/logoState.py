import game_framework
from pico2d import *
import titleState
import stage1

name = "LogoState"
image = None
logo_time = 0.0


def enter():
    global image
    image = load_image('sprite/titleLogo/kpuCredit.png')



def exit():
    global image
    del(image)



def update():
    global logo_time

    if (logo_time > 1.0):
        logo_time = 0
        #game_framework.quit()
        game_framework.push_state(titleState)
    delay(0.01)
    logo_time += 0.01



def draw():
    global image
    clear_canvas()
    image.draw(stage1.screenX//2,stage1.screenY//2,stage1.screenX,stage1.screenY)
    update_canvas()





def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type,event.key) ==(SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
    pass


def pause(): pass


def resume(): pass




