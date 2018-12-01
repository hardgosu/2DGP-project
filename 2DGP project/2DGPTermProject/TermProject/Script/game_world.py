
#레이어가 높을수록 나중에 렌더링됨 그러니까 나중에 렌더링된게 우선적으로 보임

# layer 0: Background Objects
# layer 1: Foreground Objects


Tag = ['Player','Feature','Monster','Effect','EnemyProjectile','PlayerProjectile']

Player,Feature,Monster,Effect,EnemyProjectile,PlayerProjectile,EffectAttack,FootBoard,Background,Portal = range(10)

objects = [[],[]]





def add_object(o, layer):
    objects[layer].append(o)

def add_objects(l, layer):
    for o in l:
        add_object(o, layer)


def remove_object(o):
    for i in range(len(objects)):
        if o in objects[i]:
            objects[i].remove(o)
            del o
            break


def clear():
    for o in all_objects():
        del o
    objects.clear()


def all_objects():
    for i in range(len(objects)):
        for o in objects[i]:
            yield o

