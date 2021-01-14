import math

import pygame

from Champion import Champion
from Info import Info


class Nasus(Champion):
    def __init__(self, x, y, summ=False, hp=None, mana=None):
        super().__init__(x, y, summ, name="Nasus", hp=15, mana=10, atk=1, atkrange=100, atkspd=1, be=5, ranged=False, block=10)
        self.passName = "Soul Eater"
        self.passDesc = "Gains HP when attacking"
        self.actName = "Siphoning Strike"
        self.Qbonus = 1
        self.actDesc = "Next attack deals (" + str(self.Qbonus) + ") extra damage. Damage permanently increased if it kills enemy. Super Form at 10 stacks."
        self.actCd = (Info.acTime, 3)
        self.actCost = 2
        self.Champ = Nasus
        if not summ:
            Info.champions.append(self)
        self.canUse = True
        self.Q = False
        if hp is not None:
            self.hp = hp
            self.mana = mana
        self.super = False

    def draw(self, screen):
        self.actDesc = "Next attack deals (" + str(self.Qbonus) + ") extra damage. Damage permanently increased if it kills enemy. Super Form at 10 stacks."
        screen.blit(pygame.transform.flip(self.img, self.rot >= 90 or self.rot <= -90,  False), (self.x, self.y))
        if Info.selected is self:
            pygame.draw.circle(screen, (255, 0, 0), (int(self.cx), int(self.cy)), self.atkrange, 5)
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
        if self.Qbonus >= 10 and not self.super:
            self.super = True
            self.maxhp = 20

    def fire(self):
        self.target.takeDamage(self.atk + (self.Qbonus if self.Q else 0))
        self.hp = min(self.hp + 0.25 * (self.atk + (self.Qbonus if self.Q else 0)), self.maxhp)
        if self.super:
            self.hp = min(self.hp + 0.25 * (self.atk + (self.Qbonus if self.Q else 0)), self.maxhp)
        if self.Q:
            self.abiSound.play()
            if self.target is None:
                self.Qbonus += 1
                Info.dieEffect(self.cx, self.y+self.size, 2, (0, 255, 0))
        self.Q = False


    def useAbility(self):
        self.Q = True

