import math

import pygame

from Champion import Champion
from Info import Info
from Projectile import Projectile


class Lulu(Champion):
    def __init__(self, x, y, summ=False, hp=None, mana=None):
        super().__init__(x, y, summ, name="Lulu", hp=10, mana=10, atk=0.5, atkrange=200, atkspd=1, be=5, ranged=True)
        self.passName = "Ratatatata"
        self.passDesc = "Nearby towers get increased attack speed"
        self.actName = "Hugeify!"
        self.actDesc = "Most wounded champion in range gets fully healed and stuns nearby enemies (Purple purple purple)"
        self.actCd = (Info.acTime, 5)
        self.actCost = 4
        self.Champ = Lulu
        if not summ:
            Info.champions.append(self)
        self.canUse = True
        if hp is not None:
            self.hp = hp
            self.mana = mana
        self.boosted = []
        self.ultCircle = None

    def draw(self, screen):
        if len(self.atkAnim) > 0 and self.animStart is not None and self.animStart + self.atkspd * 1000 > Info.acTime:
            self.img = self.atkAnim[len(self.atkAnim) - int((self.animStart + self.atkspd * 1000 - Info.acTime) / self.atkspd / 1000 * len(self.atkAnim))-1]
        else:
            self.img = self.idleimg
        screen.blit(pygame.transform.flip(self.img, self.rot >= 90 or self.rot <= -90,  False), (self.x, self.y))
        if Info.selected is self:
            pygame.draw.circle(screen, (255, 0, 0), (int(self.cx), int(self.cy)), self.atkrange+40, 5)
        if not self.summ:
            maxbar = pygame.Surface((self.size, 8))
            maxbar.set_alpha(80)
            maxbar.fill((0, 0, 0))
            screen.blit(maxbar, (self.x + (self.size - maxbar.get_width()) / 2, self.y - 15))
            pygame.draw.rect(screen, (min(255, int((self.maxhp - self.hp) * 255 / (self.maxhp - 1))),
                                      max(0, int(255 - (self.maxhp - self.hp) * 255 / (self.maxhp - 1))), 0), (
                                 self.x + (self.size - maxbar.get_width()) / 2, self.y - 15,
                                 max(0, maxbar.get_width() / self.maxhp * self.hp), 8))
            screen.blit(maxbar, (self.x + (self.size - maxbar.get_width()) / 2, self.y - 15 + maxbar.get_height()))
            pygame.draw.rect(screen, (0, 100, 200), (
                                 self.x + (self.size - maxbar.get_width()) / 2, self.y - 15 + maxbar.get_height(),
                                 max(0, maxbar.get_width() / self.maxmana * self.mana), 8))
        if self.ultCircle is not None:
            surface1 = pygame.Surface((560, 560))
            surface1.set_colorkey((0, 0, 0))
            surface1.set_alpha(int((self.ultCircle[1] - Info.acTime) / 1000 * 200))
            pygame.draw.circle(surface1, (150, 0, 150), (280, 280), 300 - int((self.ultCircle[1] - Info.acTime) / 1000 * 70))
            screen.blit(surface1, (self.ultCircle[0][0]-280, self.ultCircle[0][1]-280))
            if self.ultCircle[1] < Info.acTime:
                self.ultCircle = None

    def tick(self, mousePos, click):
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
            if self.hitbox.collidepoint(mousePos) and Info.summoning is None:
                if click:
                    Info.selected = self
                    return 2
                return 1
            for i in Info.champions:
                if i not in self.boosted and i.atkspd == i.oriatkspd and i.checkRange((self.cx, self.cy), self.atkrange, i.hitbox):
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
            self.ultCircle = ((champ[1].cx, champ[1].cy), Info.acTime + 1000)
            for i in Info.enemies:
                if self.checkRange((champ[1].cx, champ[1].cy), 280, i.hitbox):
                    i.takeDamage(1)
                    i.cripple((0, Info.acTime + 1000))



