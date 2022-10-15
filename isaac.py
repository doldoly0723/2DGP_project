from pico2d import*

# 화면 크기
MAP_WIDTH, MAP_HEIGHT = 1600, 900
# 전체 맵 크기
FULL_MAP_WID, FULL_MAP_HEI = 6401, 3600

class Map:
    def __init__(self):
        self.image_map = load_image('map.png')
        self.image_isaac = load_image('isaac.png')
        self.image_isaac_reverse = load_image('isaac_reverse.png')
        self.mid_x = MAP_WIDTH // 2
        self.mid_y = MAP_HEIGHT // 2
        self.map_x = FULL_MAP_WID // 2
        self.map_y = FULL_MAP_HEI // 2
        # head
        self.head_x = 20
        self.head_y = 835
        self.head_WID = 115
        self.head_HEI = 85
        self.head_frame = 0
        self.head_cnt = 0
        #body
        self.body_WID = 93
        self.body_HEI = 45
        self.body_x = 30
        self.body_y = 0 # UD, LR 에 따라 달라진다
        self.body_UD_y = 710 #위, 아래 스프라이트
        self.body_LR_y = 590 #왼쪽, 오른쪽 스프라이트
        self.body_frame = 0
        self.body_cnt = 0
        self.body_reverse_x = 26

        self.body_head_space = 45
        # 테두리 경계선
        self.end_of_left = 65
        self.end_of_right = 4800
        self.end_of_top = 2725
        self.end_of_bottom = 0
    def update(self):
        # 키 입력에 따른 이동
        self.map_x += dir_x*5
        self.map_y += dir_y*5
        # 맵 밖으로 못나가게 설정

        if self.map_x < self.end_of_left:
            self.map_x = self.end_of_left
        elif self.map_x > self.end_of_right:
            self.map_x = self.end_of_right
        elif self.map_y > self.end_of_top:
            self.map_y = self.end_of_top
        elif self.map_y < self.end_of_bottom:
            self.map_y = self.end_of_bottom

        # 키 입력에 따른 아이작 프레임 변화 머리, 다리 따로
        pass
    def update_head_frame(self): # 0, 1 눈을 깜빡이게 하면서 이동속도를 늧추지 않게 하기 위해서는? 우선은 랜덤 처리
        self.head_cnt += 1
        if self.head_cnt > 50:
            self.head_frame = (self.head_frame+1)%2
            self.head_cnt = 0
    def update_body_frame(self):
        if frame_body_Y == 0:   #LR
            self.body_y = self.body_LR_y
        elif frame_body_Y == 1: #UD
            self.body_y = self.body_UD_y

        self.body_cnt += 1
        if self.body_cnt > 20:
            self.body_frame = (self.body_frame+1)%10
            self.body_cnt = 0

    def draw(self):
        self.image_map.clip_draw(self.map_x,self.map_y,MAP_WIDTH,MAP_HEIGHT,self.mid_x,self.mid_y)
        # 몸
        if(frame_body_reverse == 0):
            self.image_isaac.clip_draw(self.body_frame * self.body_WID + self.body_x, self.body_y,self.body_WID, self.body_HEI, self.mid_x, self.mid_y - self.body_head_space)
        elif(frame_body_reverse == 1):
            self.image_isaac_reverse.clip_draw(self.body_frame * self.body_WID + self.body_reverse_x, self.body_y,self.body_WID, self.body_HEI, self.mid_x, self.mid_y - self.body_head_space)
        # 머리
        self.image_isaac.clip_draw((frame_head+self.head_frame)*self.head_WID+self.head_x, self.head_y, self.head_WID, self.head_HEI, self.mid_x, self.mid_y)
        pass

# 캐릭터 이동 및 공격 키 입력
def handle_events():
    global running
    global dir_y
    global dir_x
    global frame_head, frame_body_Y, frame_body_X, frame_body_reverse
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
                frame_body_Y = 1    #UD
                frame_body_reverse = 1
            elif event.key == SDLK_s:
                dir_y -= 1
                frame_body_Y = 1
                frame_body_reverse = 0
            elif event.key == SDLK_a:
                dir_x -= 1
                frame_body_Y = 0    #LR
                frame_body_reverse = 1
            elif event.key == SDLK_d:
                dir_x += 1
                frame_body_Y = 0
                frame_body_reverse = 0
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

running = None
dir_x = None
dir_y = None
# 맵 이동에 따른 아이작 프레임 설정 머리 다리 따로 설정 필요
frame_head = None
frame_body_reverse = None    # 반전 스프라이트 체크
frame_body_Y = None    # 상하 스프라이트인가 좌우 스프라이트인가
map = None

def enter():
    global running
    global dir_x, dir_y
    global frame_head, frame_body_Y,frame_body_reverse
    global map
    running = True
    dir_x = 0
    dir_y = 0
    frame_head = 0
    frame_body_reverse = 0  # 반전 스프라이트 체크
    frame_body_Y = 1  # 상하 스프라이트인가 좌우 스프라이트인가
    map = Map()

def exit():
    global map
    del map
def update():
    map.update()
    map.update_head_frame()
    map.update_body_frame()

def draw():
    clear_canvas()
    map.draw()
    delay(0.01)
    update_canvas()


