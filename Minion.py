import random

from Enemy import Enemy
from Info import Info


class Minion(Enemy):
    def __init__(self, x, y, hp):
        super().__init__(x, y, name="Minion", hp=hp, atk=1, atkspd = 2, speed=10, img="sudo.png")
        Info.enemies.append(self)