import pygame

from Info import Info


class SummButton:
    def __init__(self, x, y, screen, Champ, label=None, img=None):
        self.screen = screen
        self.label = label
        # self.img = pygame.image.load(img)
        self.Champ = Champ
        self.champy = Champ(0, 0, summ=True)
        self.coll = pygame.Rect(x, y, 150, 100)

    def tick(self, mousePos, click):
        has = False
        for i in Info.champions:
            if isinstance(i, self.Champ):
                has = True
        if has or Info.be < self.champy.be:
            pygame.draw.rect(self.screen, (100, 100, 100), self.coll)
        else:
            pygame.draw.rect(self.screen, (0, 200, 0), self.coll)
        if self.coll.collidepoint(mousePos[0], mousePos[1]):
            maxbar = pygame.Surface((self.coll.width, self.coll.height))
            maxbar.set_alpha(20)
            maxbar.fill((255, 255, 255))
            self.screen.blit(maxbar, (self.coll.x, self.coll.y))
            if click and not has and Info.be >= self.champy.be:
                return 2
            return 1
        return 0

    def changeLabel(self, label):
        self.label = label

