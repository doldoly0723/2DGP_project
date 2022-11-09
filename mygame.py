import game_framework
import pico2d

import playstate

pico2d.open_canvas(playstate.MAP_WIDTH, playstate.MAP_HEIGHT)
game_framework.run(playstate)
pico2d.close_canvas()