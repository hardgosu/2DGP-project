import game_framework
import pico2d
import logoState

import stage1
import stage2
import stage3

pico2d.open_canvas(stage1.screenX, stage1.screenY, sync= 60)
game_framework.run(stage3)
pico2d.close_canvas()



#print(최종)

#최종