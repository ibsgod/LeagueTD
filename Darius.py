import pygame

from Enemy import Enemy
from Info import Info


class Darius(Enemy):
    def __init__(self, x, y, hp):
        super().__init__(x, y, name="Darius", hp=hp, atk=2, atkspd=1, speed=10, atkrange=50, colour=(100, 0, 0))
        Info.enemies.append(self)
        self.prevtarg = None
        self.stack = 0
        self.passName = "Hemorrhoids"
        self.passDesc = "Damage Increases when attacking the same target."
        self.fireSound.set_volume(0.3)

    def fire(self):
        if self.target == self.prevtarg:
            self.stack += 1
        else:
            self.stack = 0
        self.target.takeDamage(self.atk + self.stack)
        self.prevtarg = self.target

    def checkRange(self, pos, rad, rect):
        distx = abs(pos[0] - rect.x - rect.width/2)
        disty = abs(pos[1] - rect.y - rect.height/2)
        if distx > (rect.width / 2 + rad):
            return False
        if disty > (rect.height / 2 + rad):
            return False
        if distx <= (rect.width / 2):
            return True
        if disty <= (rect.height / 2):
            return True
        cornerDistance_sq = (distx - rect.width / 2) ** 2 + (disty - rect.height / 2) ** 2
        return (cornerDistance_sq <= (rad ** 2))