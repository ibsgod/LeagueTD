import sys

import os
import pygame

from Ashe import Ashe
from Button import Button
from Champion import Champion
from Info import Info
from Minion import Minion
from Sidebar import Sidebar

pygame.mixer.init()
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
width = 1300
height = 650
screen = pygame.display.set_mode((width, height))
screen.fill((0, 0, 50))
Info.screen = screen
click = False
mouse = False
mousePos = None
a = Ashe(400, 200)
sidebar = Sidebar()
minSpawnTimer = 0
img = pygame.image.load("bg.png")
def play():
    global mouse
    global mousePos
    global click
    global minSpawnTimer
    while True:
        screen.fill((200, 30, 150))
        screen.blit(img, (0, 0))
        mousePos = pygame.mouse.get_pos()
        currentTime = pygame.time.get_ticks()
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pause()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        deselect = click and mousePos[0] < 1050 and mousePos[1] < 550
        if currentTime - minSpawnTimer > 1500:
            Minion(Info.enemypath[0][0] - 30, Info.enemypath[0][1] - 30)
            minSpawnTimer = currentTime
        for i in Info.champions:
            if i.tick(mousePos, click) == 2:
                deselect = False
            if i.target is not None and currentTime - Info.atkTimers[i] > i.atkspd * 1000:
                i.fire()
                Info.atkTimers[i] = currentTime
            for j in i.projects:
                j.tick()
        for i in Info.enemies:
            if i.tick(mousePos, click) == 2:
                deselect = False
        if deselect:
            Info.selected = None
        if Info.selected is None or not isinstance(Info.selected, Champion):
            Info.buttDict["sell"] = None
            Info.buttDict["use"] = None
        elif Info.buttDict["sell"] is None:
            Info.buttDict["sell"] = Button(1125, 0, 100, 40, screen,
                                                 label=pygame.font.SysFont("Microsoft Yahei UI Light", 30).render(
                                                     "Sell", 1, (255, 255, 255)))
            Info.buttDict["use"] = Button(1075, 0, 200, 40, screen, ability=True)
        for i in Info.champions:
            i.draw(screen)
            for j in i.projects:
                j.draw(screen)
        # for i in Info.enemypath:
        #     pygame.draw.rect(screen, (255, 0, 0), (i[0] - 5, i[1] - 5, 10, 10))
        for i in Info.enemies:
            i.draw(screen)
        pygame.draw.rect(screen, (0, 0, 255), (0, 550, 1200, 100))
        sidebar.draw(screen, Info.selected)
        for i in Info.buttDict:
            if Info.buttDict[i] is not None:
                if Info.buttDict[i].tick(mousePos, click):
                    if i == "use":
                        Info.selected.actCd = (pygame.time.get_ticks(), Info.selected.actCd[1])
        pygame.display.update()
        pygame.time.Clock().tick(60)

def pause():
    global mouse
    global click
    global mousePos
    while True:
        #screen.fill((200, 30, 150))
        mousePos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            click = False
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                return
        for i in Info.champions:
            i.draw(screen)
            for j in i.projects:
                j.draw()
        # for i in Info.enemypath:
        #     pygame.draw.rect(screen, (255, 0, 0), (i[0] - 5, i[1] - 5, 10, 10))
        for i in Info.enemies:
            i.draw(screen)
        pygame.draw.rect(screen, (0, 0, 255), (0, 550, 1200, 100))
        sidebar.draw(screen, Info.selected)
        pygame.display.update()
        pygame.time.Clock().tick(30)


play()
