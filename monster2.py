from pico2d import*
import isaac
import attack
import random   # 몬스터의 출현
import playstate

MAP_WIDTH, MAP_HEIGHT = 1600, 900
class Spitty:
    image = None
    def __init__(self):
        self.monster_WID = 64
        self.monster_HEI = 64

        self.monster_t = 0

        self.monster_x = 0
        self.monster_y = 0
        self.monster_status = False  # 현재 존재하는가
        if Spitty.image == None:
            Spitty.image = load_image('spitty.png')

        self.monster_frame = 0
        self.frame_count = 0

        self.choose_wall = 0 # 리스폰 지역 설정

        self.monster_hp = 300

        self.compare_x = 0
        self.compare_y = 0

        self.monster_size = 100

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
                self.choose_wall = random.randint(0, 5)
                #self.sucker_status = 1
                #초기화 작업
                self.monster_hp = 300
                self.monster_t = 0
                if self.choose_wall == 1:   #밑에 지역
                    self.monster_x = random.randint(0, MAP_WIDTH)
                    self.monster_y = 0
                elif self.choose_wall == 2: #위 지역
                    self.monster_x = random.randint(0, MAP_WIDTH)
                    self.monster_y = MAP_HEIGHT
                elif self.choose_wall == 3: #왼쪽
                    self.monster_x = 0
                    self.monster_y = random.randint(0, MAP_HEIGHT)
                elif self.choose_wall == 4: #오른쪽
                    self.monster_x = MAP_WIDTH
                    self.monster_y = random.randint(0, MAP_HEIGHT)
                self.monster_status = True
        # self.sucker_x = 0
        # self.sucker_y = 0

        pass

    def monster_player_compare_x(self):
        if playstate.player.map_x == self.end_of_left or playstate.player.map_x == self.end_of_right:
            return 1    # 테두리에 있을때
        else:
            return 2
    def monster_player_compare_y(self):
        if playstate.player.map_y == self.end_of_top or playstate.player.map_y == self.end_of_bottom:
            return 1    # 테두리에 있을 떄
        else:
            return 2

    def update(self):
        Spitty.respawn_monster(self)
        if self.monster_status == True:

            self.compare_x = self.monster_x - self.mid_x
            self.compare_y = self.monster_y - self.mid_y
            #몬스터는 x or y축 방향으로만 이동 가능
            if self.compare_x >= 0 and self.compare_y >= 0:   # 1사분면
                if self.compare_x >= self.compare_y:
                    if self.monster_player_compare_x() == 1:
                        self.monster_x = self.monster_x - 2
                    elif self.monster_player_compare_x() == 2:
                        self.monster_x = (self.monster_x - 2) - playstate.player.dir_x * 5
                        self.monster_y = self.monster_y - playstate.player.dir_y * 5

                else:
                    if self.monster_player_compare_y() == 1:
                        self.monster_y = self.monster_y - 2
                    elif self.monster_player_compare_y() == 2:
                        self.monster_y = self.monster_y - 2 - playstate.player.dir_y * 5
                        self.monster_x = self.monster_x - playstate.player.dir_x * 5


            elif self.compare_x >= 0 and self.compare_y <= 0: # 4사분면
                if abs(self.compare_x) >= abs(self.compare_y):
                    if self.monster_player_compare_x() == 1:
                        self.monster_x = self.monster_x - 2
                    elif self.monster_player_compare_x() == 2:
                        self.monster_x = self.monster_x - 2 - playstate.player.dir_x * 5
                        self.monster_y = self.monster_y - playstate.player.dir_y * 5
                else:
                    if self.monster_player_compare_y() == 1:
                        self.monster_y = self.monster_y + 2
                    elif self.monster_player_compare_y() == 2:
                        self.monster_y = self.monster_y + 2 - playstate.player.dir_y * 5
                        self.monster_x = self.monster_x - playstate.player.dir_x * 5

            elif self.compare_x <= 0 and self.compare_y <= 0: # 3사분면
                if abs(self.compare_x) >= abs(self.compare_y):
                    if self.monster_player_compare_x() == 1:
                        self.monster_x = self.monster_x + 2
                    elif self.monster_player_compare_x() == 2:
                        self.monster_x = (self.monster_x + 2) - playstate.player.dir_x * 5
                        self.monster_y = self.monster_y - playstate.player.dir_y * 5
                else:
                    if self.monster_player_compare_y() == 1:
                        self.monster_y = self.monster_y + 2
                    elif self.monster_player_compare_y() == 2:
                        self.monster_y = (self.monster_y + 2) - playstate.player.dir_y * 5
                        self.monster_x = self.monster_x - playstate.player.dir_x * 5

            elif self.compare_x <= 0 and self.compare_y >= 0: # 2사분면
                if abs(self.compare_x) >= abs(self.compare_y):
                    if self.monster_player_compare_x() == 1:
                        self.monster_x = self.monster_x + 2
                    elif self.monster_player_compare_x() == 2:
                        self.monster_x = self.monster_x + 2 - playstate.player.dir_x * 5
                        self.monster_y = self.monster_y - playstate.player.dir_y * 5

                else:
                    if self.monster_player_compare_y() == 1:
                        self.monster_y = self.monster_y - 2
                    elif self.monster_player_compare_y() == 2:
                        self.monster_y = self.monster_y - 2 - playstate.player.dir_y * 5
                        self.monster_x = self.monster_x - playstate.player.dir_x * 5

            # self.monster_x = ((1-self.monster_t)*self.monster_x + self.monster_t*playstate.player.mid_x) - playstate.player.dir_x*5
            # self.monster_y = ((1-self.monster_t)*self.monster_y + self.monster_t*playstate.player.mid_y) - playstate.player.dir_y*5
            #if self.sucker_t > 1.0:


        # 프레임 속도
        self.frame_count += 1
        if self.frame_count == 10:
            self.monster_frame = (self.monster_frame + 1) % 4
            self.frame_count = 0

    def draw(self):
        if self.monster_status == True:
            self.compare_x = self.monster_x - self.mid_x
            self.compare_y = self.monster_y - self.mid_y

            if self.compare_x >= 0 and self.compare_y >= 0:  # 1사분면
                if self.compare_x >= self.compare_y:
                    self.image.clip_composite_draw(self.monster_frame * 64, 64 * 3, self.monster_WID, self.monster_HEI,
                                                           3.141592, 'v', self.monster_x, self.monster_y, self.monster_size, self.monster_size)
                else:
                    self.image.clip_composite_draw(self.monster_frame * 64, 64 * 1, self.monster_WID,
                                                           self.monster_HEI,
                                                           0, '', self.monster_x, self.monster_y, self.monster_size, self.monster_size)

            elif self.compare_x >= 0 and self.compare_y <= 0:  # 4사분면
                if abs(self.compare_x) >= abs(self.compare_y):
                    self.image.clip_composite_draw(self.monster_frame * 64, 64 * 3, self.monster_WID,
                                                           self.monster_HEI,
                                                           3.141592, 'v', self.monster_x, self.monster_y, self.monster_size,
                                                           self.monster_size)
                else:
                    self.image.clip_composite_draw(self.monster_frame * 64, 64 * 2, self.monster_WID,
                                                           self.monster_HEI,
                                                           0, '', self.monster_x, self.monster_y, self.monster_size,
                                                           self.monster_size)

            elif self.compare_x <= 0 and self.compare_y <= 0:  # 3사분면
                if abs(self.compare_x) >= abs(self.compare_y):
                    self.image.clip_composite_draw(self.monster_frame * 64, 64 * 3, self.monster_WID,
                                                           self.monster_HEI,
                                                           0, '', self.monster_x, self.monster_y, self.monster_size,
                                                           self.monster_size)
                else:
                    self.image.clip_composite_draw(self.monster_frame * 64, 64 * 2, self.monster_WID,
                                                           self.monster_HEI,
                                                           0, '', self.monster_x, self.monster_y, self.monster_size,
                                                           self.monster_size)

            elif self.compare_x <= 0 and self.compare_y >= 0:  # 2사분면
                if abs(self.compare_x) >= abs(self.compare_y):
                    self.image.clip_composite_draw(self.monster_frame * 64, 64 * 3, self.monster_WID,
                                                           self.monster_HEI,
                                                           0, '', self.monster_x, self.monster_y, self.monster_size,
                                                           self.monster_size)
                else:
                    self.image.clip_composite_draw(self.monster_frame * 64, 64 * 1, self.monster_WID,
                                                           self.monster_HEI,
                                                           0, '', self.monster_x, self.monster_y, self.monster_size,
                                                           self.monster_size)
            draw_rectangle(*self.get_bb())
            # if self.monster_x <= playstate.player.mid_x: # sucker 스프라이트 좌우 방향
            #     self.monster_image.clip_draw(self.monster_frame*80, 0,
            #                             self.monster_WID, self.monster_HEI, self.monster_x, self.monster_y)
            # else:
            #     self.sucker_reverse_image.clip_draw(self.monster_frame * 80, 0,
            #                                 self.monster_WID, self.monster_HEI, self.monster_x, self.monster_y)


    def get_bb(self):
        return self.monster_x - 32, self.monster_y - 22, self.monster_x + 32, self.monster_y + 22

    def handle_collision(self, other, group):
        if group == 'tears:spittys':
            self.monster_hp -= playstate.player.damege
            if self.monster_hp <= 0:
                self.monster_status = False

        if group == 'player:spittys':
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
                    self.monster_status = False

monster = None

# def enter():
#     global monster
#     # 현재 10개체 생성 난이도 상승시 개체수 상승 난이도 상승을 개채를 더할것인지 랜덤 범위를 줄일것인지
#     monster = [Sucker() for i in range(5)]
#
# def exit():
#     global monster
#     del monster
# def update():
#     global monster
#     for sucker in monster:
#         sucker.respawn_sucker()
#         sucker.update()
# def draw():
#     global monster
#     for sucker in monster:
#         sucker.draw()
#






