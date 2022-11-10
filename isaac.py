from pico2d import*
import attack
import game_world
import monster
import playstate

WD, SD, AD, DD, UP_D, DOWN_D, RIGHT_D, LEFT_D, WU, SU, AU, DU, UP_U, DOWN_U, RIGHT_U, LEFT_U = range(16) # 키
key_event_table = {
    (SDL_KEYDOWN, SDLK_w): WD,
    (SDL_KEYDOWN, SDLK_s): SD,
    (SDL_KEYDOWN, SDLK_a): AD,
    (SDL_KEYDOWN, SDLK_d): DD,
    (SDL_KEYUP, SDLK_w): WU,
    (SDL_KEYUP, SDLK_s): SU,
    (SDL_KEYUP, SDLK_a): AU,
    (SDL_KEYUP, SDLK_d): DU,
    (SDL_KEYDOWN, SDLK_UP): UP_D,
    (SDL_KEYDOWN, SDLK_DOWN): DOWN_D,
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_D,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_D,
    (SDL_KEYUP, SDLK_UP): UP_U,
    (SDL_KEYUP, SDLK_DOWN): DOWN_U,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_U,
    (SDL_KEYUP, SDLK_LEFT): LEFT_U,
}

# class IDLE:
#     def enter(self, event):
#         self.dir_x = 0
#         self.dir_y = 0
#     def exit(self):
#         pass
#     def do(self):
#         self.head_cnt += 1
#         if self.head_cnt > 50:
#             self.head_frame = (self.head_frame + 1) % 2
#             self.head_cnt = 0
#
#         # update_head_frame(self): # 0, 1 눈을 깜빡이게 하면서 이동속도를 늧추지 않게 하기 위해서는? 우선은 랜덤 처리
#         if self.frame_body_Y == 0:  # LR
#             self.body_y = self.body_LR_y
#         elif self.frame_body_Y == 1:  # UD
#             self.body_y = self.body_UD_y
#
#         # update_body_frame(self):
#         self.body_cnt += 1
#         if self.body_cnt > 20:
#             self.body_frame = (self.body_frame + 1) % 10
#             self.body_cnt = 0
#
#     def draw(self):
#         self.image_map.clip_draw(self.map_x, self.map_y, MAP_WIDTH, MAP_HEIGHT, self.mid_x, self.mid_y)
#         # 몸
#         if (self.frame_body_reverse == 0):
#             self.image_isaac.clip_draw(self.body_frame * self.body_WID + self.body_x, self.body_y, self.body_WID,
#                                        self.body_HEI, self.mid_x, self.mid_y - self.body_head_space)
#         elif (self.frame_body_reverse == 1):
#             self.image_isaac_reverse.clip_draw(self.body_frame * self.body_WID + self.body_reverse_x, self.body_y,
#                                                self.body_WID, self.body_HEI, self.mid_x,
#                                                self.mid_y - self.body_head_space)
#         # 머리
#         self.image_isaac.clip_draw((self.frame_head + self.head_frame) * self.head_WID + self.head_x, self.head_y,
#                                    self.head_WID, self.head_HEI, self.mid_x, self.mid_y)
class MOVE_ATTACK:
    def enter(self, event):
        if event == WD:
            self.dir_y += 1
            self.frame_body_Y = 1   # UP, DOWN
            self.frame_nody_reverse = 1
            attack.body_dir = 4 #up
        elif event == SD:
            self.dir_y -= 1
            self.frame_body_Y = 1
            self.frame_body_reverse = 0
            attack.body_dir = 0  # down
        elif event == AD:
            self.dir_x -= 1
            self.frame_body_Y = 0  # LR
            self.frame_body_reverse = 1
            attack.body_dir = 2  # left
        elif event == DD:
            self.dir_x += 1
            self.frame_body_Y = 0
            self.frame_body_reverse = 0
            attack.body_dir = 6  # right
        if event == UP_D:
            self.frame_head = 4
            attack.attack_on = True
            attack.attack_cnt += 1
            playstate.tears = attack.Attack()
            game_world.add_object(playstate.tears, 2)
            #playstate.tears += [attack.Attack()]
        elif event == DOWN_D:
            self.frame_head = 0
            attack.attack_on = True
            attack.attack_cnt += 1
            playstate.tears = attack.Attack()
            game_world.add_object(playstate.tears, 2)
            #playstate.tears += [attack.Attack()]
        elif event == LEFT_D:
            self.frame_head = 6
            attack.attack_on = True
            attack.attack_cnt += 1
            playstate.tears = attack.Attack()
            game_world.add_object(playstate.tears, 2)
            #playstate.tears += [attack.Attack()]
        elif event == RIGHT_D:
            self.frame_head = 2
            attack.attack_on = True
            attack.attack_cnt += 1
            playstate.tears = attack.Attack()
            game_world.add_object(playstate.tears, 2)
            #playstate.tears += [attack.Attack()]
        if event == WU:
            self.dir_y -= 1
        elif event == SU:
            self.dir_y += 1
        elif event == AU:
            self.dir_x += 1
        elif event == DU:
            self.dir_x -= 1

    def exit(self):
        pass
    def do(self):
        self.map_x += self.dir_x * 5
        self.map_y += self.dir_y * 5
        self.map_x = clamp(self.end_of_left, self.map_x, self.end_of_right)
        self.map_y = clamp(self.end_of_bottom, self.map_y, self.end_of_top)

        self.head_cnt += 1
        if self.head_cnt > 50:
            self.head_frame = (self.head_frame + 1) % 2
            self.head_cnt = 0

        # update_head_frame(self): # 0, 1 눈을 깜빡이게 하면서 이동속도를 늧추지 않게 하기 위해서는? 우선은 랜덤 처리
        if self.frame_body_Y == 0:   #LR
            self.body_y = self.body_LR_y
        elif self.frame_body_Y == 1: #UD
            self.body_y = self.body_UD_y

        #update_body_frame(self):
        self.body_cnt += 1
        if self.body_cnt > 20:
            self.body_frame = (self.body_frame+1)%10
            self.body_cnt = 0

    def draw(self):
        self.image_map.clip_draw(self.map_x, self.map_y, MAP_WIDTH, MAP_HEIGHT, self.mid_x, self.mid_y)
        # 몸
        if (self.frame_body_reverse == 0):
            self.image_isaac.clip_draw(self.body_frame * self.body_WID + self.body_x, self.body_y, self.body_WID,
                                       self.body_HEI, self.mid_x, self.mid_y - self.body_head_space)
        elif (self.frame_body_reverse == 1):
            self.image_isaac_reverse.clip_draw(self.body_frame * self.body_WID + self.body_reverse_x, self.body_y,
                                               self.body_WID, self.body_HEI, self.mid_x,
                                               self.mid_y - self.body_head_space)
        # 머리
        self.image_isaac.clip_draw((self.frame_head + self.head_frame) * self.head_WID + self.head_x, self.head_y,
                                   self.head_WID, self.head_HEI, self.mid_x, self.mid_y)

