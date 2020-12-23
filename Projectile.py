import math

import pygame

from Info import Info


class Projectile:
    def __init__(self, x, y, angle, tower):
        self.x = x
        self.y = y
        self.angle = angle
        self.rotate = 0
        self.speed = 80
        self.size = 15
        self.tower = tower
        self.img = pygame.image.load('egg.png')
        self.hitbox = pygame.Rect(self.x, self.y, self.size, self.size)
        self.hit = []

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
        for i in Info.enemies:
            if i.hitbox.colliderect(self.hitbox) and i not in self.hit:
                i.takeDamage(self.tower.atk)
                self.hit.append(i)
                self.tower.projects.remove(self)
                break

