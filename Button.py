import pygame

from Info import Info


class Button:
    def __init__(self, x, y, width, height, screen, color=(255, 0, 0), label=None, ability=False):
        self.coll = pygame.Rect(x, y, width, height)
        self.color = color
        self.screen = screen
        self.label = label
        self.ability = ability

    def tick(self, mousePos, click):
        if self.coll.collidepoint(mousePos[0], mousePos[1]):
            if not self.ability:
                pygame.draw.rect(self.screen, (min(255, self.color[0]+50), min(255, self.color[1]+50), min(255, self.color[2]+50)), self.coll)
                if self.label is not None:
                    self.screen.blit(self.label, (self.coll.x + (self.coll.width - self.label.get_width()) / 2,
                                                  self.coll.y + (self.coll.height - self.label.get_height()) / 2))

            elif pygame.time.get_ticks() - Info.selected.actCd[0] > Info.selected.actCd[1] * 1000:
                pygame.draw.rect(self.screen, (0, 250, 0), self.coll)
                self.label = pygame.font.SysFont("Microsoft Yahei UI Light", 30).render("Use", 1, (255, 255, 255))
                self.screen.blit(self.label, (self.coll.x + (self.coll.width - self.label.get_width()) / 2,
                                              self.coll.y + (self.coll.height - self.label.get_height()) / 2))

            else:
                pygame.draw.rect(self.screen, (100, 100, 100), self.coll)
                self.label = pygame.font.SysFont("Microsoft Yahei UI Light", 30).render("Not Ready", 1, (255, 255, 255))
                self.screen.blit(self.label, (self.coll.x + (self.coll.width - self.label.get_width()) / 2,
                                                 self.coll.y + (self.coll.height - self.label.get_height()) / 2))
                return False
            if click:
                return True

        elif not self.ability:
            pygame.draw.rect(self.screen, self.color, self.coll)
            if self.label is not None:
                self.screen.blit(self.label, (self.coll.x + (self.coll.width - self.label.get_width()) / 2, self.coll.y + (self.coll.height - self.label.get_height()) / 2))

        elif pygame.time.get_ticks() - Info.selected.actCd[0] > Info.selected.actCd[1] * 1000:
            pygame.draw.rect(self.screen, (0, 200, 0), self.coll)
            self.label = pygame.font.SysFont("Microsoft Yahei UI Light", 30).render("Use", 1, (255, 255, 255))
            self.screen.blit(self.label, (self.coll.x + (self.coll.width - self.label.get_width()) / 2,
                                          self.coll.y + (self.coll.height - self.label.get_height()) / 2))

        else:
            pygame.draw.rect(self.screen, (100, 100, 100), self.coll)
            self.label = pygame.font.SysFont("Microsoft Yahei UI Light", 30).render("Not Ready", 1, (255, 255, 255))
            self.screen.blit(self.label, (self.coll.x + (self.coll.width - self.label.get_width()) / 2,
                                          self.coll.y + (self.coll.height - self.label.get_height()) / 2))
        return False

    def changeLabel(self, label):
        self.label = label

