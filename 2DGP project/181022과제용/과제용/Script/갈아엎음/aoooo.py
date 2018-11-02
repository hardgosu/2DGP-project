from pico2d import *
import collision
import game_framework
import objectManager


#print(collision.temp + 5000)

objectManager.objectsOfAffectedByGravity.append("고운말")
print(objectManager.objectsOfAffectedByGravity[-1])

game_framework.run(collision)



