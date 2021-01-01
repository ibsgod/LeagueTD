import math

import pygame

from Info import Info


class Projectile:
    def __init__(self, x, y, angle, tower, pen=False, speed=80, atk=1, name=""):
        self.x = x
        self.y = y
        self.angle = angle
        self.rotate = 0
        self.speed = speed
        self.size = 15
        self.pen = pen
        self.atk = atk
        self.tower = tower
        self.img = pygame.image.load('egg.png')
        self.hitbox = pygame.Rect(self.x, self.y, self.size, self.size)
        self.hit = []
        self.name = name

    def rot_center(self, image, angle):
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=image.get_rect().center)
        return rotated_image, (new_rect[0] + self.x, new_rect[1] + self.y)

    def draw(self, screen):
        tup = self.rot_center(self.img, self.rotate)
        screen.blit(tup[0], tup[1])

    def tick(self):
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y -= math.sin(math.radians(self.angle)) * self.speed
        self.rotate += 10
        self.hitbox = pygame.Rect(self.x, self.y, self.size, self.size)
        if self.x < 0 or self.y < 0 or self.x - 15 > 1050 or self.y - 15 > 550:
            self.tower.projects.remove(self)
            return
        for i in Info.enemies:
            if i.hitbox.colliderect(self.hitbox) and i not in self.hit:
                if self.name == "Ashe":
                    i.cripple((0.5, Info.acTime + 3000))
                if self.name == "Sona":
                    i.cripple((0, Info.acTime + 3000))

                i.takeDamage(self.tower.atk * self.atk)
                if not self.pen:
                    self.tower.projects.remove(self)
                    return
                else:
                    self.hit.append(i)

