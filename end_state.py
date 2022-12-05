import game_framework
from pico2d import *
import playstate

image = None
MAP_WIDTH, MAP_HEIGHT = 1600, 900

ending_sound = None
def enter():
    global image, press_image, ending_sound
    image = load_image('Sprite/ending.png')
    ending_sound = load_music('Sound/ending.mp3')
    ending_sound.set_volume(25)
    ending_sound.repeat_play()

def exit():
    ending_sound.stop()
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
                case pico2d.SDLK_ESCAPE: # item_num1
                    game_framework.quit()
                case pico2d.SDLK_SPACE: #item_num2
                    game_framework.change_state(playstate)
