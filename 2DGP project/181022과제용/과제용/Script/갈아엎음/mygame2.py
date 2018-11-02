import game_framework2
import pico2d

import main_state

pico2d.open_canvas(sync = True)
game_framework2.run(main_state)
pico2d.close_canvas()
