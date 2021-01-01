import math

import pygame

from Champion import Champion
from Info import Info
from Projectile import Projectile


class Lulu(Champion):
    def __init__(self, x, y, summ=False, hp=None, mana=None):
        super().__init__(x, y, summ, name="Lulu", hp=10, mana=10, atk=0.5, atkrange=200, atkspd=1, be=5, ranged=True, img="sudo.png")
        self.passName = "Ratatatata"
        self.passDesc = "Nearby towers get increased attack speed"
        self.actName = "Hugeify!"
        self.actDesc = "Most wounded champion in range gets fully healed and stuns nearby enemies"
        self.actCd = (0, 5)
        self.actCost = 4
        self.Champ = Lulu
        if not summ:
            Info.champions.append(self)
        self.canUse = True
        if hp is not None:
            self.hp = hp
            self.mana = mana
        self.boosted = []

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
            for i in Info.champions:
                if i not in self.boosted:
                    i.atkspd /= 1.5
                    self.boosted.append(i)
        else:
            self.x = mousePos[0] - self.size/2
            self.y = mousePos[1] - self.size/2
        self.cx = self.x + self.size / 2
        self.cy = self.y + self.size / 2

    def fire(self):
        self.projects.append(Projectile(self.cx-7, self.cy-7, self.rot, self))

    def useAbility(self):
        champ = (99999, None)
        for i in Info.champions:
            if self.checkRange((self.cx, self.cy), self.atkrange, i.hitbox) and i.hp < champ[0]:
                champ = (i.hp, i)
        if champ[1] is not None:
            champ[1].hp = champ[1].maxhp
            for i in Info.enemies:
                if self.checkRange((champ[1].cx, champ[1].cy), 200, i.hitbox):
                    i.takeDamage(1)
                    i.cripple((0, Info.acTime + 1000))


