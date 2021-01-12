import random

import pygame

class Info:
    champions = []
    enemies = []
    atkTimers = {}
    selected = None
    enemypath = [(1050, 114), (938, 114), (937, 485), (636, 485), (635, 114), (412, 114), (411, 413), (110, 413)]
    pathareas = [pygame.Rect(1 * 75, 5 * 75, 5 * 75, 1 * 75), pygame.Rect(5 * 75, 1 * 75, 1 * 75, 4 * 75),
                 pygame.Rect(6 * 75, 1 * 75, 3 * 75, 1 * 75), pygame.Rect(8 * 75, 2 * 75, 1 * 75, 5 * 75),
                 pygame.Rect(9 * 75, 3 * 75, 5 * 75, 1 * 75), pygame.Rect(9 * 75, 6 * 75, 4 * 75, 1 * 75),
                 pygame.Rect(12 * 75, 1 * 75, 1 * 75, 5 * 75), pygame.Rect(13 * 75, 1 * 75, 1 * 75, 1 * 75),
                 pygame.Rect(10 * 75, 0 * 75, 1 * 75, 3 * 75)]
    buttDict = {}
    be = 1000
    summoning = None
    acTime = 0
    particles = []
    poison = []
    rounds = 1
    playing = False
    highscore = 0
    def dieEffect(x, y, size, colour):
        for i in range(50):
            Info.particles.append([random.randint(x - 10 * size, x + 10 * size),
                                    random.randint(y - 2 * size, y + 2 * size),
                                    random.randint(-30, 30) / 10,
                                    random.randint(-60, 3) / 10,
                                    random.randint(size, size*2), (
                                    min(255, max(0, colour[0] + random.randint(-10, 10))),
                                    min(255, max(0, colour[1] + random.randint(-10, 10))),
                                    min(255, max(0, colour[2] + random.randint(-10, 10)))),
                                    Info.acTime + random.randint(-300 + 300*size, 300 + 300*size)])



