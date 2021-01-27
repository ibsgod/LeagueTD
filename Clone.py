import math
import random

import pygame

from Box import Box
from Champion import Champion
from Info import Info

class Clone(Champion):
    def __init__(self, x, y, targx=None, targy=None, dur=None, summ=False, hp=None, mana=None):
        super().__init__(x, y, summ=None, name="Clone", hp=15, mana=None, atk=1, atkrange=100, atkspd=1, be=None, ranged=None, block=10)
        self.passName = "Jack in the box"
        self.passDesc = "Periodically spawns boxes that attack enemies"
        self.Champ = Clone
        Info.champions.append(self)
        if hp is not None:
            self.hp = hp
        self.boxTimer = Info.acTime + 2000
        self.boxes = []
        self.clones = []
        self.targx = targx
        self.targy = targy
        if targx is None:
            self.targx = x
            self.targy = y
        self.dur = dur

    def draw(self, screen):
        if len(self.atkAnim) > 0 and self.animStart is not None and self.animStart + self.atkspd * 1000 > Info.acTime:
            self.img = self.atkAnim[len(self.atkAnim) - int((self.animStart + self.atkspd * 1000 - Info.acTime) / self.atkspd / 1000 * len(self.atkAnim))-1]
        else:
            self.img = self.idleimg
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

    def tick(self, mousePos, click):
        self.x += math.ceil((self.targx - self.x) / 2)
        self.y += math.ceil((self.targy - self.y) / 2)
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
        self.cx = self.x + self.size / 2
        self.cy = self.y + self.size / 2
        self.hitbox = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        if Info.acTime > self.boxTimer:
            if len(self.boxes) > 4:
                self.boxes.remove(self.boxes[0])
            self.boxes.append(Box(self.cx - 20, self.cy - 20, min(max(0, random.randint(self.cx - 120, self.cx + 80)), 1010), min(max(0, random.randint(self.cy - 120, self.cy + 80)), 510), self))
            self.boxTimer = Info.acTime + 2000
        if Info.acTime > self.dur:
            Info.champions.remove(self)




    def fire(self):
        self.target.takeDamage(self.atk)



