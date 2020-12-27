import pygame

from Champion import Champion
from Info import Info
from Projectile import Projectile


class Ashe(Champion):
    def __init__(self, x, y, summ=False):
        super().__init__(x, y, summ, name="Ashe", hp=10, mana=10, atk=1, atkrange=200, atkspd=0.5, be=5, ranged=True, img="sudo.png")
        self.passName = "Frost Shot"
        self.passDesc = "Slows enemies hit by attacks"
        self.actName = "Volley"
        self.actDesc = "Fires a splay of arrows"
        self.actCd = (0, 5)
        self.actCost = 4
        self.Champ = Ashe
        if not summ:
            Info.champions.append(self)
        Info.atkTimers[self] = pygame.time.get_ticks()
        self.canUse = True

    def fire(self):
        self.projects.append(Projectile(self.cx-7, self.cy-7, self.rot, self, name="Ashe"))

    def useAbility(self):
        self.projects.append(Projectile(self.cx-7, self.cy-7, self.rot-40, self, pen=True, atk=2, speed=40, name="Ashe"))
        self.projects.append(Projectile(self.cx-7, self.cy-7, self.rot-30, self, pen=True, atk=2, speed=40, name="Ashe"))
        self.projects.append(Projectile(self.cx-7, self.cy-7, self.rot-20, self, pen=True, atk=2, speed=40, name="Ashe"))
        self.projects.append(Projectile(self.cx-7, self.cy-7, self.rot-10, self, pen=True, atk=2, speed=40, name="Ashe"))
        self.projects.append(Projectile(self.cx-7, self.cy-7, self.rot, self, pen=True, atk=2, speed=40, name="Ashe"))
        self.projects.append(Projectile(self.cx-7, self.cy-7, self.rot+10, self, pen=True, atk=2, speed=40, name="Ashe"))
        self.projects.append(Projectile(self.cx-7, self.cy-7, self.rot+20, self, pen=True, atk=2, speed=40, name="Ashe"))
        self.projects.append(Projectile(self.cx-7, self.cy-7, self.rot+30, self, pen=True, atk=2, speed=40, name="Ashe"))
        self.projects.append(Projectile(self.cx-7, self.cy-7, self.rot+40, self, pen=True, atk=2, speed=40, name="Ashe"))
