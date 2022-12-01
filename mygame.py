import game_framework
import pico2d

import playstate
import start_state

pico2d.open_canvas(playstate.MAP_WIDTH, playstate.MAP_HEIGHT)
game_framework.run(start_state)
pico2d.close_canvas()