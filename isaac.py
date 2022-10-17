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

class Attack():
    def __init__(self):
        self.image_attack = load_image('tear.png')

        self.frame_x = 347
        self.frame_y = 39
        self.attack_WID = 47
        self.attack_HEI = 42
        self.attack_speed = 5
        self.attack_x = Map().mid_x
        self.attack_y = Map().mid_y
        self.attack_status = False
        self.attack_dir = None

        # 공격 범위
        self.attack_range = 500

    def update(self):
        if attack_on == True: # 화살표 누르면 활성화
            if self.attack_status == False:
                if frame_head == 0: # down
                    self.attack_dir = 0
                elif frame_head == 4: #up
                    self.attack_dir = 4
                elif frame_head == 6: #left
                    self.attack_dir = 6
                elif frame_head == 2: # right
                    self.attack_dir = 2

            self.attack_status = True # 공격 방향으로 직진, 다른 방향 키 입력시 공격구체 방향이동x
            if self.attack_status == True:
                if self.attack_dir == 0:
                    self.attack_y = (self.attack_y - self.attack_speed)
                    if body_dir == 2 or body_dir == 6:
                        self.attack_x -= dir_x*5
                    elif body_dir == 0 or body_dir == 4:
                        self.attack_y -= dir_y * 4

                elif self.attack_dir == 4:
                    self.attack_y = (self.attack_y + self.attack_speed)
                    if body_dir == 2 or body_dir == 6:
                        self.attack_x -= dir_x * 5
                    elif body_dir == 0 or body_dir == 4:
                        self.attack_y -= dir_y * 4

                elif self.attack_dir == 6:
                    self.attack_x = (self.attack_x - self.attack_speed)
                    if body_dir == 4 or body_dir == 0:  #공격 후 이동시 구체는 일정하게 이동
                        self.attack_y -= dir_y*5
                    elif body_dir == 2 or body_dir == 6:  # 공격 방향과 같은 축으로 이동시 구체 진행 속도 조절
                        self.attack_x -= dir_x * 4

                elif self.attack_dir == 2:
                    self.attack_x = (self.attack_x + self.attack_speed)
                    if body_dir == 4 or body_dir == 0:  #공격 후 이동시 구체는 일정하게 이동
                        self.attack_y -= dir_y*4
                    elif body_dir == 2 or body_dir == 6: #공격 방향과 같은 축으로 이동시 구체 진행 속도 조절
                        self.attack_x -= dir_x*4
            #캐릭터 이동에 따라 공격구체의 좌표값이 같이 따라 움직이는 부분 수정



    def draw(self):
        if self.attack_status == True:
            self.image_attack.clip_draw(self.frame_x, self.frame_y,
                                    self.attack_WID, self.attack_HEI, self.attack_x, self.attack_y)


        pass

# 캐릭터 이동 및 공격 키 입력
def handle_events():
    global running
    global dir_y
    global dir_x
    global frame_head, frame_body_Y, frame_body_X, frame_body_reverse
    global attack_on, body_dir
    global tears
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
                body_dir = 4    #up
            elif event.key == SDLK_s:
                dir_y -= 1
                frame_body_Y = 1
                frame_body_reverse = 0
                body_dir = 0    #down
            elif event.key == SDLK_a:
                dir_x -= 1
                frame_body_Y = 0    #LR
                frame_body_reverse = 1
                body_dir = 2    #left
            elif event.key == SDLK_d:
                dir_x += 1
                frame_body_Y = 0
                frame_body_reverse = 0
                body_dir = 6    #right
            #이동에 따른 아이작 스프라이트
            #키누르면 공격 모드 시작
            elif event.key == SDLK_UP:
                frame_head = 4
                attack_on = True
            elif event.key == SDLK_DOWN:
                frame_head = 0
                attack_on = True
            elif event.key == SDLK_LEFT:
                frame_head = 6
                attack_on = True
                tears += [Attack()]
            elif event.key == SDLK_RIGHT:
                frame_head = 2
                attack_on = True
                tears += [Attack()]
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_w:
                dir_y -= 1
            elif event.key == SDLK_s:
                dir_y += 1
            elif event.key == SDLK_a:
                dir_x += 1
            elif event.key == SDLK_d:
                dir_x -= 1
    #         #공격 버튼 up 시 공격모드 취소
    #         elif event.key == SDLK_UP:
    #             attack_on = False
    #         elif event.key == SDLK_DOWN:
    #             attack_on = False
    #         elif event.key == SDLK_LEFT:
    #             attack_on = False
    #         elif event.key == SDLK_RIGHT:
    #             attack_on = False
    # pass

running = None
dir_x = None
dir_y = None
# 맵 이동에 따른 아이작 프레임 설정 머리 다리 따로 설정 필요
frame_head = None
frame_body_reverse = None    # 반전 스프라이트 체크
frame_body_Y = None    # 상하 스프라이트인가 좌우 스프라이트인가
map = None
attack_on = None
body_dir = None
tears = None

def enter():
    global running
    global dir_x, dir_y
    global frame_head, frame_body_Y,frame_body_reverse
    global map
    global attack_on, tears, body_dir
    running = True
    attack_on = False
    dir_x = 0
    dir_y = 0
    frame_head = 0
    frame_body_reverse = 0  # 반전 스프라이트 체크
    frame_body_Y = 1  # 상하 스프라이트인가 좌우 스프라이트인가
    map = Map()

    tears = [Attack()]
    body_dir = 0

def exit():
    global map, tears
    del map
    del tears
def update():
    map.update()
    map.update_head_frame()
    map.update_body_frame()
    for tear in tears:
        tear.update()

def draw():
    clear_canvas()
    map.draw()
    for tear in tears:
        tear.draw()

    delay(0.01)
    update_canvas()


