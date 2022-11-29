from pico2d import*

import attack
import isaac
import monster_sucker
from monster_sucker import Sucker
import playstate
import game_world
import boss_monstro

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
        self.WID = 47
        self.HEI = 42
        self.speed = 5
        self.x = 0
        self.y = 0

        # 공격 범위 나중에 설정
        self.range = 0
        self.damage = 100
        self.dir = 0

        #print('생성: ', self.attack_num)

    def update(self):
        global monster_attack_range
        self.range += 1
        if (monster_attack_range - self.range) < 0:
            game_world.remove_object(self)

        if self.dir == 0:   #down
            self.y = (self.y - self.speed)
            if isaac.body_RL == True:
                if playstate.player.map_x != playstate.player.end_of_left and playstate.player.map_x != playstate.player.end_of_right:
                    self.x -= playstate.player.dir_x * 5
            if isaac.body_UD == True:
                if playstate.player.map_y != playstate.player.end_of_top and playstate.player.map_y != playstate.player.end_of_bottom:
                    self.y -= playstate.player.dir_y * 4

        elif self.dir == 1: #up
            self.y = (self.y + self.speed)
            if isaac.body_RL == True:
                if playstate.player.map_x != playstate.player.end_of_left and playstate.player.map_x != playstate.player.end_of_right:
                    self.x -= playstate.player.dir_x * 5
            if isaac.body_UD == True:
                if playstate.player.map_y != playstate.player.end_of_top and playstate.player.map_y != playstate.player.end_of_bottom:
                    self.y -= playstate.player.dir_y * 4

        elif self.dir == 2: #left
            self.x = (self.x - self.speed)
            if isaac.body_RL == True:
                if playstate.player.map_x != playstate.player.end_of_left and playstate.player.map_x != playstate.player.end_of_right:
                    self.x -= playstate.player.dir_x * 5
            if isaac.body_UD == True:
                if playstate.player.map_y != playstate.player.end_of_top and playstate.player.map_y != playstate.player.end_of_bottom:
                    self.y -= playstate.player.dir_y * 4

        elif self.dir == 3: #right
            self.x = (self.x + self.speed)
            if isaac.body_RL == True:
                if playstate.player.map_x != playstate.player.end_of_left and playstate.player.map_x != playstate.player.end_of_right:
                    self.x -= playstate.player.dir_x * 5
            if isaac.body_UD == True:
                if playstate.player.map_y != playstate.player.end_of_top and playstate.player.map_y != playstate.player.end_of_bottom:
                    self.y -= playstate.player.dir_y * 4

        elif self.dir == 4: #UL
            self.x -= self.speed
            self.y += self.speed
            if isaac.body_RL == True:
                if playstate.player.map_x != playstate.player.end_of_left and playstate.player.map_x != playstate.player.end_of_right:
                    self.x -= playstate.player.dir_x * 5
            if isaac.body_UD == True:
                if playstate.player.map_y != playstate.player.end_of_top and playstate.player.map_y != playstate.player.end_of_bottom:
                    self.y -= playstate.player.dir_y * 4

        elif self.dir == 5: # UR
            self.x += self.speed
            self.y += self.speed
            if isaac.body_RL == True:
                if playstate.player.map_x != playstate.player.end_of_left and playstate.player.map_x != playstate.player.end_of_right:
                    self.x -= playstate.player.dir_x * 5
            if isaac.body_UD == True:
                if playstate.player.map_y != playstate.player.end_of_top and playstate.player.map_y != playstate.player.end_of_bottom:
                    self.y -= playstate.player.dir_y * 4

        elif self.dir == 6: #DL
            self.x -= self.speed
            self.y -= self.speed
            if isaac.body_RL == True:
                if playstate.player.map_x != playstate.player.end_of_left and playstate.player.map_x != playstate.player.end_of_right:
                    self.x -= playstate.player.dir_x * 5
            if isaac.body_UD == True:
                if playstate.player.map_y != playstate.player.end_of_top and playstate.player.map_y != playstate.player.end_of_bottom:
                    self.y -= playstate.player.dir_y * 4

        elif self.dir == 7: #DR
            self.x += self.speed
            self.y -= self.speed
            if isaac.body_RL == True:
                if playstate.player.map_x != playstate.player.end_of_left and playstate.player.map_x != playstate.player.end_of_right:
                    self.x -= playstate.player.dir_x * 5
            if isaac.body_UD == True:
                if playstate.player.map_y != playstate.player.end_of_top and playstate.player.map_y != playstate.player.end_of_bottom:
                    self.y -= playstate.player.dir_y * 4




    # 캐릭터 이동 및 공격 키 입력
    def draw(self):
            self.image.clip_draw(self.frame_x, self.frame_y,
                                        self.WID, self.HEI, self.x, self.y)
            #draw_rectangle(*self.get_bb())


    def get_bb(self):
        return self.x - 25, self.y - 23, self.x + 21, self.y + 23

    def handle_collision(self, other, group):
        if group == 'monster_tears:player':
            if other.injury_status == False:
                game_world.remove_object(self)

attack_on = False
body_dir = 0
monster_attack_range = 200
monster_attack_damage = 100

