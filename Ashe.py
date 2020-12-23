import pygame

from Champion import Champion
from Info import Info

class Ashe(Champion):
    def __init__(self, x, y):
        super().__init__(x, y, name="Ashe", hp=10, mana=10, atk=1, atkrange=400, atkspd=0.5, be=5, img="sudo.png")
        self.passName = "Frost Shot"
        self.passDesc = "Slows enemies hit by attacks"
        self.actName = "Volley"
        self.actDesc = "Fires a splay of arrows"
        self.actCd = (0, 5)
        Info.champions.append(self)
        Info.atkTimers[self] = pygame.time.get_ticks()
