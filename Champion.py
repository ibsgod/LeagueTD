import math

import pygame

from Info import Info
from Projectile import Projectile


class Champion:
    def __init__(self, x, y, name, hp, mana, atk, atkrange, atkspd, be, img):
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
        self.rot = 0
        self.be = be
        self.img = pygame.image.load(img)
        self.size = self.img.get_width()
        self.hitbox = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        self.cx = self.x + self.img.get_width() / 2
        self.cy = self.y + self.img.get_height() / 2
        self.projects = []
        self.target = None

    def rot_center(self, image, angle):
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=image.get_rect().center)
        return rotated_image, (new_rect[0] + self.x, new_rect[1] + self.y)

    def draw(self, screen):
        tup = self.rot_center(pygame.transform.flip(self.img, False, self.rot >= 90 or self.rot <= -90), self.rot)
        screen.blit(tup[0], tup[1])
        if Info.selected is self:
            pygame.draw.circle(screen, (255, 0, 0), (int(self.cx), int(self.cy)), self.atkrange, 5)
        maxbar = pygame.Surface((self.size, 5))
        maxbar.set_alpha(80)
        maxbar.fill((0, 0, 0))
        screen.blit(maxbar, (self.x + (self.size - maxbar.get_width()) / 2, self.y - 15))
        pygame.draw.rect(screen, (min(255, int((self.maxhp - self.hp) * 255 / (self.maxhp - 1))),
                                  max(0, int(255 - (self.maxhp - self.hp) * 255 / (self.maxhp - 1))), 0), (
                             self.x + (self.size - maxbar.get_width()) / 2, self.y - 15,
                             max(0, maxbar.get_width() / self.maxhp * self.hp), 5))
        screen.blit(maxbar, (self.x + (self.size - maxbar.get_width()) / 2, self.y - 15 + maxbar.get_height()))
        pygame.draw.rect(screen, (0, 100, 200), (
                             self.x + (self.size - maxbar.get_width()) / 2, self.y - 15 + maxbar.get_height(),
                             max(0, maxbar.get_width() / self.maxmana * self.mana), 5))

    def tick(self, mousePos, click):
        self.target = None
        for i in Info.enemies:
            if self.checkRange(i.hitbox):
                if i.cx - self.cx != 0:
                    self.rot = math.degrees(math.atan((self.cy - i.cy) / (i.cx - self.cx)))
                if i.cx < self.cx:
                    self.rot -= 180
                self.target = i
                break
        if self.hitbox.collidepoint(mousePos):
            if click:
                Info.selected = self
                return 2
            return 1
        return
    


    def checkRange(self, rect):
        distx = abs(self.cx - rect.x - rect.width/2)
        disty = abs(self.cy - rect.y - rect.height/2)
        if distx > (rect.width / 2 + self.atkrange):
            return False
        if disty > (rect.height / 2 + self.atkrange):
            return False
        if distx <= (rect.width / 2):
            return True
        if disty <= (rect.height / 2):
            return True
        cornerDistance_sq = (distx - rect.width / 2) ** 2 + (disty - rect.height / 2) ** 2
        return (cornerDistance_sq <= (self.atkrange ** 2))

    def fire(self):
        self.projects.append(Projectile(self.cx-7, self.cy-7, self.rot, self))





