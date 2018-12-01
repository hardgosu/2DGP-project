import game_framework
import pico2d

import main_state
import stage1
import stage2

pico2d.open_canvas(main_state.screenX, main_state.screenY, sync= 60)
game_framework.run(stage1)
pico2d.close_canvas()

#print(최종)

#최종