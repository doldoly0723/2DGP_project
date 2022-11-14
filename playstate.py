from pico2d import*
import game_framework
import isaac
import game_world
import monster

from isaac import Player
from monster import Sucker
from attack import Attack
from monster2 import Spitty
MAP_WIDTH, MAP_HEIGHT = 1600, 900

player = None
suckers = None
tears = None
spittys = None

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

    game_world.add_collision_pairs(tears, suckers, 'tears:suckers')
    game_world.add_collision_pairs(tears, spittys, 'tears:spittys')

def exit():
    game_world.clear()

def update():
    for game_object in game_world.all_objects():
        game_object.update()
    for a, b, group in game_world.all_collision_pairs():
        if collide(a, b):

            print('COLLISION', group)
            a.handle_collision(b, group)
            b.handle_collision(a, group)
    # print('start')
    # for game_object in game_world.all_objects():
    #     print(game_object)
    # print('end')

    # player.update()
    # for tear in tears:
    #     tear.update()
    # for sucker in suckers:
    #     sucker.respawn_sucker()
    #     sucker.update()

def draw_world():
    for game_object in game_world.all_objects():
        game_object.draw()
    # global player, suckers, tears
    # # player.draw()
    # for tear in tears:
    #     tear.draw()
    # for sucker in suckers:
    #     sucker.draw()
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
