from pico2d import*
import isaac
import random   # 몬스터의 출현
MAP_WIDTH, MAP_HEIGHT = 1600, 900
class Sucker:
    def __init__(self):
        self.sucker_WID = 80
        self.sucker_HEI = 80
        self.sucker_t = 0
        self.sucker_x = 0
        self.sucker_y = 0
        self.sucker_status = False  # 현재 존재하는가
        self.sucker_image = load_image('sucker.png')
        self.sucker_reverse_image = load_image('sucker_reverse.png')
        self.sucker_frame = 0
        self.frame_count = 0

        self.reverse_x = MAP_WIDTH//2

        self.choose_wall = 0 # 리스폰 지역 설정

        self.sucker_hp = 200
        pass

    def respawn_sucker(self):
        if 1 == random.randint(0, 1000): #랜덤한 시간으로 몬스터를 생성 난이도 상승시 범위도 같이 높여야 한다
            if self.sucker_status == False:
                self.choose_wall = random.randint(0, 5)
                #self.sucker_status = 1
                #초기화 작업
                self.sucker_hp = 200
                self.sucker_t = 0
                if self.choose_wall == 1:   #밑에 지역
                    self.sucker_x = random.randint(0,isaac.MAP_WIDTH)
                    self.sucker_y = 0
                elif self.choose_wall == 2: #위 지역
                    self.sucker_x = random.randint(0,isaac.MAP_WIDTH)
                    self.sucker_y = isaac.MAP_HEIGHT
                elif self.choose_wall == 3: #왼쪽
                    self.sucker_x = 0
                    self.sucker_y = random.randint(0,isaac.MAP_HEIGHT)
                elif self.choose_wall == 4: #오른쪽
                    self.sucker_x = isaac.MAP_WIDTH
                    self.sucker_y = random.randint(0,isaac.MAP_HEIGHT)
                self.sucker_status = True
        # self.sucker_x = 0
        # self.sucker_y = 0

        pass

    def update(self):
        if self.sucker_status == True:
            self.sucker_t += 0.00001
            self.sucker_x = ((1-self.sucker_t)*self.sucker_x + self.sucker_t*isaac.map.mid_x) - isaac.dir_x*5
            self.sucker_y = ((1-self.sucker_t)*self.sucker_y + self.sucker_t*isaac.map.mid_y) - isaac.dir_y*5
            #if self.sucker_t > 1.0:


        self.frame_count += 1
        if self.frame_count == 10:
            self.sucker_frame = (self.sucker_frame + 1) % 2
            self.frame_count = 0
            pass

    def draw(self):
        if self.sucker_status == True:
            if self.sucker_x <= self.reverse_x: # sucker 스프라이트 좌우 방향
                self.sucker_image.clip_draw(self.sucker_frame*80, 0,
                                        self.sucker_WID, self.sucker_HEI, self.sucker_x, self.sucker_y)
            else:
                self.sucker_reverse_image.clip_draw(self.sucker_frame * 80, 0,
                                            self.sucker_WID, self.sucker_HEI, self.sucker_x, self.sucker_y)
        pass

    def take_damage(self):
        pass

monster = None

def enter():
    global monster
    # 현재 10개체 생성 난이도 상승시 개체수 상승 난이도 상승을 개채를 더할것인지 랜덤 범위를 줄일것인지
    monster = [Sucker() for i in range(3)]

def exit():
    global monster
    del monster
def update():
    global monster
    for sucker in monster:
        sucker.respawn_sucker()
        sucker.update()
def draw():
    global monster
    for sucker in monster:
        sucker.draw()







