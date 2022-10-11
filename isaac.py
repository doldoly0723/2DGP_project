from pico2d import*
# 화면 크기
MAP_WIDTH, MAP_HEIGHT = 1600, 900
# 전체 맵 크기
FULL_MAP_WID, FULL_MAP_HEI = 6401, 3600

class Map:
    def __init__(self):
        self.image = load_image('map.png')
        self.mid_x = MAP_WIDTH // 2
        self.mid_y = MAP_HEIGHT // 2
        self.map_x = FULL_MAP_WID // 2
        self.map_y = FULL_MAP_HEI // 2

    def update(self):
        self.map_x += dir_x*5
        self.map_y += dir_y*5
        pass
    def draw(self):
        self.image.clip_draw(self.map_x,self.map_y,MAP_WIDTH,MAP_HEIGHT,self.mid_x,self.mid_y)
        pass

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


running = True
dir_x=0;
dir_y=0;
map = Map()

while running:
    clear_canvas()
    handle_events()
    map.update()
    map.draw()
    update_canvas()

    delay(0.01)



close_canvas()
