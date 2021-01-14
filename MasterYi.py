import math
import random

import pygame

from Champion import Champion
from Info import Info


class MasterYi(Champion):
    def __init__(self, x, y, summ=False, hp=None, mana=None):
        super().__init__(x, y, summ, name="Master Yi", hp=8, mana=10, atk=1, atkrange=80, atkspd=0.4, be=5, ranged=False, block=3)
        self.passName = "Double Strike"
        self.passDesc = "Hits twice every 4th attack"
        self.actName = "Alpha Strike"
        self.actDesc = "Becomes invincible and strikes nearby enemies"
        self.actCd = (Info.acTime, 5)
        self.actCost = 4
        self.Champ = MasterYi
        if not summ:
            Info.champions.append(self)
        self.Qlim = 8
        self.Qed = [None] * self.Qlim
        self.nextQ = 0
        self.Qline = None
        self.canUse = False
        self.attack = 0
        if hp is not None:
            self.hp = hp
            self.mana = mana

    def draw(self, screen):
        if len(self.Qed) == self.Qlim:
            screen.blit(pygame.transform.flip(self.img, self.rot >= 90 or self.rot <= -90,  False), (self.x, self.y))
        elif self.target is not None:
            # screen.blit(tup[0], (self.target.cx - self.size/2, self.target.cy - self.size/2))
             pygame.draw.line(screen, (255, 255, 0), self.Qline[0], self.Qline[1], 5)
        if Info.selected is self:
            pygame.draw.circle(screen, (255, 0, 0), (int(self.cx), int(self.cy)), self.atkrange, 5)
            pygame.draw.circle(screen, (0, 255, 0), (int(self.cx), int(self.cy)), self.atkrange*2, 5)
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
        self.canUse = False
        if not self.summ:
            if len(self.Qed) == self.Qlim:
                self.target = None
                self.blocked = []
                for i in Info.enemies:
                    if self.checkRange((self.cx, self.cy), self.atkrange*2, i.hitbox):
                        self.canUse = True
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
        if len(self.Qed) < self.Qlim and Info.acTime > self.nextQ:
            new = False
            for i in Info.enemies[:]:
                if self.checkRange((self.cx, self.cy) if self.target is None else (self.target.cx, self.target.cy), self.atkrange*2, i.hitbox) and i not in self.Qed:
                    self.target = i
                    if random.randint(1, 2) == 1:
                        self.Qline = (
                        (random.randint(self.target.x - 20, self.target.x + self.target.size + 20), self.target.y - 20),
                        (random.randint(self.target.x - 20, self.target.x + self.target.size + 20),
                         self.target.y + self.target.size + 20))
                    else:
                        self.Qline = (
                        (self.target.x - 20, random.randint(self.target.y - 20, self.target.y + self.target.size + 20)),
                        (self.target.x + self.target.size + 20,
                         random.randint(self.target.y - 20, self.target.y + self.target.size + 20)))
                    new = True
                    break
            if new:
                self.Qed.append(self.target)
            else:
                self.target = None
                while len(self.Qed) < self.Qlim:
                    self.Qed.append(None)
            if len(self.Qed) == self.Qlim:
                for i in self.Qed[:]:
                    if i is not None:
                        i.takeDamage(self.atk*2)
            self.nextQ = Info.acTime + 100
        elif not self.summ:
            self.blocked = []
            for i in Info.enemies:
                if self.checkRange((self.cx, self.cy), self.atkrange, i.hitbox):
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


    def takeDamage(self, dmg):
        if len(self.Qed) < self.Qlim:
            return
        self.hp -= dmg
        if self.hp <= 0:
            self.abiSound.stop()
            Info.dieEffect(self.cx, self.y + self.size, 2, (0, 255, 255))
            Info.champions.remove(self)
            if Info.selected is self:
                Info.selected = None
            for i in Info.enemies:
                if self is i.target:
                    i.target = None

    def fire(self):
        if len(self.Qed) == self.Qlim:
            self.target.takeDamage(self.atk)
            self.attack += 1
            if self.attack % 4 == 0 and self.target is not None:
                self.target.takeDamage(self.atk)

    def useAbility(self):
        self.Qed.clear()

