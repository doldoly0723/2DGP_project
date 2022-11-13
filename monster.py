from pico2d import*
import isaac
import random   # 몬스터의 출현
import playstate
MAP_WIDTH, MAP_HEIGHT = 1600, 900
class Sucker:
    def __init__(self):
        self.monster_WID = 80
        self.monster_HEI = 80

        self.monster_t = 0

        self.monster_x = 0
        self.monster_y = 0
        self.monster_status = False  # 현재 존재하는가

        self.monster_image = load_image('sucker.png')
        self.sucker_reverse_image = load_image('sucker_reverse.png')
        self.monster_frame = 0
        self.frame_count = 0

        self.reverse_x = MAP_WIDTH//2

        self.choose_wall = 0 # 리스폰 지역 설정

        self.monster_hp = 100
        pass

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
                    self.monster_x = random.randint(0,isaac.MAP_WIDTH)
                    self.monster_y = 0
                elif self.choose_wall == 2: #위 지역
                    self.monster_x = random.randint(0,isaac.MAP_WIDTH)
                    self.monster_y = isaac.MAP_HEIGHT
                elif self.choose_wall == 3: #왼쪽
                    self.monster_x = 0
                    self.monster_y = random.randint(0,isaac.MAP_HEIGHT)
                elif self.choose_wall == 4: #오른쪽
                    self.monster_x = isaac.MAP_WIDTH
                    self.monster_y = random.randint(0,isaac.MAP_HEIGHT)
                self.monster_status = True
        # self.sucker_x = 0
        # self.sucker_y = 0

        pass

    def update(self):
        Sucker.respawn_sucker(self)
        if self.monster_status == True:
            self.monster_t += 0.00001
            self.monster_x = ((1-self.monster_t)*self.monster_x + self.monster_t*playstate.player.mid_x) - playstate.player.dir_x*5
            self.monster_y = ((1-self.monster_t)*self.monster_y + self.monster_t*playstate.player.mid_y) - playstate.player.dir_y*5
            #if self.sucker_t > 1.0:


        self.frame_count += 1
        if self.frame_count == 10:
            self.monster_frame = (self.monster_frame + 1) % 2
            self.frame_count = 0
            pass

    def draw(self):
        if self.monster_status == True:
            if self.monster_x <= self.reverse_x: # sucker 스프라이트 좌우 방향
                self.monster_image.clip_draw(self.monster_frame*80, 0,
                                        self.monster_WID, self.monster_HEI, self.monster_x, self.monster_y)
            else:
                self.sucker_reverse_image.clip_draw(self.monster_frame * 80, 0,
                                            self.monster_WID, self.monster_HEI, self.monster_x, self.monster_y)
        pass

    def take_damage(self):
        pass


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






