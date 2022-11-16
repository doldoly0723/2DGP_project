from pico2d import*

import attack
import game_world
import isaac
import random   # 몬스터의 출현
import playstate
MAP_WIDTH, MAP_HEIGHT = 1600, 900
class Monstro:
    image = None
    reverse_image = None
    def __init__(self):
        self.monster_WID = 80
        self.monster_HEI = 90

        self.monster_t = 0

        self.monster_x = 0
        self.monster_y = 0
        self.monster_status = False  # 현재 존재하는가

        if Monstro.image == None:
            Monstro.image = load_image('Monstro.png')
        self.monster_frame = 0
        self.frame_count = 0

        self.choose_wall = 0 # 리스폰 지역 설정

        self.monster_hp = 200
        self.monster_size = 200

        self.choose_pattern = None
        self.pattern_status = False
        self.pattern_1 =[5,6,7,4,5,8]   # 패턴 프레임 순서
        self.pattern_2 = [1,2]          # 패턴 프레임 순서
        self.frame_cnt = 0 # 리스트 안의 프레임 번호

    def respawn_monstro(self):
        if self.monster_status == False:
            Monstro.__init__(self)
            self.choose_wall = random.randint(1, 4)
            #self.sucker_status = 1
            #초기화 작업
            self.monster_hp = 3000
            self.monster_t = 0
            if self.choose_wall == 1:   #밑에 지역
                self.monster_x = random.randint(0, MAP_WIDTH)
                self.monster_y = 0 - 100
            elif self.choose_wall == 2: #위 지역
                self.monster_x = random.randint(0, MAP_WIDTH)
                self.monster_y = MAP_HEIGHT + 100
            elif self.choose_wall == 3: #왼쪽
                self.monster_x = 0 - 100
                self.monster_y = random.randint(0, MAP_HEIGHT)
            elif self.choose_wall == 4: #오른쪽
                self.monster_x = MAP_WIDTH + 100
                self.monster_y = random.randint(0, MAP_HEIGHT)
            self.monster_status = True

    def update(self):
        Monstro.respawn_monstro(self)
        if self.monster_status == True:
            if self.monster_frame == 7:
                #self.monster_t += 0.00005  # 시간 지날수록 속도 증가
                self.monster_t = 0.02   # monstro 속도 고정
                if playstate.player.map_x == playstate.player.end_of_left or playstate.player.map_x == playstate.player.end_of_right:
                    self.monster_x = ((1 - self.monster_t) * self.monster_x + self.monster_t * playstate.player.mid_x)
                else:
                    self.monster_x = ((1-self.monster_t)*self.monster_x + self.monster_t*playstate.player.mid_x) - playstate.player.dir_x*5

                if playstate.player.map_y == playstate.player.end_of_top or playstate.player.map_y == playstate.player.end_of_bottom:
                    self.monster_y = ((1 - self.monster_t) * self.monster_y + self.monster_t * playstate.player.mid_y)
                else:
                    self.monster_y = ((1-self.monster_t)*self.monster_y + self.monster_t*playstate.player.mid_y) - playstate.player.dir_y*5
            else:
                self.monster_x -= playstate.player.dir_x*5
                self.monster_y -= playstate.player.dir_y*5
        print(self.monster_t)
        if self.pattern_status == False:
            self.choose_pattern = random.randint(1,10)
            #self.choose_pattern = 2
            self.pattern_status = True

        if self.pattern_status == True:
            if 1 <= self.choose_pattern <= 7:
                self.monster_frame = self.pattern_1[self.frame_cnt]

                # 패턴 프레임 속도
                if self.monster_frame == 7:
                    self.frame_count += 1
                else:
                    self.frame_count += 5
                if self.frame_count == 50:
                    self.frame_cnt += 1
                    self.frame_count = 0
                # 패턴 끝
                if self.frame_cnt == 6:
                    self.frame_cnt = 0
                    self.monster_frame = 0
                    self.pattern_status = False

            elif 7 <= self.choose_pattern <= 10:
                self.monster_frame = self.pattern_2[self.frame_cnt]
                # 패턴 프레임 속도
                self.frame_count += 1
                if self.frame_count == 50:
                    self.frame_cnt += 1
                    self.frame_count = 0
                # 패턴 끝
                if self.frame_cnt == 2:
                    self.frame_cnt = 0
                    self.monster_frame = 0
                    self.pattern_status = False


        # self.frame_count += 1
        # if self.frame_count == 10:
        #     self.monster_frame = (self.monster_frame + 1) % 9
        #     self.frame_count = 0
        #     pass

    def draw(self):
        if self.monster_status == True:
            if self.monster_x >= MAP_WIDTH//2: # 스프라이트 좌우 방향
                if self.monster_frame <= 4:
                    self.image.clip_composite_draw(self.monster_frame * 80, 253, self.monster_WID, self.monster_HEI,
                                                   0, '', self.monster_x, self.monster_y, self.monster_size,
                                                   self.monster_size)
                else:
                    self.image.clip_composite_draw((self.monster_frame - 5) * 80, 143, self.monster_WID,
                                                   self.monster_HEI,
                                                   0, '', self.monster_x, self.monster_y, self.monster_size,
                                                   self.monster_size)
            else:
                if self.monster_frame <= 4:
                    self.image.clip_composite_draw(self.monster_frame * 80, 253, self.monster_WID, self.monster_HEI,
                                               3.141592, 'v', self.monster_x, self.monster_y, self.monster_size,
                                               self.monster_size)
                else:
                    self.image.clip_composite_draw((self.monster_frame-5) * 80, 143, self.monster_WID, self.monster_HEI,
                                                   3.141592, 'v', self.monster_x, self.monster_y, self.monster_size,
                                                   self.monster_size)
            draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.monster_x - 40*(self.monster_size//100), self.monster_y - 45*(self.monster_size//100), \
               self.monster_x + 40*(self.monster_size//100), self.monster_y + 45*(self.monster_size//100)

    def handle_collision(self, other, group):
        if group == 'tears:monstros':
            self.monster_hp -= playstate.player.damege
            if self.monster_hp <= 0:
                game_world.remove_object(self)
                #self.monster_status = False
        if group == 'player:monstros':
            if other.injury_status == False:
                self.monster_hp -= attack.Attack().attack_damage
                print(self.get_bb())
                print(other.get_bb())
                la, ba, ra, ta = self.get_bb()
                lb, bb, rb, tb = other.get_bb()

                if la < rb and tb - ba > 5 and ta - bb > 5 and ra - lb > 5:
                    self.monster_x += 100
                elif ra > lb and tb - ba > 5 and ta - bb > 5 and rb - la > 5:
                    self.monster_x -= 100
                elif ta > bb and tb - ba > 5:
                    self.monster_y -= 100
                elif ba < tb:
                    self.monster_y += 100

                playstate.player.injury_status = True
                if self.monster_hp <= 0:
                    print('remove')
                    game_world.remove_object(self)
                    #self.monster_status = False







