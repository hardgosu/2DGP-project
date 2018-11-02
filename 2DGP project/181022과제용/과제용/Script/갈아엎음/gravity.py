from pico2d import *
#추후에 상속으로 정리.

class Gravity:

    def __init__(self,width,height,x,y,a):
        self.objectsOfAffectedByGravity = []

        self.width = width
        self.height = height
        self.positionX = x
        self.positionY = y


        self.acceleration = a




        pass


    def collide(self , b):
        left_a, bottom_a, right_a, top_a = self.get_bb()
        left_b, bottom_b, right_b, top_b = b.get_bb()

        if left_a > right_b:
            return False
        if right_a < left_b:
            return False
        if top_a < bottom_b:
            return False
        if bottom_a > top_b:
            return False
        return True


    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.positionX  - self.width // 2 , self.positionY - self.height//2,self.positionX + self.width//2,self.positionY + self.height//2

    def update(self):
        self.draw_bb()
        for obj in self.objectsOfAffectedByGravity:
            #print("중력적용!!!!")
            #print(obj)
            if self.collide(obj):
                obj.y -= self.acceleration





        pass