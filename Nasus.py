import math
import random

import pygame

from Champion import Champion
from Info import Info


class Nasus(Champion):
    def __init__(self, x, y, summ=False, hp=None, mana=None):
        super().__init__(x, y, summ, name="Nasus", hp=15, mana=10, atk=1, atkrange=100, atkspd=1, be=5, ranged=False, block=2, img="sudo.png")
        self.passName = "Soul Eater"
        self.passDesc = "Gains HP when attacking"
        self.actName = "Siphoning Strike"
        self.Qbonus = 1
        self.actDesc = "Next attack deals (" + str(self.Qbonus) + ") extra damage. Damage permanently increased if it kills enemy."
        self.actCd = (0, 5)
        self.actCost = 4
        self.Champ = Nasus
        if not summ:
            Info.champions.append(self)
        self.canUse = True
        self.Q = False
        if hp is not None:
            self.hp = hp
            self.mana = mana

    def draw(self, screen):
        self.actDesc = "Next attack deals (" + str(self.Qbonus) + ") extra damage. Damage permanently increased if it kills enemy."
        tup = self.rot_center(pygame.transform.flip(self.img, False, self.rot >= 90 or self.rot <= -90), self.rot)
        screen.blit(tup[0], tup[1])
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


    def fire(self):
        self.target.takeDamage(self.atk + (self.Qbonus if self.Q else 0))
        self.hp = min(self.hp + 0.5 * (self.atk + (self.Qbonus if self.Q else 0)), self.maxhp)
        if self.Q and self.target is None:
            self.Qbonus += 1
            Info.dieEffect(self.cx, self.y+self.size, 2, (0, 255, 0))
        self.Q = False


    def useAbility(self):
        self.Q = True

