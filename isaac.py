from pico2d import*
# 화면 크기
MAP_WIDTH, MAP_HEIGHT = 1600, 900
# 전체 맵 크기
FULL_MAP_WID, FULL_MAP_HEI = 6401, 3600

class Map:
    def __init__(self):
        self.image_map = load_image('map.png')
        self.image_isaac = load_image('isaac.png')
        self.mid_x = MAP_WIDTH // 2
        self.mid_y = MAP_HEIGHT // 2
        self.map_x = FULL_MAP_WID // 2
        self.map_y = FULL_MAP_HEI // 2
        # 수정 필요 좌표 다시 구하기
        self.head_x = 20
        self.head_y = 835
        self.head_WID = 115
        self.head_HEI = 85
        self.head_frame = 0

    def update(self):
        # 키 입력에 따른 이동
        self.map_x += dir_x*5
        self.map_y += dir_y*5
        self.head_frame = self.head_x + frame_head * self.head_WID
        # 키 입력에 따른 아이작 프레임 변화 머리, 다리 따로
        pass
    def draw(self):
        self.image_map.clip_draw(self.map_x,self.map_y,MAP_WIDTH,MAP_HEIGHT,self.mid_x,self.mid_y)
        # 머리
        self.image_isaac.clip_draw(self.head_frame, self.head_y, self.head_WID, self.head_HEI, self.mid_x, self.mid_y)
        # 몸
        pass

# 캐릭터 이동 및 공격 키 입력
def handle_events():
    global running
    global dir_y
    global dir_x
    global frame_head
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN:
            # 이동
            if event.key == SDLK_w:
                dir_y += 1
            elif event.key == SDLK_s:
                dir_y -= 1
            elif event.key == SDLK_a:
                dir_x -= 1
            elif event.key == SDLK_d:
                dir_x += 1
            #이동에 따른 아이작 스프라이트
            elif event.key == SDLK_UP:
                frame_head = 4
            elif event.key == SDLK_DOWN:
                frame_head = 0
            elif event.key == SDLK_LEFT:
                frame_head = 6
            elif event.key == SDLK_RIGHT:
                frame_head = 2
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
dir_x=0
dir_y=0
# 맵 이동에 따른 아이작 프레임 설정 머리 다리 따로 설정 필요
frame_head = 0
frame_bodyX = 0
frame_bodyY = 0
map = Map()

while running:
    clear_canvas()
    handle_events()
    map.update()
    map.draw()
    update_canvas()

    delay(0.01)



close_canvas()
