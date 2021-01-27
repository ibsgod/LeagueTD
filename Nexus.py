import pygame

from Info import Info


class Nexus:
    def __init__(self, x, y, hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.maxhp = hp
        self.size = 120
        self.name = "Nexus"
        self.hitbox = pygame.Rect(self.x, self.y, self.size, self.size)
        self.colour = (200, 200, 255)

    def draw(self, screen):
        maxbar = pygame.Surface((self.size, 5))
        maxbar.set_alpha(80)
        maxbar.fill((0, 0, 0))
        screen.blit(maxbar, (self.x + (self.size - maxbar.get_width()) / 2, self.y - 15))
        pygame.draw.rect(screen, (min(255, int((self.maxhp - self.hp) * 255 / (self.maxhp))),
                                  max(0, int(255 - (self.maxhp - self.hp) * 255 / (self.maxhp))), 0), (
                             self.x + (self.size - maxbar.get_width()) / 2, self.y - 15,
                             max(0, maxbar.get_width() / self.maxhp * self.hp), 5))


    def tick(self, mousePos, click):
        for i in Info.enemies[:]:
            if i.hitbox.colliderect(self.hitbox):
                self.hp -= 1
                Info.enemies.remove(i)

        if self.hitbox.collidepoint(mousePos) and Info.summoning is None:
            if click:
                Info.selected = self
                return 2
            return 1
        return