class HEART:
    pass

next_state = {
    MOVE_ATTACK: {WU: MOVE_ATTACK, SU: MOVE_ATTACK, AU: MOVE_ATTACK, DU: MOVE_ATTACK,
                  WD: MOVE_ATTACK, SD: MOVE_ATTACK, AD: MOVE_ATTACK, DD: MOVE_ATTACK,
                  UP_U: MOVE_ATTACK, DOWN_U: MOVE_ATTACK, LEFT_U: MOVE_ATTACK, RIGHT_U: MOVE_ATTACK,
                  UP_D: MOVE_ATTACK, DOWN_D: MOVE_ATTACK, LEFT_D: MOVE_ATTACK, RIGHT_D: MOVE_ATTACK
                  }
}
# 화면 크기
MAP_WIDTH, MAP_HEIGHT = 1600, 900
# 전체 맵 크기
FULL_MAP_WID, FULL_MAP_HEI = 6401, 3600

class Player:

    def add_event(self, event):
        self.q.insert(0, event)

    def handle_event(self, event):
        if(event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
    def __init__(self):
        self.image_map = load_image('map.png')
        self.image_isaac = load_image('isaac.png')
        self.image_isaac_reverse = load_image('isaac_reverse.png')


        self.mid_x = MAP_WIDTH // 2
        self.mid_y = MAP_HEIGHT // 2
        self.map_x = FULL_MAP_WID // 2
        self.map_y = FULL_MAP_HEI // 2
        # head
        self.head_x = 20
        self.head_y = 835
        self.head_WID = 115
        self.head_HEI = 85
        self.head_frame = 0
        self.head_cnt = 0
        #body
        self.body_WID = 93
        self.body_HEI = 45
        self.body_x = 30
        self.body_y = 0 # UD, LR 에 따라 달라진다
        self.body_UD_y = 710 #위, 아래 스프라이트
        self.body_LR_y = 590 #왼쪽, 오른쪽 스프라이트
        self.body_frame = 0
        self.body_cnt = 0
        self.body_reverse_x = 26

        self.body_head_space = 45
        # 테두리 경계선
        self.end_of_left = 65
        self.end_of_right = 4800
        self.end_of_top = 2725
        self.end_of_bottom = 0

        self.dir_x = 0
        self.dir_y = 0
        self.frame_head = 0
        self.frame_body_reverse = 0  # 반전 스프라이트 체크
        self.frame_body_Y = 1  # 상하 스프라이트인가 좌우 스프라이트인가

        self.q = []
        self.cur_state = MOVE_ATTACK
        self.cur_state.enter(self, None)

    def update(self):
        self.cur_state.do(self)

        if self.q:
            event = self.q.pop()
            self.cur_state.exit(self)
            self.cur_state = next_state[self.cur_state][event]
            self.cur_state.enter(self, event)
    #     # 키 입력에 따른 이동
    #     self.map_x += dir_x*5
    #     self.map_y += dir_y*5
    #     # 맵 밖으로 못나가게 설정
    #
    #     if self.map_x < self.end_of_left:
    #         self.map_x = self.end_of_left
    #     elif self.map_x > self.end_of_right:
    #         self.map_x = self.end_of_right
    #     elif self.map_y > self.end_of_top:
    #         self.map_y = self.end_of_top
    #     elif self.map_y < self.end_of_bottom:
    #         self.map_y = self.end_of_bottom
    #
    #     # 키 입력에 따른 아이작 프레임 변화 머리, 다리 따로
    #     pass
    # def update_head_frame(self): # 0, 1 눈을 깜빡이게 하면서 이동속도를 늧추지 않게 하기 위해서는? 우선은 랜덤 처리
    #     self.head_cnt += 1
    #     if self.head_cnt > 50:
    #         self.head_frame = (self.head_frame+1) % 2
    #         self.head_cnt = 0
    # def update_body_frame(self):
    #     if frame_body_Y == 0:   #LR
    #         self.body_y = self.body_LR_y
    #     elif frame_body_Y == 1: #UD
    #         self.body_y = self.body_UD_y
    #
    #     self.body_cnt += 1
    #     if self.body_cnt > 20:
    #         self.body_frame = (self.body_frame+1)%10
    #         self.body_cnt = 0




    def draw(self):
        self.cur_state.draw(self)
        # self.image_map.clip_draw(self.map_x,self.map_y,MAP_WIDTH,MAP_HEIGHT,self.mid_x,self.mid_y)
        # # 몸
        # if(frame_body_reverse == 0):
        #     self.image_isaac.clip_draw(self.body_frame * self.body_WID + self.body_x, self.body_y,self.body_WID, self.body_HEI, self.mid_x, self.mid_y - self.body_head_space)
        # elif(frame_body_reverse == 1):
        #     self.image_isaac_reverse.clip_draw(self.body_frame * self.body_WID + self.body_reverse_x, self.body_y,self.body_WID, self.body_HEI, self.mid_x, self.mid_y - self.body_head_space)
        # # 머리
        # self.image_isaac.clip_draw((frame_head+self.head_frame)*self.head_WID+self.head_x, self.head_y, self.head_WID, self.head_HEI, self.mid_x, self.mid_y)
        # pass


# 캐릭터 이동 및 공격 키 입력
# def handle_events():
#     global dir_y
#     global dir_x
#     global frame_head, frame_body_Y, frame_body_X, frame_body_reverse
#     global attack_on, body_dir
#     global tears
#     events = get_events()
#     for event in events:
#         if event.type == SDL_KEYDOWN:
#             # 이동
#             if event.key == SDLK_w:
#                 dir_y += 1
#                 frame_body_Y = 1    #UD
#                 frame_body_reverse = 1
#                 attack.body_dir = 4    #up
#             elif event.key == SDLK_s:
#                 dir_y -= 1
#                 frame_body_Y = 1
#                 frame_body_reverse = 0
#                 attack.body_dir = 0    #down
#             elif event.key == SDLK_a:
#                 dir_x -= 1
#                 frame_body_Y = 0    #LR
#                 frame_body_reverse = 1
#                 attack.body_dir = 2    #left
#             elif event.key == SDLK_d:
#                 dir_x += 1
#                 frame_body_Y = 0
#                 frame_body_reverse = 0
#                 attack.body_dir = 6    #right
#             #이동에 따른 아이작 스프라이트
#             #키누르면 공격 모드 시작
#             elif event.key == SDLK_UP:
#                 frame_head = 4
#                 attack.attack_on = True
#                 attack.attack_cnt += 1
#                 attack.tears += [attack.Attack()]
#
#             elif event.key == SDLK_DOWN:
#                 frame_head = 0
#                 attack.attack_on = True
#                 attack.attack_cnt += 1
#                 attack.tears += [attack.Attack()]
#
#             elif event.key == SDLK_LEFT:
#                 frame_head = 6
#                 attack.attack_on = True
#                 attack.attack_cnt += 1
#                 attack.tears += [attack.Attack()]
#
#             elif event.key == SDLK_RIGHT:
#                 frame_head = 2
#                 attack.attack_on = True
#                 attack.attack_cnt += 1
#                 attack.tears += [attack.Attack()]
#
#         elif event.type == SDL_KEYUP:
#             if event.key == SDLK_w:
#                 dir_y -= 1
#             elif event.key == SDLK_s:
#                 dir_y += 1
#             elif event.key == SDLK_a:
#                 dir_x += 1
#             elif event.key == SDLK_d:
#                 dir_x -= 1
#
# dir_x = None
# dir_y = None
# # 맵 이동에 따른 아이작 프레임 설정 머리 다리 따로 설정 필요
# frame_head = None
# frame_body_reverse = None    # 반전 스프라이트 체크
# frame_body_Y = None    # 상하 스프라이트인가 좌우 스프라이트인가
# player = None
#
#
# def enter():
#     global dir_x, dir_y
#     global frame_head, frame_body_Y,frame_body_reverse
#     global player
#     attack.enter()
#     monster.enter()
#
#
#
#     player = Player()
#
#
# def exit():
#     global player, tears
#     del player
#     attack.exit()
#     monster.exit()
# def update():
#     player.update()
#     player.update_head_frame()
#     player.update_body_frame()
#     attack.update()
#     monster.update()
# def draw():
#     clear_canvas()
#     player.draw()
#     attack.draw()
#     monster.draw()
#     delay(0.01)
#     update_canvas()

