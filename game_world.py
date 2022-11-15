# object[0] : 바닥 계층
# object[1] : 상위 계층
objects = [[], [], []]
collision_group = dict()

def add_object(o, depth):
    objects[depth].append(o)

def add_objects(ol, depth):
    objects[depth] += ol

def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o) # 리스트에 빼주는거
            remove_collision_objecct(o)
            del(o) #메모리에서 날려준다
            break

# yield 포함된 함수 -> 발생자, 제너레이트 함수, for문 과 연동하여 사용
def all_objects():
    for layer in objects:
        for o in layer:
            yield o # 제러레이터, 모든 객체들을 하나씩 넘겨준다.


def second_objects():
    for o in objects[1][:]:
        yield o

def clear():
    for o in all_objects():
        del o
    for layer in objects:
        layer.clear()

collision_group['tears:suckers'] = [[],[]]
collision_group['tears:spittys'] = [[],[]]
collision_group['player:suckers'] = [[],[]]
collision_group['player:spittys'] = [[],[]]
def add_collision_pairs(a, b, group):
    print('add new group')
    #collision_group[group] = [[], []]  # 호출될때마다 초기화 된다
    if a:
        if type(a) == list:
            collision_group[group][0] += a
        else:
            collision_group[group][0].append(a)
    if b:
        if type(b) == list:
            collision_group[group][1] += b
        else:
            collision_group[group][1].append(b)

def all_collision_pairs():
    for group, pairs in collision_group.items():
        for a in pairs[0]:
            for b in pairs[1]:
                yield a, b, group
def remove_collision_objecct(o):
    for pairs in collision_group.values():
        if o in pairs[0]: pairs[0].remove(o)
        elif o in pairs[1]: pairs[1].remove(o)