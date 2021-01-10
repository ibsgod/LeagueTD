import math
import random

import pygame

from Champion import Champion
from Info import Info
from Poison import Poison


class Singed(Champion):
    def __init__(self, x, y, summ=False, hp=None, mana=None):
        super().__init__(x, y, summ, name="Singed", hp=20, mana=10, atk=1, atkrange=100, atkspd=1, be=5, ranged=False, block=4, img="sudo.png")
        self.passName = "Fart"
        self.passDesc = "Farts so bad it hurts enemies"
        self.actName = "Sanik"
        self.actDesc = "Runs this shit like cardio"
        self.actCd = (0, 0.5)
        self.actCost = 0.05
        self.Champ = Singed
        if not summ:
            Info.champions.append(self)
        self.canUse = True
        if hp is not None:
            self.hp = hp
            self.mana = mana
        self.running = False
        self.dir = -1
        self.speed = 20
        self.path = 0
        min = (999999, None)
        for i in range(len(Info.enemypath)):
            if (self.x - Info.enemypath[i][0]) ** 2 + (self.y - Info.enemypath[i][1]) ** 2 < min[0]:
                min = ((self.x - Info.enemypath[i][0]) ** 2 + (self.y - Info.enemypath[i][1]) ** 2, Info.enemypath[i])
                self.path = i
        self.x = min[1][0] - self.size / 2
        self.y = min[1][1] - self.size / 2
        self.cx = self.x + self.size / 2
        self.cy = self.y + self.size / 2
        self.hitbox = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        Info.poison = []

        
    def draw(self, screen):
        if not self.running:
            screen.blit(pygame.transform.flip(self.img, self.rot >= 90 or self.rot <= -90,  False), (self.x, self.y))
        else:
            screen.blit(pygame.transform.flip(self.img, self.dir == 1 and self.path != 1 or self.path == 7,  False), (self.x, self.y))
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
        else:
            for i in Info.enemypath[1:]:
                pygame.draw.rect(screen, (255, 0, 0), (i[0] - 5, i[1] - 5, 10, 10))

    def tick(self, mousePos, click):
        if self.path == len(Info.enemypath)-1:
            self.dir = -1
        if self.path == 1:
            self.dir = 1
        if self.mana <= 0:
            self.running = False
        if self.running and Info.playing:
            self.mana = max(0, self.mana-0.05)
            if self.cx != Info.enemypath[self.path][0]:
                if abs(Info.enemypath[self.path][0] - (self.cx)) > self.speed:
                    self.x += self.speed * (Info.enemypath[self.path][0] - (self.cx)) / abs(
                        Info.enemypath[self.path][0] - (self.cx))
                else:
                    self.x += Info.enemypath[self.path][0] - (self.cx)
            if self.cy != Info.enemypath[self.path][1]:
                if abs(Info.enemypath[self.path][1] - (self.cy)) > self.speed:
                    self.y += self.speed * (Info.enemypath[self.path][1] - (self.cy)) / abs(
                        Info.enemypath[self.path][1] - (self.cy))
                else:
                    self.y += Info.enemypath[self.path][1] - (self.cy)
            if self.cx == Info.enemypath[self.path][0] and self.cy == Info.enemypath[self.path][1]:
                self.path += self.dir
        self.cx = self.x + self.size / 2
        self.cy = self.y + self.size / 2
        self.hitbox = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
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
                    if len(self.blocked) < self.block and not self.running:
                        self.blocked.append(i)
            if Info.playing:
                Info.poison.append(Poison(self.cx, self.cy + 10,
                      random.randint(-10, 3) / 10 * -self.dir,
                      random.randint(-10, 3) / 10,
                      random.randint(5, 10), (
                          150 + random.randint(-10, 10),
                          0 + random.randint(0, 10),
                          150 + random.randint(-10, 10)),
                      Info.acTime + random.randint(500, 1500), self))
                if len(Info.poison) > 70:
                    Info.poison.remove(Info.poison[0])
            if self.hitbox.collidepoint(mousePos) and Info.summoning is None:
                if click:
                    Info.selected = self
                    return 2
                return 1
        else:
            min = (999999, None)
            for i in Info.enemypath[1:]:
                if (mousePos[0] - i[0])**2 + (mousePos[1] - i[1])**2 < min[0]:
                    min = ((mousePos[0] - i[0])**2 + (mousePos[1] - i[1])**2, i)
            self.x = min[1][0] - self.size/2
            self.y = min[1][1] - self.size/2
        self.cx = self.x + self.size / 2
        self.cy = self.y + self.size / 2
        self.hitbox = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())



    def fire(self):
        self.target.takeDamage(self.atk)


    def useAbility(self):
        self.running = not self.running

