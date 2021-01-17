import math

import pygame

from Enemy import Enemy
from Info import Info
from Projectile import Projectile


class Swain(Enemy):
    def __init__(self, x, y, hp):
        super().__init__(x, y, name="Swain", hp=hp, atk=0.5, atkspd=1, speed=5, atkrange=200, colour=(100, 0, 0))
        Info.enemies.append(self)
        self.passName = "Ravenous Flock"
        self.passDesc = "Continously drains health from nearby champions."

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
        if self.slow[0] > 0 or self.slow[1] < Info.acTime:
            for i in Info.champions:
                if self.checkRange((self.cx, self.cy), self.atkrange, i.hitbox):
                    pygame.draw.line(screen, (200, 0, 0), (self.cx, self.cy), (i.cx, i.cy), 5)

    def tick(self, mousePos, click):
        self.target = None
        self.rot = 180
        for i in Info.champions:
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
        if self.target is None:
            self.move()
        if self.slow[0] > 0 or self.slow[1] < Info.acTime:
            for i in Info.champions:
                if self.checkRange((self.cx, self.cy), self.atkrange, i.hitbox):
                    i.takeDamage(0.05)
                    self.hp = min(self.maxhp, self.hp + 0.05)
        if self.hitbox.collidepoint(mousePos) and Info.summoning is None:
            if click:
                Info.selected = self
                return 2
            return 1
        return

    def fire(self):
        self.projects.append(Projectile(self.cx-7, self.cy-7, self.rot, self, name="Swain"))

