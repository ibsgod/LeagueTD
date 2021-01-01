import pygame

from Info import Info


class Poison:
    def __init__(self, x, y, xvel, yvel, size, colour, dur, tower):
        self.x = x
        self.y = y
        self.xvel = xvel
        self.yvel = yvel
        self.size = size
        self.colour = colour
        self.dur = dur
        self.hit = []
        self.tower = tower

    def tick(self, screen):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size)
        self.x += self.xvel
        self.y += self.yvel
        if self.dur < Info.acTime:
            Info.poison[str(id(self.tower))].remove(self)
        for i in Info.enemies:
            if i not in self.hit and i.hitbox.collidepoint(self.x+self.size/2, self.y+self.size/2):
                self.hit.append(i)
                i.takeDamage(self.tower.atk/10)

