from pico2d import*
# 화면 크기
MAP_WIDTH, MAP_HEIGHT = 1600, 900
# 전체 맵 크기
FULL_MAP_WID, FULL_MAP_HEI = 7113, 4000

# 캐릭터 이동 및 공격 키 입력
def handle_events():
    global running
    global dir_y
    global dir_x
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_w:
                dir_y += 1
            elif event.key == SDLK_s:
                dir_y -= 1
            elif event.key == SDLK_a:
                dir_x -= 1
            elif event.key == SDLK_d:
                dir_x += 1
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_w:
                dir_y -= 1
            elif event.key == SDLK_s:
                dir_y += 1
            elif event.key == SDLK_a:
                dir_x += 1
            elif event.key == SDLK_d:
                dir_x -= 1
    pass

open_canvas(MAP_WIDTH,MAP_HEIGHT)

isaac = load_image('isaac.png')
MAP = load_image('map.png')


running = True
dir_x=0;
dir_y=0;
mid_x = MAP_WIDTH // 2
mid_y = MAP_HEIGHT // 2
map_x = FULL_MAP_WID // 2
map_y = FULL_MAP_HEI // 2

while running:
    clear_canvas()
    # 이미지의 좌표를 변경하며 맵이 이동하는 것처럼 보임
    MAP.clip_draw(map_x,map_y,MAP_WIDTH,MAP_HEIGHT,mid_x,mid_y)
    
    update_canvas()

    handle_events()
    map_x += dir_x*5
    map_y += dir_y*5
    delay(0.01)



close_canvas()
