from pico2d import*

MAP_WIDTH, MAP_HEIGHT = 1200, 1000

# 캐릭터 이동 및 공격 키 입력
def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
    pass

open_canvas(MAP_WIDTH,MAP_HEIGHT)

isaac = load_image('isaac.png')
MAP = load_image('map.png')

running = True

while running:
    handle_events()
    clear_canvas()



close_canvas()
