from pico2d import*
import isaac
import random   # 몬스터의 출현


class Sucker:
    def __init__(self):
        self.sucker_WID = 80
        self.sucker_HEI = 80
        self.sucker_t = 0
        self.sucker_x = 0
        self.sucker_y = 0
        self.sucker_sx = 0
        self.sucker_sy = 0
        self.sucker_status = False  # 현재 존재하는가
        self.sucker_image = load_image('sucker.png')
        self.sucker_frame = 0
        self.frame_count = 0

        self.choose_wall = 0 # 리스폰 지역 설정
        pass

    def respawn_sucker(self):
        if 1 == random.randint(0, 1000): #랜덤한 시간으로 몬스터를 생성 난이도 상승시 범위도 같이 높여야 한다
            if self.sucker_status == False:
                self.choose_wall = random.randint(0, 5)
                self.sucker_status = 1
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
            if self.sucker_t > 1.0:
                sucker.take_damage()
                #self.sucker_t -=0.00002

        self.frame_count += 1
        if self.frame_count == 10:
            self.sucker_frame = (self.sucker_frame + 1) % 2
            self.frame_count = 0
            pass

    def draw(self):
        if self.sucker_status == True:
            self.sucker_image.clip_draw(self.sucker_frame*80, 0,
                                        self.sucker_WID, self.sucker_HEI, self.sucker_x, self.sucker_y)

        pass

    def take_damage(self):
        pass

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

open_canvas(isaac.MAP_WIDTH,isaac.MAP_HEIGHT)

running = True

isaac.enter()
#sucker = Sucker()
monster = [Sucker() for i in range(10)] #현재 10개체 생성 난이도 상승시 개체수 상승

while isaac.running:
    isaac.handle_events()
    isaac.update()
    isaac.draw()
    for sucker in monster:
        sucker.respawn_sucker()
        sucker.update()
        sucker.draw()
    update_canvas()

isaac.exit()

pico2d.clear_canvas()





