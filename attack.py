from pico2d import*

import attack
import isaac
import monster
from monster import Sucker
import playstate
import game_world

# 화면 크기
MAP_WIDTH, MAP_HEIGHT = 1600, 900
# 전체 맵 크기
FULL_MAP_WID, FULL_MAP_HEI = 6401, 3600

class Attack():
    image = None
    def __init__(self):
        if Attack.image == None:
            Attack.image = load_image('tear.png')

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
        self.attack_range = 0

        self.attack_num = attack_cnt # 처음 생성될때 번호를 가지고 생성

        self.Num_tear = None # 2개 연속 사격시 처음 구체 사라지고 두번째 구체를 사라지게 하기 위한 변수

        #print('생성: ', self.attack_num)

    def update(self):
        global tears, attack_cnt, attack_range
        if attack_on == True: # 화살표 누르면 활성화
            if self.attack_status == False:
                if playstate.player.frame_head == 0: # down
                    self.attack_dir = 0
                elif playstate.player.frame_head == 4: #up
                    self.attack_dir = 4
                elif playstate.player.frame_head == 6: #left
                    self.attack_dir = 6
                elif playstate.player.frame_head == 2: # right
                    self.attack_dir = 2

            self.attack_status = True # 공격 방향으로 직진, 다른 방향 키 입력시 공격구체 방향이동x
            if self.attack_status == True:
                # 공격 사거리
                self.attack_range += 1
                if (attack_range - self.attack_range) < 0:
                    game_world.remove_object(self)
                    attack_cnt -= 1

                if self.attack_dir == 0:    #down
                    self.attack_y = (self.attack_y - self.attack_speed)
                    if isaac.body_RL == True:
                        self.attack_x -= playstate.player.dir_x*5
                    if isaac.body_UD == True:
                        self.attack_y -= playstate.player.dir_y * 4

                elif self.attack_dir == 4:  #up
                    self.attack_y = (self.attack_y + self.attack_speed)
                    if isaac.body_RL == True:
                        self.attack_x -= playstate.player.dir_x * 5
                    if isaac.body_UD == True:
                        self.attack_y -= playstate.player.dir_y * 4

                elif self.attack_dir == 6:  #left
                    self.attack_x = (self.attack_x - self.attack_speed)
                    if isaac.body_UD == True:  #공격 후 이동시 구체는 일정하게 이동
                        self.attack_y -= playstate.player.dir_y*5
                    if isaac.body_RL == True:  # 공격 방향과 같은 축으로 이동시 구체 진행 속도 조절
                        self.attack_x -= playstate.player.dir_x * 4

                elif self.attack_dir == 2:  #right
                    self.attack_x = (self.attack_x + self.attack_speed)
                    if isaac.body_UD == True:  #공격 후 이동시 구체는 일정하게 이동
                        self.attack_y -= playstate.player.dir_y*5
                    if isaac.body_RL == True: #공격 방향과 같은 축으로 이동시 구체 진행 속도 조절
                        self.attack_x -= playstate.player.dir_x*4


    # 캐릭터 이동 및 공격 키 입력
    def draw(self):
            if self.attack_status == True:
                self.image.clip_draw(self.frame_x, self.frame_y,
                                        self.attack_WID, self.attack_HEI, self.attack_x, self.attack_y, attack_size, attack_size)
            # draw_rectangle(*self.get_bb())

            # 공격 구체 남은 갯수
            for i in range(attack_max - attack_cnt):
                self.image.clip_draw(20, 37, 40, 82, 1550 + i*(-20), 850)
    def get_bb(self):
        return self.attack_x - 21*attack_size/40, self.attack_y - 23*attack_size/40, \
               self.attack_x + 21*attack_size/40, self.attack_y + 23*attack_size/40

    def handle_collision(self, other, group):
        global attack_cnt
        if group == 'tears:suckers' or group == 'tears:spittys' or 'tears:monstros':
            attack_cnt -= 1
            game_world.remove_object(self)
attack_on = False
body_dir = 0
attack_cnt = 0  # 공격 횟수
attack_max = 5

attack_damage = 100
attack_range = 100
attack_size = 40

