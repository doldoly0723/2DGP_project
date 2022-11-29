from pico2d import*
import isaac
import attack
import random   # 몬스터의 출현
import playstate

PIXEL_PER_METER = (10.0 / 0.1)  #10 pixel 10cm
RUN_SPEED_KMPH = 15.0   #Km / Hour

RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

MAP_WIDTH, MAP_HEIGHT = 1600, 900
class Spitty:
    image = None
    def __init__(self):
        self.WID = 64
        self.HEI = 64

        self.monster_t = 0

        self.x = 0
        self.y = 0
        self.monster_status = False  # 현재 존재하는가
        if Spitty.image == None:
            Spitty.image = load_image('spitty.png')

        self.frame = 0
        self.frame_count = 0

        self.choose_wall = 0 # 리스폰 지역 설정

        self.hp = 300

        # 플레이어와 몬스터의 위치 비교
        self.compare_x = 0
        self.compare_y = 0

        self.size = 100

        self.mid_x = MAP_WIDTH // 2
        self.mid_y = MAP_HEIGHT // 2

        self.end_of_left = 65
        self.end_of_right = 4800
        self.end_of_top = 2725
        self.end_of_bottom = 0

    def respawn_monster(self):
        if self.monster_status == False:
            Spitty.__init__(self) # 초기화
        if 1 == random.randint(0, 500): #랜덤한 시간으로 몬스터를 생성 난이도 상승시 범위도 같이 높여야 한다
            if self.monster_status == False:
                self.choose_wall = random.randint(1, 4)
                #self.sucker_status = 1
                #초기화 작업
                self.hp = 300
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
                self.x = 200
                self.y = 550
                self.monster_status = True
        # self.sucker_x = 0
        # self.sucker_y = 0

        pass

    def monster_player_compare_x(self):
        if playstate.player.map_x == self.end_of_left or playstate.player.map_x == self.end_of_right:
            return 1    # 플레이어가 테두리에 있을때
        else:
            return 2
    def monster_player_compare_y(self):
        if playstate.player.map_y == self.end_of_top or playstate.player.map_y == self.end_of_bottom:
            return 1    # 플레이어가 테두리에 있을 떄
        else:
            return 2

    def update(self):
        Spitty.respawn_monster(self)
        if self.monster_status == True:
            self.compare_x = self.x - self.mid_x
            self.compare_y = self.y - self.mid_y
            #몬스터는 x or y축 방향으로만 이동 가능
            if self.compare_x >= 0 and self.compare_y >= 0:   # 1사분면
                if abs(self.compare_x) >= abs(self.compare_y):
                    if self.monster_player_compare_x() == 1:
                        self.x = self.x - 2
                        self.y = self.y - playstate.player.dir_y * 5
                    elif self.monster_player_compare_x() == 2:
                        self.x = (self.x - 2) - playstate.player.dir_x * 5
                        if self.monster_player_compare_y() == 2:
                            self.y = self.y - playstate.player.dir_y * 5
                else:
                    if self.monster_player_compare_y() == 1:
                        self.y = self.y - 2
                        self.x = self.x - playstate.player.dir_x * 5
                    elif self.monster_player_compare_y() == 2:
                        self.y = self.y - 2 - playstate.player.dir_y * 5
                        if self.monster_player_compare_x() == 2:
                            self.x = self.x - playstate.player.dir_x * 5


            elif self.compare_x >= 0 and self.compare_y <= 0: # 4사분면
                if abs(self.compare_x) >= abs(self.compare_y):
                    if self.monster_player_compare_x() == 1:
                        self.x = self.x - 2
                        self.y = self.y - playstate.player.dir_y * 5
                    elif self.monster_player_compare_x() == 2:
                        self.x = self.x - 2 - playstate.player.dir_x * 5
                        if self.monster_player_compare_y() == 2:
                            self.y = self.y - playstate.player.dir_y * 5
                else:
                    if self.monster_player_compare_y() == 1:
                        self.y = self.y + 2
                        self.x = self.x - playstate.player.dir_x * 5
                    elif self.monster_player_compare_y() == 2:
                        self.y = self.y + 2 - playstate.player.dir_y * 5
                        if self.monster_player_compare_x() == 2:
                            self.x = self.x - playstate.player.dir_x * 5

            elif self.compare_x <= 0 and self.compare_y <= 0: # 3사분면
                if abs(self.compare_x) >= abs(self.compare_y):
                    if self.monster_player_compare_x() == 1:
                        self.x = self.x + 2
                        self.y = self.y - playstate.player.dir_y * 5
                    elif self.monster_player_compare_x() == 2:
                        self.x = (self.x + 2) - playstate.player.dir_x * 5
                        if self.monster_player_compare_y() == 2:
                            self.y = self.y - playstate.player.dir_y * 5
                else:
                    if self.monster_player_compare_y() == 1:
                        self.y = self.y + 2
                        self.x = self.x - playstate.player.dir_x * 5
                    elif self.monster_player_compare_y() == 2:
                        self.y = (self.y + 2) - playstate.player.dir_y * 5
                        if self.monster_player_compare_x() == 2:
                            self.x = self.x - playstate.player.dir_x * 5

            elif self.compare_x <= 0 and self.compare_y >= 0: # 2사분면
                if abs(self.compare_x) >= abs(self.compare_y):
                    if self.monster_player_compare_x() == 1:
                        self.x = self.x + 2
                        self.y = self.y - playstate.player.dir_y * 5
                    elif self.monster_player_compare_x() == 2:
                        self.x = self.x + 2 - playstate.player.dir_x * 5
                        if self.monster_player_compare_y() == 2:
                            self.y = self.y - playstate.player.dir_y * 5

                else:
                    if self.monster_player_compare_y() == 1:
                        self.y = self.y - 2
                        self.x = self.x - playstate.player.dir_x * 5
                    elif self.monster_player_compare_y() == 2:
                        self.y = self.y - 2 - playstate.player.dir_y * 5
                        if self.monster_player_compare_x() == 2:
                            self.x = self.x - playstate.player.dir_x * 5



        # 프레임 속도
        self.frame_count += 1
        if self.frame_count == 10:
            self.frame = (self.frame + 1) % 4
            self.frame_count = 0

    def draw(self):
        if self.monster_status == True:
            self.compare_x = self.x - self.mid_x
            self.compare_y = self.y - self.mid_y

            if self.compare_x >= 0 and self.compare_y >= 0:  # 1사분면
                if self.compare_x >= self.compare_y:
                    self.image.clip_composite_draw(self.frame * 64, 64 * 3, self.WID, self.HEI,
                                                           3.141592, 'v', self.x, self.y, self.size, self.size)
                else:
                    self.image.clip_composite_draw(self.frame * 64, 64 * 1, self.WID,
                                                           self.HEI,
                                                           0, '', self.x, self.y, self.size, self.size)

            elif self.compare_x >= 0 and self.compare_y <= 0:  # 4사분면
                if abs(self.compare_x) >= abs(self.compare_y):
                    self.image.clip_composite_draw(self.frame * 64, 64 * 3, self.WID,
                                                           self.HEI,
                                                           3.141592, 'v', self.x, self.y, self.size,
                                                           self.size)
                else:
                    self.image.clip_composite_draw(self.frame * 64, 64 * 2, self.WID,
                                                           self.HEI,
                                                           0, '', self.x, self.y, self.size,
                                                           self.size)

            elif self.compare_x <= 0 and self.compare_y <= 0:  # 3사분면
                if abs(self.compare_x) >= abs(self.compare_y):
                    self.image.clip_composite_draw(self.frame * 64, 64 * 3, self.WID,
                                                           self.HEI,
                                                           0, '', self.x, self.y, self.size,
                                                           self.size)
                else:
                    self.image.clip_composite_draw(self.frame * 64, 64 * 2, self.WID,
                                                           self.HEI,
                                                           0, '', self.x, self.y, self.size,
                                                           self.size)

            elif self.compare_x <= 0 and self.compare_y >= 0:  # 2사분면
                if abs(self.compare_x) >= abs(self.compare_y):
                    self.image.clip_composite_draw(self.frame * 64, 64 * 3, self.WID,
                                                           self.HEI,
                                                           0, '', self.x, self.y, self.size,
                                                           self.size)
                else:
                    self.image.clip_composite_draw(self.frame * 64, 64 * 1, self.WID,
                                                           self.HEI,
                                                           0, '', self.x, self.y, self.size,
                                                           self.size)
            # draw_rectangle(*self.get_bb())


    def get_bb(self):
        return self.x - 32, self.y - 22, self.x + 32, self.y + 22

    def handle_collision(self, other, group):
        if group == 'tears:spittys':
            self.hp -= attack.attack_damage
            if self.hp <= 0:
                isaac.kill_cnt += 1
                self.monster_status = False

        if group == 'player:spittys':
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
                    isaac.kill_cnt += 1     #보스 출현을 위한 kill cnt
                    self.monster_status = False






