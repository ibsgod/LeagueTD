import math

import pygame

from Info import Info

# base template class for champions
class Champion:
    # initializing with base stats and location
    def __init__(self, x, y, summ, name, hp, mana, atk, atkrange, atkspd, be, ranged, block=0):
        self.x = x
        self.y = y
        self.name = name
        self.hp = hp
        self.maxhp = hp
        self.mana = mana
        self.maxmana = mana
        self.atk = atk
        self.atkrange = atkrange
        self.atkspd = atkspd
        self.oriatkspd = atkspd
        self.rot = 0
        self.be = be
        self.ranged = ranged
        # loading image
        self.img = pygame.image.load("sudo.png")
        try:
            self.img = pygame.image.load("ChampSprites/" + name.lower().replace(" ", "") + ".png")
        except:
            pass
        self.idleimg = self.img
        self.size = self.img.get_width()
        self.hitbox = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        self.cx = self.x + self.size / 2
        self.cy = self.y + self.size / 2
        self.projects = []
        self.target = None
        self.summ = summ
        self.block = block
        self.blocked = []
        Info.atkTimers[self] = Info.acTime
        # loading audio
        try:
            self.fireSound = pygame.mixer.Sound(self.name.lower().replace(" ", "") + "atk.wav")
        except:
            self.fireSound = None
        try:
            self.abiSound = pygame.mixer.Sound(self.name.lower().replace(" ", "") + "abi.wav")
        except:
            self.abiSound = None
        self.atkAnim = []
        i = 1
        # loading animation sprites
        while True:
            try:
                self.atkAnim.append(pygame.image.load("ChampSprites/" + self.name.lower().replace(" ", "") + str(i) + ".png"))
                i += 1
            except:
                break
        self.animStart = None
        self.firing = True

    # draw method
    def draw(self, screen):
        # animation logic for scaling with attack speed
        if len(self.atkAnim) > 0 and self.animStart is not None and self.animStart + self.atkspd * 1000 > Info.acTime:
            self.img = self.atkAnim[len(self.atkAnim) - int((self.animStart + self.atkspd * 1000 - Info.acTime) / self.atkspd / 1000 * len(self.atkAnim))-1]
        else:
            self.img = self.idleimg
        screen.blit(pygame.transform.flip(self.img, self.rot >= 90 or self.rot <= -90,  False), (self.x, self.y))
        # draw attack range circle if champion is selected
        if Info.selected is self:
            pygame.draw.circle(screen, (255, 0, 0), (int(self.cx), int(self.cy)), self.atkrange+40, 5)
        # drawing health and mana bars above head
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

    # tick method handles all logic for champ during each frame
    def tick(self, mousePos, click):
        if not self.summ:
            self.target = None
            self.blocked = []
            # range detection for champions
            for i in Info.enemies:
                if self.checkRange((self.cx, self.cy), self.atkrange, i.hitbox):
                    if self.target is None:
                        # EPIC TRIGONOMETRY to find angle to shoot targeted enemy
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
                        break
                    # blocking enemies for melee champs
                    if len(self.blocked) < self.block:
                        self.blocked.append(i)
            self.cx = self.x + self.size / 2
            self.cy = self.y + self.size / 2
            self.hitbox = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
            # checking if player clicked on champion to select
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


    # logic for checking rectangle-circle collision
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

    # taking damage and removing champ if dead
    def takeDamage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            Info.dieEffect(self.cx, self.y + self.size, 2, (0, 255, 255))
            Info.champions.remove(self)
            for j in Info.champions:
                j.atkspd = j.oriatkspd
            if Info.selected is self:
                Info.selected = None
            for i in Info.enemies:
                if self is i.target:
                    i.target = None









