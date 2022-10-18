from pico2d import*
import isaac

# 화면 크기
MAP_WIDTH, MAP_HEIGHT = 1600, 900
# 전체 맵 크기
FULL_MAP_WID, FULL_MAP_HEI = 6401, 3600

class Attack():
    def __init__(self):
        self.image_attack = load_image('tear.png')

        self.frame_x = 347
        self.frame_y = 39
        self.attack_WID = 47
        self.attack_HEI = 42
        self.attack_speed = 5
        self.attack_x = MAP_WIDTH // 2
        self.attack_y = MAP_HEIGHT // 2
        self.attack_status = False
        self.attack_dir = None

        # 공격 범위 나중에 설정
        self.attack_range = 500

        self.attack_damage = 100

    def update(self):
        if attack_on == True: # 화살표 누르면 활성화
            if self.attack_status == False:
                if isaac.frame_head == 0: # down
                    self.attack_dir = 0
                elif isaac.frame_head == 4: #up
                    self.attack_dir = 4
                elif isaac.frame_head == 6: #left
                    self.attack_dir = 6
                elif isaac.frame_head == 2: # right
                    self.attack_dir = 2

            self.attack_status = True # 공격 방향으로 직진, 다른 방향 키 입력시 공격구체 방향이동x
            if self.attack_status == True:
                if self.attack_dir == 0:
                    self.attack_y = (self.attack_y - self.attack_speed)
                    if body_dir == 2 or body_dir == 6:
                        self.attack_x -= isaac.dir_x*5
                    elif body_dir == 0 or body_dir == 4:
                        self.attack_y -= isaac.dir_y * 4

                elif self.attack_dir == 4:
                    self.attack_y = (self.attack_y + self.attack_speed)
                    if body_dir == 2 or body_dir == 6:
                        self.attack_x -= isaac.dir_x * 5
                    elif body_dir == 0 or body_dir == 4:
                        self.attack_y -= isaac.dir_y * 4

                elif self.attack_dir == 6:
                    self.attack_x = (self.attack_x - self.attack_speed)
                    if body_dir == 4 or body_dir == 0:  #공격 후 이동시 구체는 일정하게 이동
                        self.attack_y -= isaac.dir_y*5
                    elif body_dir == 2 or body_dir == 6:  # 공격 방향과 같은 축으로 이동시 구체 진행 속도 조절
                        self.attack_x -= isaac.dir_x * 4

                elif self.attack_dir == 2:
                    self.attack_x = (self.attack_x + self.attack_speed)
                    if body_dir == 4 or body_dir == 0:  #공격 후 이동시 구체는 일정하게 이동
                        self.attack_y -= isaac.dir_y*5
                    elif body_dir == 2 or body_dir == 6: #공격 방향과 같은 축으로 이동시 구체 진행 속도 조절
                        self.attack_x -= isaac.dir_x*4
            #캐릭터 이동에 따라 공격구체의 좌표값이 같이 따라 움직이는 부분 수정
        # if monster.Sucker().sucker_x-40 <= self.attack_x <= monster.Sucker().sucker_x+40:
        #     if monster.Sucker().sucker_y-40 <= self.attack_y <= monster.Sucker().sucker_y+40:
        #         self.attack_status = False


    def draw(self):
        if self.attack_status == True:
            self.image_attack.clip_draw(self.frame_x, self.frame_y,
                                    self.attack_WID, self.attack_HEI, self.attack_x, self.attack_y)


        pass

# 캐릭터 이동 및 공격 키 입력




attack_on = None
body_dir = None
tears = None

def enter():
    global attack_on, tears, body_dir
    attack_on = False
    tears = [Attack()]
    body_dir = 0

def exit():
    global tears
    del tears
def update():
    for tear in tears:
        tear.update()
def draw():
    for tear in tears:
        tear.draw()
    #update_canvas()

