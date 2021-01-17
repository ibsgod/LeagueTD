import math
from math import ceil

import pygame

from Info import Info
from Projectile import Projectile


class Box:
    def __init__(self, x, y, targx, targy, tower):
        self.x = x
        self.y = y
        self.img = pygame.image.load("sudo.png")
        try:
            self.img = pygame.image.load(name.lower().replace(" ", "") + ".png")
        except:
            pass
        self.idleimg = self.img
        self.rot = 0
        self.name = "Box"
        self.atk = 0.5
        self.atkspd = 1
        self.tower = tower
        self.atkrange = 150
        self.size = self.img.get_width()
        self.cx = self.x + self.size / 2
        self.cy = self.y + self.size / 2
        self.targx = targx
        self.targy = targy
        Info.atkTimers[self] = Info.acTime
        self.hitbox = pygame.Rect(self.x, self.y, self.size, self.size)
        self.projects = []
        try:
            self.fireSound = pygame.mixer.Sound(self.name.lower().replace(" ", "") + "atk.wav")
        except:
            self.fireSound = None
        self.atkAnim = []
        i = 1
        while True:
            try:
                self.atkAnim.append(pygame.image.load(self.name.lower().replace(" ", "") + str(i) + ".png"))
                i += 1
            except:
                break
        self.animStart = None
        self.firing = True


    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.img, self.rot >= 90 or self.rot <= -90, False), (self.x, self.y))
        if Info.selected is self:
            pygame.draw.circle(screen, (255, 0, 0), (int(self.cx), int(self.cy)), self.atkrange+50, 5)

    def tick(self, mousePos, click):
        self.x += ceil((self.targx - self.x) / 2)
        self.y += ceil((self.targy - self.y) / 2)
        self.target = None
        for i in Info.enemies:
            if self.tower.checkRange((self.cx, self.cy), self.atkrange, i.hitbox):
                if self.target is None:
                    if i.cx - self.cx != 0:
                        self.rot = math.degrees(math.atan((self.cy - i.cy) / (i.cx - self.cx)))
                    else:
                        if self.cy > i.cy:
                            self.rot = 90
                        else:
                            self.rot = -90
                self.target = i
                if i.cx < self.cx:
                    self.rot -= 180
                break
        self.hitbox = pygame.Rect(self.x, self.y, self.size, self.size)
        self.cx = self.x + self.size / 2
        self.cy = self.y + self.size / 2
        if self.hitbox.collidepoint(mousePos) and Info.summoning is None:
            if click:
                Info.selected = self
                return 2
            return 1
        return

    def fire(self):
        self.projects.append(Projectile(self.cx - 7, self.cy - 7, self.rot, self, name="Box"))