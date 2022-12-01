from pico2d import*
import game_framework
import isaac
import game_world
import monster_sucker
import item_state
import game_over_state
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
boss_2 = False
boss_3 = False

item_1 = False  #stage 1
item_2 = False
item_3 = False

Round_2_respawn = False
Round_3_respawn = False

Round_1 = True
Round_2 = False
Round_3 = False

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
    tears = Attack()

    game_world.add_object(player, 0)

    suckers = [Sucker() for i in range(3)]
    game_world.add_objects(suckers, 1)

    spittys = [Spitty() for i in range(3)]
    game_world.add_objects(spittys, 1)

    # 몬스터와 공격 충돌체크
    game_world.add_collision_pairs(None, suckers, 'tears:suckers')
    game_world.add_collision_pairs(None, spittys, 'tears:spittys')

    # 몬스터와 캐릭터 충돌 체크
    game_world.add_collision_pairs(player, suckers, 'player:suckers')
    game_world.add_collision_pairs(player, spittys, 'player:spittys')

    #몬스터 공격과 플레이어 충돌 체크
    game_world.add_collision_pairs(None, player, 'monster_tears:player')

def exit():
    game_world.clear()

def update():
    global monstros, boss_1, boss_2, boss_3, item_1, item_2, item_3, suckers, spittys, Round_2_respawn, Round_3_respawn
    global Round_1, Round_2, Round_3
    for game_object in game_world.all_objects():
        game_object.update()
    for a, b, group in game_world.all_collision_pairs():
        if collide(a, b):

            print('COLLISION', group)
            b.handle_collision(a, group)
            a.handle_collision(b, group)


    if player.HP == 0:
        game_framework.change_state(game_over_state)

    #1라운드
    if isaac.kill_cnt >= 0:     #보스 생성 조건
        if boss_1 == False:     #보스 1번만 생성되도록
            monstros = Monstro()
            game_world.add_object(monstros, 1)
            game_world.add_collision_pairs(None, monstros, 'tears:monstros')
            game_world.add_collision_pairs(player, monstros, 'player:monstros')
            boss_1 = True
    if isaac.boss_kill_cnt == 1:

        if item_1 == False:
            game_framework.push_state(item_state)
            item_1 = True
            Round_2_respawn = True
            # 맵 다른거 그리기 위해
            Round_1 = False
            Round_2 = True

    # 2라운드
    if Round_2_respawn == True:
        suckers = [Sucker() for i in range(5)]
        game_world.add_objects(suckers, 1)

        spittys = [Spitty() for i in range(5)]
        game_world.add_objects(spittys, 1)

        # 몬스터와 공격 충돌체크
        game_world.add_collision_pairs(None, suckers, 'tears:suckers')
        game_world.add_collision_pairs(None, spittys, 'tears:spittys')

        # 몬스터와 캐릭터 충돌 체크
        game_world.add_collision_pairs(player, suckers, 'player:suckers')
        game_world.add_collision_pairs(player, spittys, 'player:spittys')
        Round_2_respawn = False

    if isaac.kill_cnt >= 20:     #보스 생성 조건
        if boss_2 == False:
            monstros = [Monstro() for i in range(2)]
            game_world.add_objects(monstros, 1)
            game_world.add_collision_pairs(None, monstros, 'tears:monstros')
            game_world.add_collision_pairs(player, monstros, 'player:monstros')
            boss_2 = True
    if isaac.boss_kill_cnt == 3:
        if item_2 == True and item_3 == False:
            game_framework.push_state(item_state)
            item_3 = True

        if item_2 == False:
            game_framework.push_state(item_state)
            item_2 = True
            Round_3_respawn = True
            Round_2 = False
            Round_3 = True

    # 3라운드
    if Round_3_respawn == True:
        suckers = [Sucker() for i in range(7)]
        game_world.add_objects(suckers, 1)

        spittys = [Spitty() for i in range(7)]
        game_world.add_objects(spittys, 1)

        # 몬스터와 공격 충돌체크
        game_world.add_collision_pairs(None, suckers, 'tears:suckers')
        game_world.add_collision_pairs(None, spittys, 'tears:spittys')

        # 몬스터와 캐릭터 충돌 체크
        game_world.add_collision_pairs(player, suckers, 'player:suckers')
        game_world.add_collision_pairs(player, spittys, 'player:spittys')
        Round_3_respawn = False

    if isaac.kill_cnt >= 50:     #보스 생성 조건
        if boss_3 == False:
            monstros = [Monstro() for i in range(3)]
            game_world.add_objects(monstros, 1)
            game_world.add_collision_pairs(None, monstros, 'tears:monstros')
            game_world.add_collision_pairs(player, monstros, 'player:monstros')
            boss_3 = True
    if isaac.boss_kill_cnt == 6:
        #end_state
        game_framework.change_state(end_state)

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
