import pygame

from Info import Info


class SummButton:
    def __init__(self, x, y, screen, img, Champ, label=None):
        self.screen = screen
        self.label = label
        self.img = pygame.image.load(img)
        self.Champ = Champ
        self.coll = pygame.Rect(x, y, img.get_width(), img.get_height())

    def tick(self, mousePos, click):
        has = False
        for i in Info.champions:
            if isinstance(i, self.Champ):
                has = True
        if has:
            # grayed out champ
            pass
        elif self.coll.collidepoint(mousePos[0], mousePos[1]):
            pygame.draw.rect(self.screen, (min(255, self.color[0]+50), min(255, self.color[1]+50), min(255, self.color[2]+50)), self.coll)
            if self.label is not None:
                self.screen.blit(self.label, (self.coll.x + (self.coll.width - self.label.get_width()) / 2, self.coll.y + (self.coll.height - self.label.get_height()) / 2))
            if click:
                return True
        else:
            pygame.draw.rect(self.screen, self.color, self.coll)
            if self.label is not None:
                self.screen.blit(self.label, (self.coll.x + (self.coll.width - self.label.get_width()) / 2, self.coll.y + (self.coll.height - self.label.get_height()) / 2))
        return False

    def changeLabel(self, label):
        self.label = label

