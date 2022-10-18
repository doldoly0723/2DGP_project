import pico2d

import isaac
import monster

pico2d.open_canvas(isaac.MAP_WIDTH,isaac.MAP_HEIGHT)

isaac.enter()

while isaac.running:
    isaac.handle_events()
    isaac.update()
    isaac.draw()
isaac.exit()

pico2d.clear_canvas()