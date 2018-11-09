import game_framework
import pico2d

import main_state




pico2d.open_canvas(main_state.screenX, main_state.screenY, sync= 60)
game_framework.run(main_state)
pico2d.close_canvas()

#print(최종)

#최종