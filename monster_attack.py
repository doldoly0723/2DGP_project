from pico2d import*

import attack
import isaac
import monster
from monster import Sucker
import playstate
import game_world
import monstro

# 화면 크기
MAP_WIDTH, MAP_HEIGHT = 1600, 900
# 전체 맵 크기
FULL_MAP_WID, FULL_MAP_HEI = 6401, 3600

class Monster_Attack():
    image = None
    def __init__(self):
        if Monster_Attack.image == None:
            Monster_Attack.image = load_image('monster_tear.png')

        self.frame_x = 340
        self.frame_y = 39
        self.attack_WID = 47
        self.attack_HEI = 42
        self.attack_speed = 5
        self.attack_x = 0
        self.attack_y = 0
        self.attack_status = False
        self.attack_dir = None

        # 공격 범위 나중에 설정
        self.attack_range = 300

        self.attack_damage = 100

        self.Num_tear = None # 2개 연속 사격시 처음 구체 사라지고 두번째 구체를 사라지게 하기 위한 변수

        self.dir = 0

        #print('생성: ', self.attack_num)

    def update(self):

        self.attack_range -= 1
        if self.attack_range < 0:
            game_world.remove_object(self)

        if self.dir == 0:   #down
            self.attack_y = (self.attack_y - self.attack_speed)
            if body_dir == 2 or body_dir == 6:
                self.attack_x -= playstate.player.dir_x * 5
            elif body_dir == 0 or body_dir == 4:
                self.attack_y -= playstate.player.dir_y * 4

        elif self.dir == 1: #up
            self.attack_y = (self.attack_y + self.attack_speed)
            if body_dir == 2 or body_dir == 6:
                self.attack_x -= playstate.player.dir_x * 5
            elif body_dir == 0 or body_dir == 4:
                self.attack_y -= playstate.player.dir_y * 4

        elif self.dir == 2: #left
            self.attack_x = (self.attack_x - self.attack_speed)
            if body_dir == 4 or body_dir == 0:  # 공격 후 이동시 구체는 일정하게 이동
                self.attack_y -= playstate.player.dir_y * 5
            elif body_dir == 2 or body_dir == 6:  # 공격 방향과 같은 축으로 이동시 구체 진행 속도 조절
                self.attack_x -= playstate.player.dir_x * 4

        elif self.dir == 3: #right
            self.attack_x = (self.attack_x + self.attack_speed)
            if body_dir == 4 or body_dir == 0:  # 공격 후 이동시 구체는 일정하게 이동
                self.attack_y -= playstate.player.dir_y * 5
            elif body_dir == 2 or body_dir == 6:  # 공격 방향과 같은 축으로 이동시 구체 진행 속도 조절
                self.attack_x -= playstate.player.dir_x * 4

        elif self.dir == 4: #UL
            self.attack_x -= self.attack_speed
            self.attack_y += self.attack_speed
            if body_dir == 4 or body_dir == 0:  # 공격 후 이동시 구체는 일정하게 이동
                self.attack_y -= playstate.player.dir_y * 5
            elif body_dir == 2 or body_dir == 6:  # 공격 방향과 같은 축으로 이동시 구체 진행 속도 조절
                self.attack_x -= playstate.player.dir_x * 4

        elif self.dir == 5: # UR
            self.attack_x += self.attack_speed
            self.attack_y += self.attack_speed
            if body_dir == 4 or body_dir == 0:  # 공격 후 이동시 구체는 일정하게 이동
                self.attack_y -= playstate.player.dir_y * 5
            elif body_dir == 2 or body_dir == 6:  # 공격 방향과 같은 축으로 이동시 구체 진행 속도 조절
                self.attack_x -= playstate.player.dir_x * 4

        elif self.dir == 6: #DL
            self.attack_x -= self.attack_speed
            self.attack_y -= self.attack_speed
            if body_dir == 4 or body_dir == 0:  # 공격 후 이동시 구체는 일정하게 이동
                self.attack_y -= playstate.player.dir_y * 5
            elif body_dir == 2 or body_dir == 6:  # 공격 방향과 같은 축으로 이동시 구체 진행 속도 조절
                self.attack_x -= playstate.player.dir_x * 4

        elif self.dir == 7: #DR
            self.attack_x += self.attack_speed
            self.attack_y -= self.attack_speed
            if body_dir == 4 or body_dir == 0:  # 공격 후 이동시 구체는 일정하게 이동
                self.attack_y -= playstate.player.dir_y * 5
            elif body_dir == 2 or body_dir == 6:  # 공격 방향과 같은 축으로 이동시 구체 진행 속도 조절
                self.attack_x -= playstate.player.dir_x * 4




    # 캐릭터 이동 및 공격 키 입력
    def draw(self):
            self.image.clip_draw(self.frame_x, self.frame_y,
                                        self.attack_WID, self.attack_HEI, self.attack_x, self.attack_y)
            draw_rectangle(*self.get_bb())


    def get_bb(self):
        return self.attack_x - 25, self.attack_y - 23, self.attack_x + 21, self.attack_y + 23

    def handle_collision(self, other, group):
        if group == 'monster_tears:player':
            if other.injury_status == False:
                game_world.remove_object(self)

attack_on = False
body_dir = 0

