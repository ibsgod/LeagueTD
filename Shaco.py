import math
import random

import pygame

from Box import Box
from Champion import Champion
from Clone import Clone
from Info import Info

class Shaco(Champion):
    def __init__(self, x, y, summ=False, hp=None, mana=None):
        super().__init__(x, y, summ, name="Shaco", hp=15, mana=10, atk=1, atkrange=50, atkspd=1, be=5, ranged=False, block=10)
        self.passName = "Jack in the box"
        self.passDesc = "Periodically spawns boxes that attack enemies"
        self.actName = "Hallucinate"
        self.actDesc = "Creates a clone for a few seconds"
        self.actCd = (Info.acTime, 5)
        self.actCost = 6
        self.Champ = Shaco
        if not summ:
            Info.champions.append(self)
        self.canUse = True
        if hp is not None:
            self.hp = hp
            self.mana = mana
        self.boxes = []
        self.boxTime = 2000
        self.boxTimer = Info.acTime + self.boxTime


    def draw(self, screen):
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
            if Info.acTime > self.boxTimer:
                if len(self.boxes) > 4:
                    self.boxes.remove(self.boxes[0])
                while True:
                    rx = min(max(0, random.randint(self.cx - 120, self.cx + 80)), 1010)
                    ry = min(max(0, random.randint(self.cy - 120, self.cy + 80)), 510)
                    yes = False
                    for i in Info.pathareas:
                        if i.collidepoint(rx + 20, ry + 20):
                            yes = True
                            break
                    if not yes:
                        self.boxes.append(Box(self.cx - 20, self.cy - 20, rx, ry, self))
                        break
                self.boxTimer = Info.acTime + self.boxTime
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
        self.target.takeDamage(self.atk)


    def useAbility(self):
        while True:
            rx = min(max(0, random.randint(self.cx - 52, self.cx + 48)), 1098)
            ry = min(max(0, random.randint(self.cy - 152, self.cy + 48)), 498)
            yes = False
            for i in Info.pathareas:
                if i.collidepoint(rx+52, ry+52):
                    Clone(self.cx - 52, self.cy - 52, rx, ry, dur=Info.acTime + 10000)
                    yes = True
                    break
            if yes:
                break

