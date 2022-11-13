from pico2d import*
import game_framework
import isaac
import game_world
import monster

from isaac import Player
from monster import Sucker
from attack import Attack
MAP_WIDTH, MAP_HEIGHT = 1600, 900

player = None
suckers = None
tears = None

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
    global player, suckers, tears
    player = Player()
    tears = Attack()

    game_world.add_object(player, 0)

    suckers = [Sucker() for i in range(5)]
    game_world.add_objects(suckers, 1)

    

def exit():
    global player, suckers, tears
    del player
    del suckers
    del tears

def update():
    global player, suckers, tears
    for game_object in game_world.all_objects():
        game_object.update()

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


