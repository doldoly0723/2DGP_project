import game_framework
from pico2d import *

import playstate


# fill here
# running = True
image = None
MAP_WIDTH, MAP_HEIGHT = 1600, 900

def enter():
    global image, press_image
    image = load_image('Sprite/gameover_state.png')

def exit():
    global image
    del image
    # 아이템 상태 빠져나갈때 초기화

def update():
    pass


def draw():
    image.draw(MAP_WIDTH//2, MAP_HEIGHT//2)
    update_canvas()
    pass

def handle_events():
    global item_choose
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            match event.key:
                case pico2d.SDLK_ESCAPE: # 종료
                    game_framework.quit()
                case pico2d.SDLK_r: # 재시작
                    game_framework.change_state(playstate)


def pause():
    pass

def resume():
    pass



