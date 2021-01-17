import random

import pygame

from Info import Info


class Enemy:
    def __init__(self, x, y, name, hp, atk, atkspd, speed, atkrange=80, colour=(200, 0, 0)):
        self.x = x
        self.y = y
        self.name = name
        self.hp = hp
        self.maxhp = hp
        self.atk = atk
        self.atkspd = atkspd
        self.speed = speed
        self.img = pygame.image.load("sudo.png")
        try:
            self.img = pygame.image.load("EnemySprites/" + name.lower().replace(" ", "") + ".png")
        except:
            pass
        self.idleimg = self.img
        self.path = 1
        self.width = self.img.get_width()
        self.height = self.img.get_width()
        self.size = self.img.get_width()
        self.cx = self.x + self.width/2
        self.cy = self.y + self.height/2
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.slow = (1, 0)
        self.target = None
        self.projects = []
        self.atkrange = atkrange
        self.colour = colour
        self.rot = 0
        Info.atkTimers[self] = Info.acTime
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
        if len(self.atkAnim) > 0 and self.animStart is not None and self.animStart + self.atkspd * 1000 > Info.acTime:
            self.img = self.atkAnim[len(self.atkAnim) - int((self.animStart + self.atkspd * 1000 - Info.acTime) / self.atkspd / 1000 * len(self.atkAnim))-1]
        else:
            self.img = self.idleimg
        screen.blit(pygame.transform.flip(self.img, self.rot >= 90 or self.rot <= -90,  False), (int(self.x), int(self.y)))
        if Info.selected is self:
            pygame.draw.circle(screen, (255, 0, 0), (int(self.cx), int(self.cy)), self.atkrange+50, 5)
        maxbar = pygame.Surface((self.size, 5))
        maxbar.set_alpha(80)
        maxbar.fill((0, 0, 0))
        screen.blit(maxbar, (self.x + (self.size - maxbar.get_width()) / 2, self.y - 15))
        pygame.draw.rect(screen, (min(255, int((self.maxhp - self.hp) * 255 / (self.maxhp))),
                                  max(0, int(255 - (self.maxhp - self.hp) * 255 / (self.maxhp))), 0), (
                         self.x + (self.size - maxbar.get_width()) / 2, self.y - 15,
                         max(0, maxbar.get_width() / self.maxhp * self.hp), 5))

    def tick(self, mousePos, click):
        yes = False
        self.target = None
        self.rot = 180
        for i in Info.champions:
            if i.blocked is not None and self in i.blocked:
                self.target = i
                yes = True
                if self.cx < i.cx:
                    self.rot -= 180
                break
        if not yes and Info.playing:
            self.move()
        if self.hitbox.collidepoint(mousePos) and Info.summoning is None:
            if click:
                Info.selected = self
                return 2
            return 1
        return

    def move(self):
        newspeed = self.speed
        if self.slow[1] > Info.acTime:
            newspeed *= self.slow[0]
        if self.path < len(Info.enemypath):
            if self.cx != Info.enemypath[self.path][0]:
                if abs(Info.enemypath[self.path][0] - (self.cx)) > newspeed:
                    self.x += newspeed * (Info.enemypath[self.path][0] - (self.cx)) / abs(Info.enemypath[self.path][0] - (self.cx))
                else:
                    self.x += Info.enemypath[self.path][0] - (self.cx)
            if self.cy != Info.enemypath[self.path][1]:
                if abs(Info.enemypath[self.path][1] - (self.cy)) > newspeed:
                    self.y += newspeed * (Info.enemypath[self.path][1] - (self.cy)) / abs(Info.enemypath[self.path][1] - (self.cy))
                else:
                    self.y += Info.enemypath[self.path][1] - (self.cy)
            if self.cx == Info.enemypath[self.path][0] and self.cy == Info.enemypath[self.path][1]:
                self.path += 1
        self.cx = self.x + self.width / 2
        self.cy = self.y + self.height / 2
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def takeDamage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            Info.dieEffect(self.cx, self.y + self.size, 2, self.colour)
            if self in Info.enemies:
                Info.enemies.remove(self)
            if Info.selected is self:
                Info.selected = None
            for i in Info.champions:
                if self is i.target:
                    i.target = None

    def fire(self):
        self.target.takeDamage(self.atk)

    def cripple(self, crip):
        if crip[0] < self.slow[0] or crip[0] == self.slow[0] and crip[1] > self.slow[1]:
            self.slow = crip

    def checkRange(self, pos, rad, rect):
        distx = abs(pos[0] - rect.x - rect.width/2)
        disty = abs(pos[1] - rect.y - rect.height/2)
        if distx > (rect.width / 2 + rad):
            return False
        if disty > (rect.height / 2 + rad):
            return False
        if distx <= (rect.width / 2):
            return True
        if disty <= (rect.height / 2):
            return True
        cornerDistance_sq = (distx - rect.width / 2) ** 2 + (disty - rect.height / 2) ** 2
        return (cornerDistance_sq <= (rad ** 2))