import math

from Enemy import Enemy
from Info import Info
from Projectile import Projectile


class Draven(Enemy):
    def __init__(self, x, y, hp):
        super().__init__(x, y, name="Draven", hp=hp, atk=2, atkspd=1, speed=10, atkrange=200, colour=(100, 0, 0))
        Info.enemies.append(self)
        self.passName = "Blood Rush"
        self.passDesc = "Speed permanently increased with each attack."

    def tick(self, mousePos, click):
        self.target = None
        self.rot = 180
        for i in Info.champions:
            if self.checkRange((self.cx, self.cy), self.atkrange, i.hitbox):
                if self.target is None:
                    if i.cx - self.cx != 0:
                        self.rot = math.degrees(math.atan((self.cy - i.cy) / (i.cx - self.cx)))
                    else:
                        if self.cy > i.cy:
                            self.rot = 90
                        else:
                            self.rot = -90
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
        self.speed += 1

