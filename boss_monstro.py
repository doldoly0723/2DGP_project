from pico2d import*

import attack
import game_world
import isaac
import random   # 몬스터의 출현
import playstate
import game_framework
import monster_attack
from monster_attack import Monster_Attack
MAP_WIDTH, MAP_HEIGHT = 1600, 900
monster_tears = None

PIXEL_PER_METER = (10.0 / 0.1)  #10 pixel 10cm
RUN_SPEED_KMPH = 25.0   #Km / Hour

RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# TIME_PER_ACTION = 10.0
# ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
# FRAMES_PER_ACTION = 4

class Monstro:
    image = None
    reverse_image = None
    def __init__(self):
        self.WID = 80
        self.HEI = 90

        self.monster_t = 0

        self.x = 0
        self.y = 0
        self.status = False  # 현재 존재하는가

        if Monstro.image == None:
            Monstro.image = load_image('Monstro.png')
        self.frame = 0
        self.frame_count = 0

        self.choose_wall = 0 # 리스폰 지역 설정

        self.hp = 200
        self.size = 200

        self.choose_pattern = None
        self.pattern_status = False
        self.pattern_1 =[5,6,7,4,5,8]   # 패턴 프레임 순서
        self.pattern_2 = [1,2]          # 패턴 프레임 순서
        self.pattern_3 = [3]
        self.frame_cnt_in_pattern_list = 0 # 리스트 안의 프레임 번호

        self.attack_status = False
        self.tear_num = 0

    def respawn_monstro(self):
        if self.status == False:
            Monstro.__init__(self)
            self.choose_wall = random.randint(1, 4)
            #self.sucker_status = 1
            #초기화 작업
            self.hp = 2000
            self.monster_t = 0
            if self.choose_wall == 1:   #밑에 지역
                self.x = random.randint(0, MAP_WIDTH)
                self.y = 0 - 100
            elif self.choose_wall == 2: #위 지역
                self.x = random.randint(0, MAP_WIDTH)
                self.y = MAP_HEIGHT + 100
            elif self.choose_wall == 3: #왼쪽
                self.x = 0 - 100
                self.y = random.randint(0, MAP_HEIGHT)
            elif self.choose_wall == 4: #오른쪽
                self.x = MAP_WIDTH + 100
                self.y = random.randint(0, MAP_HEIGHT)
            self.status = True

    def update(self):
        Monstro.respawn_monstro(self)
        if self.status == True:
            if self.frame == 7:
                #self.monster_t += 0.00005  # 시간 지날수록 속도 증가
                # self.monster_t = 0.02   # monstro 속도 고정
                self.dir = math.atan2(playstate.player.mid_y - self.y, playstate.player.mid_x - self.x)
                if playstate.player.map_x == playstate.player.end_of_left or playstate.player.map_x == playstate.player.end_of_right:
                    self.x += RUN_SPEED_PPS * math.cos(self.dir)*game_framework.frame_time
                else:
                    if playstate.player.injury_status == True:
                        self.x += RUN_SPEED_PPS * math.cos(self.dir)*game_framework.frame_time - playstate.player.dir_x*isaac.INJURY_SPEED_PPS*game_framework.frame_time
                    else:
                        self.x += RUN_SPEED_PPS * math.cos(self.dir)*game_framework.frame_time - playstate.player.dir_x*isaac.RUN_SPEED_PPS*game_framework.frame_time

                if playstate.player.map_y == playstate.player.end_of_top or playstate.player.map_y == playstate.player.end_of_bottom:
                    self.y += RUN_SPEED_PPS * math.sin(self.dir) * game_framework.frame_time
                else:
                    if playstate.player.injury_status == True:
                        self.y += RUN_SPEED_PPS * math.sin(self.dir) * game_framework.frame_time - playstate.player.dir_y*isaac.INJURY_SPEED_PPS*game_framework.frame_time
                    else:
                        self.y += RUN_SPEED_PPS * math.sin(self.dir) * game_framework.frame_time - playstate.player.dir_y*isaac.RUN_SPEED_PPS*game_framework.frame_time
            else:
                if playstate.player.map_x != playstate.player.end_of_left and playstate.player.map_x != playstate.player.end_of_right:
                    if playstate.player.injury_status == True:
                        self.x -= playstate.player.dir_x*isaac.INJURY_SPEED_PPS*game_framework.frame_time
                    else:
                        self.x -= playstate.player.dir_x * isaac.RUN_SPEED_PPS * game_framework.frame_time
                if playstate.player.map_y != playstate.player.end_of_top and playstate.player.map_y != playstate.player.end_of_bottom:
                    if playstate.player.injury_status == True:
                        self.y -= playstate.player.dir_y*isaac.INJURY_SPEED_PPS*game_framework.frame_time
                    else:
                        self.y -= playstate.player.dir_y * isaac.RUN_SPEED_PPS * game_framework.frame_time

        if self.pattern_status == False:
            self.choose_pattern = random.randint(1,10)
            #self.choose_pattern = 9
            #self.choose_pattern = 10
            self.pattern_status = True

        if self.pattern_status == True:
            if 1 <= self.choose_pattern <= 5:
                self.frame = self.pattern_1[self.frame_cnt_in_pattern_list]

                # 패턴 프레임 속도
                if self.frame == 7:
                    self.frame_count += 1
                else:
                    self.frame_count += 5
                if self.frame_count == 50:
                    self.frame_cnt_in_pattern_list += 1
                    self.frame_count = 0
                # 패턴 끝
                if self.frame_cnt_in_pattern_list == 6:
                    self.frame_cnt_in_pattern_list = 0
                    self.frame = 0
                    self.pattern_status = False

            elif 6 <= self.choose_pattern <= 7:
                self.frame = self.pattern_2[self.frame_cnt_in_pattern_list]
                # 패턴 프레임 속도
                self.frame_count += 1
                if self.frame_count == 50:
                    self.frame_cnt_in_pattern_list += 1
                    self.frame_count = 0
                # 패턴 끝
                if self.frame_cnt_in_pattern_list == 2:
                    self.frame_cnt_in_pattern_list = 0
                    self.frame = 0
                    self.pattern_status = False

            elif 8 <= self.choose_pattern <= 10:
                self.frame = self.pattern_3[self.frame_cnt_in_pattern_list]
                self.frame_count += 1
                if self.attack_status == False:
                    monster_tears = [Monster_Attack() for i in range(8)]
                    game_world.add_objects(monster_tears, 3)
                    for tear in monster_tears:
                        tear.dir = self.tear_num % 8
                        tear.x = self.x
                        tear.y = self.y
                        self.tear_num += 1
                    game_world.add_collision_pairs(monster_tears, None, 'monster_tears:player')

                    self.attack_status = True

                if self.frame_count == 100:
                    self.frame_cnt_in_pattern_list += 1
                    self.frame_count = 0
                if self.frame_cnt_in_pattern_list == 1:
                    self.frame_cnt_in_pattern_list = 0
                    self.frame = 0
                    #self.tear_num = 0
                    self.pattern_status = False
                    self.attack_status = False


        # self.frame_count += 1
        # if self.frame_count == 10:
        #     self.frame = (self.frame + 1) % 9
        #     self.frame_count = 0
        #     pass

    def draw(self):
        if self.status == True:
            if self.x >= MAP_WIDTH//2: # 스프라이트 좌우 방향
                if self.frame <= 4:
                    self.image.clip_composite_draw(self.frame * 80, 253, self.WID, self.HEI,
                                                   0, '', self.x, self.y, self.size,
                                                   self.size)
                else:
                    self.image.clip_composite_draw((self.frame - 5) * 80, 143, self.WID,
                                                   self.HEI,
                                                   0, '', self.x, self.y, self.size,
                                                   self.size)
            else:
                if self.frame <= 4:
                    self.image.clip_composite_draw(self.frame * 80, 253, self.WID, self.HEI,
                                               3.141592, 'v', self.x, self.y, self.size,
                                               self.size)
                else:
                    self.image.clip_composite_draw((self.frame-5) * 80, 143, self.WID, self.HEI,
                                                   3.141592, 'v', self.x, self.y, self.size,
                                                   self.size)
            # draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 40*(self.size//100), self.y - 45*(self.size//100), \
               self.x + 40*(self.size//100), self.y + 45*(self.size//100)

    def handle_collision(self, other, group):
        if group == 'tears:monstros':
            self.hp -= attack.attack_damage
            if self.hp <= 0:
                isaac.boss_kill_cnt += 1
                game_world.remove_object(self)
                #self.status = False
        if group == 'player:monstros':
            if other.injury_status == False:
                self.hp -= playstate.player.damage
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
                    print('remove')
                    isaac.boss_kill_cnt += 1
                    game_world.remove_object(self)
                    #self.status = False







