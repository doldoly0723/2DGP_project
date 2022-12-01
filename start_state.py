import game_framework
from pico2d import *
import playstate

image = None
MAP_WIDTH, MAP_HEIGHT = 1600, 900


def enter():
    global image, press_image
    image = load_image('start.png')

def exit():
    global image
    del image

def update():
    pass

def draw():
    image.draw(MAP_WIDTH//2, MAP_HEIGHT//2)
    update_canvas()

def handle_events():
    global item_choose
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            match event.key:
                case pico2d.SDLK_ESCAPE: 
                    game_framework.quit()
                case pico2d.SDLK_SPACE:
                    game_framework.change_state(playstate)
