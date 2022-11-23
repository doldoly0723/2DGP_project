from pico2d import*
import game_framework
import isaac
import game_world
import monster_sucker
import item_state
import end_state

from isaac import Player
from monster_sucker import Sucker
from attack import Attack
from monster_spitty import Spitty
from boss_monstro import Monstro
from monster_attack import Monster_Attack
MAP_WIDTH, MAP_HEIGHT = 1600, 900

player = None
suckers = None
tears = None
spittys = None
monstros = None
monster_tears = None

boss_1 = False  #stage 1
item_1 = False  #stage 1

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        else:
            player.handle_event(event)

def enter():
    global player, suckers, tears, spittys
    player = Player()
    #tears = Attack()

    game_world.add_object(player, 0)

    suckers = [Sucker() for i in range(3)]
    game_world.add_objects(suckers, 1)

    spittys = [Spitty() for i in range(3)]
    game_world.add_objects(spittys, 1)

    # 몬스터와 공격 충돌체크
    game_world.add_collision_pairs(None, suckers, 'tears:suckers')
    game_world.add_collision_pairs(None, spittys, 'tears:spittys')

    #몬스터와 캐릭터 충돌 체크
    game_world.add_collision_pairs(player, suckers, 'player:suckers')
    game_world.add_collision_pairs(player, spittys, 'player:spittys')

    #몬스터 공격과 플레이어 충돌 체크
    game_world.add_collision_pairs(None, player, 'monster_tears:player')

def exit():
    game_world.clear()

def update():
    global monstros, boss_1, item_1
    for game_object in game_world.all_objects():
        game_object.update()
    for a, b, group in game_world.all_collision_pairs():
        if collide(a, b):

            print('COLLISION', group)
            b.handle_collision(a, group)
            a.handle_collision(b, group)


    if player.HP == 0:
        game_framework.change_state(end_state)

    if isaac.kill_cnt >= 0:     #보스 생성 조건
        if boss_1 == False:
            monstros = Monstro()
            game_world.add_object(monstros, 1)
            game_world.add_collision_pairs(None, monstros, 'tears:monstros')
            game_world.add_collision_pairs(player, monstros, 'player:monstros')
            boss_1 = True
    if isaac.boss_kill_cnt == 1:
        if item_1 == False:
            game_framework.push_state(item_state)
            item_1 = True

def draw_world():
    for game_object in game_world.all_objects():
        game_object.draw()

    delay(0.01)

def draw():
    clear_canvas()
    draw_world()
    update_canvas()

def pause():
    pass

def resume():
    pass

def collide(a, b):
    la, ba, ra, ta = a.get_bb()
    lb, bb, rb, tb = b.get_bb()

    if la > rb: return False
    if ra < lb: return False
    if ta < bb: return False
    if ba > tb: return False

    return True
