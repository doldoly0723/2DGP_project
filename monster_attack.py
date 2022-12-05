from pico2d import*

import attack
import game_framework
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

PIXEL_PER_METER = (10.0 / 0.1)  #10 pixel 10cm
ATTACK_SPEED_KMPH = 23.0   #Km / Hour

ATTACK_SPEED_MPM = (ATTACK_SPEED_KMPH * 1000.0 / 60.0)
ATTACK_SPEED_MPS = (ATTACK_SPEED_MPM / 60.0)
ATTACK_SPEED_PPS = (ATTACK_SPEED_MPS * PIXEL_PER_METER)

class Monster_Attack():
    image = None

    def __init__(self):
        if Monster_Attack.image == None:
            Monster_Attack.image = load_image('Sprite/monster_tear.png')

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

    def player_MonsterAttack_move(self):
        if isaac.body_RL == True:
            if playstate.player.map_x != playstate.player.end_of_left and playstate.player.map_x != playstate.player.end_of_right:
                if playstate.player.injury_status == True:
                    self.x -= playstate.player.dir_x * isaac.INJURY_SPEED_PPS * game_framework.frame_time
                else:
                    self.x -= playstate.player.dir_x * isaac.RUN_SPEED_PPS * game_framework.frame_time
        if isaac.body_UD == True:
            if playstate.player.map_y != playstate.player.end_of_top and playstate.player.map_y != playstate.player.end_of_bottom:
                if playstate.player.injury_status == True:
                    self.y -= playstate.player.dir_y * isaac.INJURY_SPEED_PPS * game_framework.frame_time
                else:
                    self.y -= playstate.player.dir_y * isaac.RUN_SPEED_PPS * game_framework.frame_time

    def update(self):
        global monster_attack_range
        self.range += 1
        if (monster_attack_range - self.range) < 0:
            game_world.remove_object(self)

        if self.dir == 0:   #down
            self.y -= ATTACK_SPEED_PPS * game_framework.frame_time
            self.player_MonsterAttack_move()

        elif self.dir == 1: #up
            self.y += ATTACK_SPEED_PPS * game_framework.frame_time
            self.player_MonsterAttack_move()

        elif self.dir == 2: #left
            self.x -= ATTACK_SPEED_PPS * game_framework.frame_time
            self.player_MonsterAttack_move()

        elif self.dir == 3: #right
            self.x += ATTACK_SPEED_PPS * game_framework.frame_time
            self.player_MonsterAttack_move()

        elif self.dir == 4: #UL
            self.x -= ATTACK_SPEED_PPS * game_framework.frame_time
            self.y += ATTACK_SPEED_PPS * game_framework.frame_time
            self.player_MonsterAttack_move()

        elif self.dir == 5: # UR
            self.x += ATTACK_SPEED_PPS * game_framework.frame_time
            self.y += ATTACK_SPEED_PPS * game_framework.frame_time
            self.player_MonsterAttack_move()

        elif self.dir == 6: #DL
            self.x -= ATTACK_SPEED_PPS * game_framework.frame_time
            self.y -= ATTACK_SPEED_PPS * game_framework.frame_time
            self.player_MonsterAttack_move()

        elif self.dir == 7: #DR
            self.x += ATTACK_SPEED_PPS * game_framework.frame_time
            self.y -= ATTACK_SPEED_PPS * game_framework.frame_time
            self.player_MonsterAttack_move()




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

