import random

import pygame


class Info:
    champions = []
    enemies = []
    atkTimers = {}
    selected = None
    enemypath = [(1155, 114), (936, 114), (936, 483), (636, 483), (636, 114), (410, 114), (410, 413), (110, 413)]
    pathareas = [pygame.Rect(1 * 75, 5 * 75, 5 * 75, 1 * 75), pygame.Rect(5 * 75, 1 * 75, 1 * 75, 4 * 75),
                 pygame.Rect(6 * 75, 1 * 75, 3 * 75, 1 * 75), pygame.Rect(8 * 75, 2 * 75, 1 * 75, 5 * 75),
                 pygame.Rect(9 * 75, 3 * 75, 5 * 75, 1 * 75), pygame.Rect(9 * 75, 6 * 75, 4 * 75, 1 * 75),
                 pygame.Rect(12 * 75, 1 * 75, 1 * 75, 5 * 75), pygame.Rect(13 * 75, 1 * 75, 1 * 75, 1 * 75),
                 pygame.Rect(10 * 75, 0 * 75, 1 * 75, 3 * 75)]
    buttDict = {}
    be = 100
    summoning = None
    playTime = 0
    acTime = 0
    particles = []
    po = 4

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
                                    Info.acTime + random.randint(500, 1000)])



