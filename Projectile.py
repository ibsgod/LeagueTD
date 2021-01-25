import math
import random

import pygame

from Info import Info


class Projectile:
    def __init__(self, x, y, angle, tower, pen=False, speed=80, atk=1, name=""):
        self.x = x
        self.y = y
        self.angle = angle
        self.rotate = angle
        self.speed = speed
        self.pen = pen
        self.atk = atk
        self.tower = tower
        self.img = pygame.image.load('egg.png')
        if tower.name == "Ashe":
            self.img = pygame.image.load('asheprojectile.png')
        if name == "Sona":
            self.img = pygame.transform.scale(pygame.image.load('sonaprojectile' + str(random.randint(1,2)) + '.png'), (40, 40))
        if name == "sonault":
            self.img = pygame.image.load('sonault.png')
        self.size = self.img.get_width()
        if self.angle < -90 and self.angle > -270:
            self.img = pygame.transform.flip(self.img, False, True)
        self.hitbox = pygame.Rect(self.x, self.y, self.size, self.size)
        self.hit = []
        self.name = name
        self.rotated_image = pygame.transform.rotate(self.img, self.rotate)

    def draw(self, screen):
        self.new_rect = self.rotated_image.get_rect(center=self.img.get_rect().center)
        self.tup = (self.rotated_image, (self.new_rect[0] + self.x, self.new_rect[1] + self.y))
        screen.blit(self.tup[0], self.tup[1])

    def tick(self):
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y -= math.sin(math.radians(self.angle)) * self.speed
        self.hitbox = pygame.Rect(self.x, self.y, self.size, self.size)
        if self.x < 0 or self.y < 0 or self.x - 15 > 1050 or self.y - 15 > 550:
            self.tower.projects.remove(self)
            return
        if self.tower in Info.champions or self.name == "Box":
            for i in Info.enemies:
                if i.hitbox.colliderect(self.hitbox) and i not in self.hit:
                    if self.name == "Ashe":
                        i.cripple((0.5, Info.acTime + 3000))
                    if self.name == "sonault":
                        i.cripple((0, Info.acTime + 3000))
                    i.takeDamage(self.tower.atk * self.atk)
                    if not self.pen:
                        self.tower.projects.remove(self)
                        return
                    else:
                        self.hit.append(i)
        elif self.tower in Info.enemies:
            for i in Info.champions:
                if i.hitbox.colliderect(self.hitbox) and i not in self.hit:
                    i.takeDamage(self.tower.atk * self.atk)
                    if not self.pen:
                        self.tower.projects.remove(self)
                        return
                    else:
                        self.hit.append(i)


