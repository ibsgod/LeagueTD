import random

from Enemy import Enemy
from Info import Info


class Minion(Enemy):
    def __init__(self, x, y, hp):
        super().__init__(x, y, name="Minion", hp=hp, atk=0.5, atkspd=1, speed=10, colour=(200, 0, 0))
        Info.enemies.append(self)