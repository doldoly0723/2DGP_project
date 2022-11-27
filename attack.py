from pico2d import*

import attack
import game_framework
import isaac
import monster_sucker
from monster_sucker import Sucker
import playstate
import game_world

# 화면 크기
MAP_WIDTH, MAP_HEIGHT = 1600, 900
# 전체 맵 크기
FULL_MAP_WID, FULL_MAP_HEI = 6401, 3600

PIXEL_PER_METER = (10.0 / 0.1)  #10 pixel 10cm
ATTACK_SPEED_KMPH = 20.0   #Km / Hour

ATTACK_SPEED_MPM = (ATTACK_SPEED_KMPH * 1000.0 / 60.0)
ATTACK_SPEED_MPS = (ATTACK_SPEED_MPM / 60.0)
ATTACK_SPEED_PPS = (ATTACK_SPEED_MPS * PIXEL_PER_METER)

class Attack():
    image = None
    def __init__(self):
        if Attack.image == None:
            Attack.image = load_image('tear.png')

        self.frame_x = 347
        self.frame_y = 39
        self.WID = 47
        self.HEI = 42
        self.speed = 5
        self.x = MAP_WIDTH // 2
        self.y = MAP_HEIGHT // 2
        self.status = False
        self.dir = None

        # 공격 범위 나중에 설정
        self.range = 0


    def update(self):
        global tears, attack_cnt, attack_range
        if attack_on == True: # 화살표 누르면 활성화
            if self.status == False:
                if playstate.player.frame_head == 0: # down
                    self.dir = 0
                elif playstate.player.frame_head == 4: #up
                    self.dir = 4
                elif playstate.player.frame_head == 6: #left
                    self.dir = 6
                elif playstate.player.frame_head == 2: # right
                    self.dir = 2

            self.status = True # 공격 방향으로 직진, 다른 방향 키 입력시 공격구체 방향이동x
            if self.status == True:
                # 공격 사거리
                self.range += 1
                if (attack_range - self.range) < 0:
                    game_world.remove_object(self)
                    attack_cnt -= 1

                if self.dir == 0:    #down
                    # self.y = (self.y - self.speed)
                    # if isaac.body_RL == True:
                    #     self.x -= playstate.player.dir_x * ATTACK_SPEED_PPS * game_framework.frame_time
                    # if isaac.body_UD == True:
                    #     self.y -= playstate.player.dir_y * ATTACK_SPEED_PPS * game_framework.frame_time
                    self.y -= ATTACK_SPEED_PPS * game_framework.frame_time
                    if isaac.body_UD == True:
                        self.y -= playstate.player.dir_y * 6
                    if isaac.body_RL == True:
                        self.x -= playstate.player.dir_x * 6

                elif self.dir == 4:  #up
                    # self.y = (self.y + self.speed)
                    # if isaac.body_RL == True:
                    #     self.x -= playstate.player.dir_x * ATTACK_SPEED_PPS * game_framework.frame_time
                    # if isaac.body_UD == True:
                    #     self.y -= playstate.player.dir_y * ATTACK_SPEED_PPS * game_framework.frame_time
                    self.y += ATTACK_SPEED_PPS * game_framework.frame_time
                    if isaac.body_UD == True:
                        self.y -= playstate.player.dir_y * 6
                    if isaac.body_RL == True:
                        self.x -= playstate.player.dir_x * 6

                elif self.dir == 6:  #left
                    # self.x = (self.x - self.speed)
                    # if isaac.body_UD == True:  #공격 후 이동시 구체는 일정하게 이동
                    #     self.y -= playstate.player.dir_y*ATTACK_SPEED_PPS * game_framework.frame_time
                    # if isaac.body_RL == True:  # 공격 방향과 같은 축으로 이동시 구체 진행 속도 조절
                    #     self.x -= playstate.player.dir_x * ATTACK_SPEED_PPS * game_framework.frame_time
                    self.x -= ATTACK_SPEED_PPS * game_framework.frame_time
                    if isaac.body_UD == True:
                        self.y -= playstate.player.dir_y * 6
                    if isaac.body_RL == True:
                        self.x -= playstate.player.dir_x * 6

                elif self.dir == 2:  #right
                    # self.x = (self.x + self.speed)
                    # if isaac.body_UD == True:  #공격 후 이동시 구체는 일정하게 이동
                    #     self.y -= playstate.player.dir_y*ATTACK_SPEED_PPS * game_framework.frame_time
                    # if isaac.body_RL == True: #공격 방향과 같은 축으로 이동시 구체 진행 속도 조절
                    #     self.x -= playstate.player.dir_x*ATTACK_SPEED_PPS * game_framework.frame_time
                    self.x += ATTACK_SPEED_PPS * game_framework.frame_time
                    if isaac.body_UD == True:
                        self.y -= playstate.player.dir_y * 6
                    if isaac.body_RL == True:
                        self.x -= playstate.player.dir_x * 6


    # 캐릭터 이동 및 공격 키 입력
    def draw(self):
            if self.status == True:
                self.image.clip_draw(self.frame_x, self.frame_y,
                                        self.WID, self.HEI, self.x, self.y, attack_size, attack_size)
            # draw_rectangle(*self.get_bb())

            # 공격 구체 남은 갯수
            for i in range(attack_max - attack_cnt):
                self.image.clip_draw(20, 37, 40, 82, 1550 + i*(-20), 850)
    def get_bb(self):
        return self.x - 21*attack_size/40, self.y - 23*attack_size/40, \
               self.x + 21*attack_size/40, self.y + 23*attack_size/40

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

