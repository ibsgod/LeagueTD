import math

import pygame

from Champion import Champion
from Info import Info
from Projectile import Projectile


class Sona(Champion):
    def __init__(self, x, y, summ=False, hp=None, mana=None):
        super().__init__(x, y, summ, name="Sona", hp=10, mana=10, atk=0.5, atkrange=200, atkspd=1, be=5, ranged=True, img="sudo.png")
        self.passName = "Nightcore"
        self.passDesc = "Nearby towers regen health"
        self.actName = "Crescendo"
        self.actDesc = "Fires a beam that stuns enemies"
        self.actCd = (0, 5)
        self.actCost = 4
        self.Champ = Sona
        if not summ:
            Info.champions.append(self)
        self.canUse = True
        if hp is not None:
            self.hp = hp
            self.mana = mana
        self.regenTimer = Info.acTime

    def tick(self, mousePos, click):
        if not self.summ:
            self.target = None
            self.blocked = []
            for i in Info.enemies:
                if self.checkRange((self.cx, self.cy), self.atkrange, i.hitbox):
                    if self.target is None:
                        if i.cx - self.cx != 0:
                            self.rot = math.degrees(math.atan((self.cy - i.cy) / (i.cx - self.cx)))
                        if i.cx < self.cx:
                            self.rot -= 180
                        self.target = i
                    if len(self.blocked) < self.block:
                        self.blocked.append(i)
            if self.hitbox.collidepoint(mousePos) and Info.summoning is None:
                if click:
                    Info.selected = self
                    return 2
                return 1
            if Info.acTime - self.regenTimer > 1500:
                for i in Info.champions:
                    if self.checkRange((self.cx, self.cy), self.atkrange, i.hitbox):
                        i.hp = min(i.hp+1, i.maxhp)
                self.regenTimer = Info.acTime
        else:
            self.x = mousePos[0] - self.size/2
            self.y = mousePos[1] - self.size/2
        self.cx = self.x + self.size / 2
        self.cy = self.y + self.size / 2

    def fire(self):
        self.projects.append(Projectile(self.cx-7, self.cy-7, self.rot, self))

    def useAbility(self):
        self.projects.append(Projectile(self.cx-7, self.cy-7, self.rot, self, pen=True, atk=2, speed=40, name="Sona"))
