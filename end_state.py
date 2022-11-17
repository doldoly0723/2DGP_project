import game_framework
from pico2d import *

import isaac
import playstate
import attack
import monstro


# fill here
# running = True
image = None
MAP_WIDTH, MAP_HEIGHT = 1600, 900

def enter():
    global image, press_image
    image = load_image('gameover_state.png')

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
                case pico2d.SDLK_ESCAPE: # item_num1
                    game_framework.quit()
                case pico2d.SDLK_r: #item_num2
                    isaac.kill_cnt = 0
                    isaac.boss_kill_cnt = 0
                    isaac.body_RL = False
                    isaac.body_UD = False

                    attack.attack_on = False
                    attack.body_dir = 0
                    attack.attack_cnt = 0  # 공격 횟수
                    attack.attack_max = 5
                    attack.attack_damage = 100
                    attack.attack_range = 100
                    attack.attack_size = 40

                    # monster_attack.attack_on = False
                    # monster_attack.body_dir = 0
                    # monster_attack.monster_attack_range = 200
                    # monster_attack.monster_attack_damage = 100


                    playstate.player = None
                    playstate.suckers = None
                    playstate.tears = None
                    playstate.spittys = None
                    playstate.monstros = None
                    playstate.monster_tears = None
                    playstate.boss_1 = False  # stage 1
                    playstate.item_1 = False

                    monstro.monster_tears = None

                    game_framework.change_state(playstate)


def pause():
    pass

def resume():
    pass



