import game_framework
from pico2d import *

import isaac
import playstate
import random
import attack


# fill here
# running = True
image = None
press_image = None
item_choose = False
item_num1 = None
item_num2 = None
item_num3 = None
item_WEI = 130
item_HIE = 150
item = { 1: 'damege_up', 2: 'range_up', 3: 'max_attack_up', 4: 'heart_up', 5: 'attack_size_up'}
MAP_WIDTH, MAP_HEIGHT = 1600, 900
item_sound = None

def enter():
    global image, press_image, item_sound
    image = load_image('Sprite/item1.png')
    press_image = load_image('Sprite/press_num.png')

    item_sound = load_wav('Sound/item.wav')
    item_sound.set_volume(30)

    # fill here
    pass

def exit():
    global image, item_sound
    del image
    # 아이템 상태 빠져나갈때 초기화
    playstate.player.dir_x = 0
    playstate.player.dir_y = 0
    item_sound.play()
    # fill here
    pass

def update():
    #play_state.update()
    global item_num1,item_num2, item_num3, item_choose
    if item_choose == False:
        item_num1 = random.randint(1, 5)
        item_num2 = random.randint(1, 5)
        while(item_num2 == item_num1):
            item_num2 = random.randint(1, 5)
        item_num3 = random.randint(1, 5)
        while(item_num3 == item_num1 or item_num3 == item_num2):
            item_num3 = random.randint(1, 5)
        item_choose = True


def draw():
    global item_num1, item_num2, item_num3, item_choose
    clear_canvas()
    playstate.draw_world()
    if item_num1 == 1:
        image.clip_draw(item_WEI*1, 500, item_WEI, item_HIE, MAP_WIDTH//3, MAP_HEIGHT//2)
    elif item_num1 == 2:
        image.clip_draw(item_WEI*0, 650, item_WEI, item_HIE, MAP_WIDTH // 3, MAP_HEIGHT // 2)
    elif item_num1 == 3:
        image.clip_draw(item_WEI*3, 650, item_WEI + 40, item_HIE, MAP_WIDTH // 3, MAP_HEIGHT // 2)
    elif item_num1 == 4:
        image.clip_draw(item_WEI*0, 500, item_WEI, item_HIE, MAP_WIDTH // 3, MAP_HEIGHT // 2)
    elif item_num1 == 5:
        image.clip_draw(item_WEI*3, 500, item_WEI+ 40, item_HIE, MAP_WIDTH // 3, MAP_HEIGHT // 2)

    if item_num2 == 1:
        image.clip_draw(item_WEI * 1, 500, item_WEI, item_HIE, MAP_WIDTH // 2, MAP_HEIGHT // 2)
    elif item_num2 == 2:
        image.clip_draw(item_WEI * 0, 650, item_WEI, item_HIE, MAP_WIDTH // 2, MAP_HEIGHT // 2)
    elif item_num2 == 3:
        image.clip_draw(item_WEI * 3, 650, item_WEI + 40, item_HIE, MAP_WIDTH // 2, MAP_HEIGHT // 2)
    elif item_num2 == 4:
        image.clip_draw(item_WEI * 0, 500, item_WEI, item_HIE, MAP_WIDTH // 2, MAP_HEIGHT // 2)
    elif item_num2 == 5:
        image.clip_draw(item_WEI * 3, 500, item_WEI + 40, item_HIE, MAP_WIDTH // 2, MAP_HEIGHT // 2)

    if item_num3 == 1:
        image.clip_draw(item_WEI * 1, 500, item_WEI, item_HIE, MAP_WIDTH // 3 * 2, MAP_HEIGHT // 2)
    elif item_num3 == 2:
        image.clip_draw(item_WEI * 0, 650, item_WEI, item_HIE, MAP_WIDTH // 3 * 2, MAP_HEIGHT // 2)
    elif item_num3 == 3:
        image.clip_draw(item_WEI * 3, 650, item_WEI + 40, item_HIE, MAP_WIDTH // 3 * 2, MAP_HEIGHT // 2)
    elif item_num3 == 4:
        image.clip_draw(item_WEI * 0, 500, item_WEI, item_HIE, MAP_WIDTH // 3 * 2, MAP_HEIGHT // 2)
    elif item_num3 == 5:
        image.clip_draw(item_WEI * 3, 500, item_WEI + 40, item_HIE, MAP_WIDTH // 3 * 2, MAP_HEIGHT // 2)

    press_image.clip_draw(0, 0, 225, 55, MAP_WIDTH//3, MAP_HEIGHT//3)
    press_image.clip_draw(225, 0, 235, 55, MAP_WIDTH // 2, MAP_HEIGHT // 3)
    press_image.clip_draw(465, 0, 232, 55, MAP_WIDTH // 3 * 2, MAP_HEIGHT // 3)
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
                case pico2d.SDLK_1: # item_num1
                    if item_num1 == 1:
                        attack.attack_damage += 100
                    elif item_num1 == 2:
                        attack.attack_range += 50
                    elif item_num1 == 3:
                        attack.attack_max += 2
                    elif item_num1 == 4:
                        playstate.player.HP += 2
                    elif item_num1 == 5:
                        attack.attack_size += 20
                    item_choose = False
                    game_framework.pop_state()
                case pico2d.SDLK_2: #item_num2
                    if item_num2 == 1:
                        attack.attack_damage += 100
                    elif item_num2 == 2:
                        attack.attack_range += 50
                    elif item_num2 == 3:
                        attack.attack_max += 2
                    elif item_num2 == 4:
                        playstate.player.HP += 2
                    elif item_num2 == 5:
                        attack.attack_size += 20
                    item_choose = False
                    game_framework.pop_state()
                case pico2d.SDLK_3: #item_num3
                    if item_num3 == 1:
                        attack.attack_damage += 100
                    elif item_num3 == 2:
                        attack.attack_range += 50
                    elif item_num3 == 3:
                        attack.attack_max += 2
                    elif item_num3 == 4:
                        playstate.player.HP += 2
                    elif item_num3 == 5:
                        attack.attack_size += 20
                    item_choose = False
                    game_framework.pop_state()






