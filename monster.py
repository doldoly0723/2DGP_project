from pico2d import*

import attack
import isaac
import random   # 몬스터의 출현
import playstate
MAP_WIDTH, MAP_HEIGHT = 1600, 900
class Sucker:
    image = None
    reverse_image = None
    def __init__(self):
        self.monster_WID = 80
        self.monster_HEI = 80

        self.monster_t = 0

        self.monster_x = 0
        self.monster_y = 0
        self.monster_status = False  # 현재 존재하는가

        if Sucker.image == None:
            Sucker.image = load_image('sucker.png')
        if Sucker.reverse_image == None:
            Sucker.reverse_image = load_image('sucker_reverse.png')
        self.monster_frame = 0
        self.frame_count = 0

        self.reverse_x = MAP_WIDTH//2

        self.choose_wall = 0 # 리스폰 지역 설정

        self.monster_hp = 200

    def respawn_sucker(self):
        if self.monster_status == False:
            Sucker.__init__(self) # 초기화
        if 1 == random.randint(0, 500): #랜덤한 시간으로 몬스터를 생성 난이도 상승시 범위도 같이 높여야 한다
            if self.monster_status == False:
                self.choose_wall = random.randint(0, 5)
                #self.sucker_status = 1
                #초기화 작업
                self.monster_hp = 200
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

    def update(self):
        Sucker.respawn_sucker(self)
        if self.monster_status == True:
            self.monster_t += 0.00001
            if playstate.player.map_x == playstate.player.end_of_left or playstate.player.map_x == playstate.player.end_of_right:
                self.monster_x = ((1 - self.monster_t) * self.monster_x + self.monster_t * playstate.player.mid_x)
            else:
                self.monster_x = ((1-self.monster_t)*self.monster_x + self.monster_t*playstate.player.mid_x) - playstate.player.dir_x*5

            if playstate.player.map_y == playstate.player.end_of_top or playstate.player.map_y == playstate.player.end_of_bottom:
                self.monster_y = ((1 - self.monster_t) * self.monster_y + self.monster_t * playstate.player.mid_y)
            else:
                self.monster_y = ((1-self.monster_t)*self.monster_y + self.monster_t*playstate.player.mid_y) - playstate.player.dir_y*5

        self.frame_count += 1
        if self.frame_count == 10:
            self.monster_frame = (self.monster_frame + 1) % 2
            self.frame_count = 0
            pass

    def draw(self):
        if self.monster_status == True:
            if self.monster_x <= self.reverse_x: # sucker 스프라이트 좌우 방향
                self.image.clip_draw(self.monster_frame*80, 0,
                                        self.monster_WID, self.monster_HEI, self.monster_x, self.monster_y)
            else:
                self.reverse_image.clip_draw(self.monster_frame * 80, 0,
                                            self.monster_WID, self.monster_HEI, self.monster_x, self.monster_y)
            draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.monster_x - 30, self.monster_y - 40, self.monster_x + 30, self.monster_y + 30

    def handle_collision(self, other, group):
        if group == 'tears:suckers':
            self.monster_hp -= playstate.player.damege
            if self.monster_hp <= 0:
                self.monster_status = False
        if group == 'player:suckers':
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






