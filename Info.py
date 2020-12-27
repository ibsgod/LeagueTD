import pygame


class Info:
    champions = []
    enemies = []
    atkTimers = {}
    selected = None
    enemypath = [(1155, 114), (936, 114), (936, 483), (636, 483), (636, 114), (410, 114), (410, 413), (110, 413)]
    pathareas = []
    pathareas.append(pygame.Rect(1*75, 5*75, 5*75, 1*75))
    pathareas.append(pygame.Rect(5*75, 1*75, 1*75, 4*75))
    pathareas.append(pygame.Rect(6*75, 1*75, 3*75, 1*75))
    pathareas.append(pygame.Rect(8*75, 2*75, 1*75, 5*75))
    pathareas.append(pygame.Rect(9*75, 3*75, 5*75, 1*75))
    pathareas.append(pygame.Rect(9*75, 6*75, 4*75, 1*75))
    pathareas.append(pygame.Rect(12*75, 1*75, 1*75, 5*75))
    pathareas.append(pygame.Rect(13*75, 1*75, 1*75, 1*75))
    pathareas.append(pygame.Rect(10*75, 0*75, 1*75, 3*75))
    buttDict = {}
    be = 10
    summoning = None
