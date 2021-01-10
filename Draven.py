import math

from Enemy import Enemy
from Info import Info
from Projectile import Projectile


class Draven(Enemy):
    def __init__(self, x, y, hp):
        super().__init__(x, y, name="Draven", hp=hp, atk=2, atkspd=1, speed=10, atkrange=200, img="sudo.png", colour=(100, 0, 0))
        Info.enemies.append(self)
        self.flip = True

    def tick(self, mousePos, click):
        self.target = None
        for i in Info.champions:
            if self.checkRange((self.cx, self.cy), self.atkrange, i.hitbox):
                if self.target is None:
                    if i.cx - self.cx != 0:
                        self.rot = math.degrees(math.atan((self.cy - i.cy) / (i.cx - self.cx)))
                    if i.cx < self.cx:
                        self.rot -= 180
                    self.target = i
        if self.target is None:
            self.move()
        if self.hitbox.collidepoint(mousePos) and Info.summoning is None:
            if click:
                Info.selected = self
                return 2
            return 1
        return

    def fire(self):
        self.projects.append(Projectile(self.cx-7, self.cy-7, self.rot, self, name="Draven"))

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