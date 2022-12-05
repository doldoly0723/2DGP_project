import game_framework
from pico2d import *
import playstate

image = None
MAP_WIDTH, MAP_HEIGHT = 1600, 900
sound = None


def enter():
    global image, press_image, sound
    image = load_image('Sprite/start.png')
    sound = load_music('Sound/start.mp3')
    sound.set_volume(35)
    sound.repeat_play()

def exit():
    sound.stop()
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
                case pico2d.SDLK_RETURN:
                    game_framework.change_state(playstate)
