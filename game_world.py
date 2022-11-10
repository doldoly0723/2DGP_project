# object[0] : 바닥 계층
# object[1] : 상위 계층
objects = [[], [], []]

def add_object(o, depth):
    objects[depth].append(o)

def add_objects(ol, depth):
    objects[depth] += ol

def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o) # 리스트에 빼주는거
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
