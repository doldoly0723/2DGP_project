from pico2d import*

import math
import attack
import game_framework
import isaac
import random   # 몬스터의 출현
import playstate
MAP_WIDTH, MAP_HEIGHT = 1600, 900

PIXEL_PER_METER = (10.0 / 0.1)  #10 pixel 10cm
RUN_SPEED_KMPH = 5.0   #Km / Hour

RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 10.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2


class Sucker:
    image = None
    reverse_image = None
    death_sound = None
    def __init__(self):
        self.WID = 80
        self.HEI = 80

        self.monster_t = 0

        self.x = 0
        self.y = 0
        self.monster_status = False  # 현재 존재하는가

        if Sucker.image == None:
            Sucker.image = load_image('Sprite/sucker.png')
        if Sucker.reverse_image == None:
            Sucker.reverse_image = load_image('Sprite/sucker_reverse.png')

        self.frame = 0
        self.frame_count = 0

        self.reverse_x = MAP_WIDTH//2

        self.choose_wall = 0 # 리스폰 지역 설정

        self.hp = 200
        self.dir = 0

        if Sucker.death_sound is None:
            Sucker.death_sound = load_wav('Sound/Death_sucker.wav')
            Sucker.death_sound.set_volume(15)

    def respawn_sucker(self):
        if self.monster_status == False:
            Sucker.__init__(self) # 초기화
        if 1 == random.randint(0, 500): #랜덤한 시간으로 몬스터를 생성 난이도 상승시 범위도 같이 높여야 한다
            if self.monster_status == False:
                self.choose_wall = random.randint(1, 4)
                #self.sucker_status = 1
                #초기화 작업
                self.hp = 200
                self.monster_t = 0
                if self.choose_wall == 1:   #밑에 지역
                    self.x = random.randint(0, MAP_WIDTH)
                    self.y = 0
                elif self.choose_wall == 2: #위 지역
                    self.x = random.randint(0, MAP_WIDTH)
                    self.y = MAP_HEIGHT
                elif self.choose_wall == 3: #왼쪽
                    self.x = 0
                    self.y = random.randint(0, MAP_HEIGHT)
                elif self.choose_wall == 4: #오른쪽
                    self.x = MAP_WIDTH
                    self.y = random.randint(0, MAP_HEIGHT)
                # self.x = 500
                # self.y = 500
                self.monster_status = True




    def update(self):
        Sucker.respawn_sucker(self)
        if self.monster_status == True:
            # self.monster_t += 0.00001  # 시간 지날수록 속도 증가
            # self.monster_t = 0.005      # 속도 고정
            self.dir = math.atan2(playstate.player.mid_y - self.y, playstate.player.mid_x - self.x)
            if playstate.player.map_x == playstate.player.end_of_left or playstate.player.map_x == playstate.player.end_of_right:
                self.x += RUN_SPEED_PPS * math.cos(self.dir)*game_framework.frame_time
            else:
                if playstate.player.injury_status == True:
                    self.x += RUN_SPEED_PPS * math.cos(self.dir)*game_framework.frame_time - playstate.player.dir_x*isaac.INJURY_SPEED_PPS*game_framework.frame_time
                else:
                    self.x += RUN_SPEED_PPS * math.cos(self.dir)*game_framework.frame_time - playstate.player.dir_x*isaac.RUN_SPEED_PPS*game_framework.frame_time

            if playstate.player.map_y == playstate.player.end_of_top or playstate.player.map_y == playstate.player.end_of_bottom:
                self.y += RUN_SPEED_PPS * math.sin(self.dir)*game_framework.frame_time
            else:
                if playstate.player.injury_status == True:
                    self.y += RUN_SPEED_PPS * math.sin(self.dir)*game_framework.frame_time - playstate.player.dir_y*isaac.INJURY_SPEED_PPS*game_framework.frame_time
                else:
                    self.y += RUN_SPEED_PPS * math.sin(self.dir)*game_framework.frame_time - playstate.player.dir_y*isaac.RUN_SPEED_PPS*game_framework.frame_time


            # self.x += RUN_SPEED_PPS * math.cos(self.dir)*game_framework.frame_time
            # self.y += RUN_SPEED_PPS * math.sin(self.dir)*game_framework.frame_time

        self.frame = (self.frame + FRAMES_PER_ACTION + ACTION_PER_TIME + game_framework.frame_time) % FRAMES_PER_ACTION
        # self.frame_count += 1
        # if self.frame_count == 10:
        #     self.frame = (self.frame + 1) % 2
        #     self.frame_count = 0
        #     pass



    def draw(self):
        if self.monster_status == True:
            if self.x <= self.reverse_x: # sucker 스프라이트 좌우 방향
                self.image.clip_draw(int(self.frame)*80, 0,
                                        self.WID, self.HEI, self.x, self.y)
            else:
                self.reverse_image.clip_draw(int(self.frame) * 80, 0,
                                            self.WID, self.HEI, self.x, self.y)
            # draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 30, self.y - 40, self.x + 30, self.y + 30

    def handle_collision(self, other, group):
        if group == 'tears:suckers':
            self.hp -= attack.attack_damage
            if self.hp <= 0:
                Sucker.death_sound.play()
                isaac.kill_cnt += 1
                self.monster_status = False
        if group == 'player:suckers':
            if other.injury_status == False:
                self.hp -= playstate.player.damage
                print('asdfsdafdsafdasf')
                print(self.get_bb())
                print(other.get_bb())
                la, ba, ra, ta = self.get_bb()
                lb, bb, rb, tb = other.get_bb()

                if la < rb and tb - ba > 5 and ta - bb > 5 and ra - lb > 5:
                    self.x += 100
                elif ra > lb and tb - ba > 5 and ta - bb > 5 and rb - la > 5:
                    self.x -= 100
                elif ta > bb and tb - ba > 5:
                    self.y -= 100
                elif ba < tb:
                    self.y += 100

                if self.hp <= 0:
                    isaac.kill_cnt += 1     # 보스 출현을 위한 킬 카운트
                    self.monster_status = False


monster = None






