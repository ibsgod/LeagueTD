import math

import pygame

from Champion import Champion
from Info import Info
from Projectile import Projectile


class Ashe(Champion):
    def __init__(self, x, y, summ=False, hp=None, mana=None):
        super().__init__(x, y, summ, name="Ashe", hp=6, mana=10, atk=1, atkrange=200, atkspd=0.6666666, be=16, ranged=True)
        self.passName = "Frost Shot"
        self.passDesc = "Slows enemies hit by attacks"
        self.actName = "Volley"
        self.actDesc = "Fires a splay of arrows (Dayum, dat ashe)"
        self.actCd = (Info.acTime, 5)
        self.actCost = 4
        self.Champ = Ashe
        if not summ:
            Info.champions.append(self)
        self.canUse = True
        if hp is not None:
            self.hp = hp
            self.mana = mana

    def tick(self, mousePos, click):
        self.canUse = len(Info.enemies) > 0
        if not self.summ:
            self.target = None
            self.blocked = []
            for i in Info.enemies:
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
                    if len(self.blocked) < self.block:
                        self.blocked.append(i)
            self.cx = self.x + self.size / 2
            self.cy = self.y + self.size / 2
            self.hitbox = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
            if self.hitbox.collidepoint(mousePos) and Info.summoning is None:
                if click:
                    Info.selected = self
                    return 2
                return 1
        else:
            self.x = mousePos[0] - self.size/2
            self.y = mousePos[1] - self.size/2
        self.cx = self.x + self.size / 2
        self.cy = self.y + self.size / 2
        self.hitbox = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())

    def fire(self):
        self.projects.append(Projectile(self.cx-30, self.cy-30, self.rot, self, name="Ashe"))

    def useAbility(self):
        # pain.
        # angles = []
        # for i in Info.enemies:
        #     pee = 0
        #     if i.cx - self.cx != 0:
        #         pee = math.degrees(math.atan((self.cy - i.cy) / (i.cx - self.cx)))
        #     if i.cx < self.cx:
        #         pee -= 180
        #     angles.append(pee)
        # angles.sort()
        # angles += angles
        # start = 0
        # end = 0
        # tot = 0
        # _max = [(0, 0)]
        # while start < len(angles)/2 and end < len(angles):
        #     if min(angles[end] - angles[start], 360 - angles[start] + angles[end]) <= 80:
        #         tot += 1
        #         end += 1
        #         if tot > _max[0][0]:
        #             _max.clear()
        #             _max.append((tot, angles[start]))
        #         elif tot == _max[0][0]:
        #             _max.append((tot, angles[start]))
        #     else:
        #         tot -= 1
        #         start += 1
        # self.rot = _max[int(len(_max)/2)][1]
        self.rot = math.degrees(math.atan((self.cy - Info.enemies[0].cy) / (Info.enemies[0].cx - self.cx)))
        if Info.enemies[0].cx < self.cx:
            self.rot -= 180
        self.projects.append(Projectile(self.cx-30, self.cy-30, self.rot-40, self, atk=2, speed=40, name="Ashe"))
        self.projects.append(Projectile(self.cx-30, self.cy-30, self.rot-30, self, atk=2, speed=40, name="Ashe"))
        self.projects.append(Projectile(self.cx-30, self.cy-30, self.rot-20, self, atk=2, speed=40, name="Ashe"))
        self.projects.append(Projectile(self.cx-30, self.cy-30, self.rot-10, self, atk=2, speed=40, name="Ashe"))
        self.projects.append(Projectile(self.cx-30, self.cy-30, self.rot, self, atk=2, speed=40, name="Ashe"))
        self.projects.append(Projectile(self.cx-30, self.cy-30, self.rot+10, self, atk=2, speed=40, name="Ashe"))
        self.projects.append(Projectile(self.cx-30, self.cy-30, self.rot+20, self, atk=2, speed=40, name="Ashe"))
        self.projects.append(Projectile(self.cx-30, self.cy-30, self.rot+30, self, atk=2, speed=40, name="Ashe"))
        self.projects.append(Projectile(self.cx-30, self.cy-30, self.rot+40, self, atk=2, speed=40, name="Ashe"))
