import sys

import os
import pygame
import json

from Ashe import Ashe
from Button import Button
from Champion import Champion
from Info import Info
from Lulu import Lulu
from MasterYi import MasterYi
from Minion import Minion
from Nasus import Nasus
from Sidebar import Sidebar
from Singed import Singed
from Sona import Sona
from SummButton import SummButton

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
sidebar = Sidebar()
manaTimer = 0
img = pygame.image.load("bg.png")
Info.buttDict["Ashe"] = SummButton(0, 550, screen, Ashe)
Info.buttDict["MasterYi"] = SummButton(150, 550, screen, MasterYi)
Info.buttDict["Sona"] = SummButton(300, 550, screen, Sona)
Info.buttDict["Lulu"] = SummButton(450, 550, screen, Lulu)
Info.buttDict["Nasus"] = SummButton(600, 550, screen, Nasus)
Info.buttDict["Singed"] = SummButton(750, 550, screen, Singed)
Info.rounds = 1
currentTime = 0
pauseTime = 0
time = 0
hovering = None
data = ""
playing = False
startPause = 0
roundLine = 0
currIter = 0
nextTime = 0
startLine = 0
try:
    with open("state.txt") as file:
        data = json.load(file)
except:
    pass
if len(data) > 0:
    Info.be = data["be"]
    Info.playTime = data["playTime"]
    Info.rounds = data["rounds"]
    for i in data["champions"]:
        c = eval(i["name"])(i["x"], i["y"], hp=i["hp"], mana=i["mana"])
        if i["name"] == "Nasus":
            c.Qbonus = i["Qbonus"]
roundInfo = None
with open("rounds.txt") as file:
    roundInfo = file.readlines()
    space = lambda x: x.split(' ')
    removeNewLine = lambda x: x.replace('\n', '')
    roundInfo = list(map(removeNewLine, roundInfo))
    roundInfo = list(map(space, roundInfo))

def play():
    global mouse
    global mousePos
    global click
    global minSpawnTimer
    global manaTimer
    global pauseTime
    global time
    global hovering
    global playing
    global startPause
    global currIter
    global nextTime
    global roundLine
    global startLine
    while True:
        screen.fill((200, 30, 150))
        screen.blit(img, (0, 0))
        mousePos = pygame.mouse.get_pos()
        currentTime = pygame.time.get_ticks()
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                if playing:
                    startPause = pygame.time.get_ticks()
                pause()
                if playing:
                    pauseTime += pygame.time.get_ticks() - startPause
                currentTime = pygame.time.get_ticks()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        time = (Info.playTime + currentTime - pauseTime)
        Info.acTime = time
        deselect = click and mousePos[0] < 1050 and mousePos[1] < 550
        if playing and Info.acTime > nextTime and roundInfo[roundLine][0] != '-':
            if roundInfo[roundLine][0] == "m":
                Minion(Info.enemypath[0][0] - 30, Info.enemypath[0][1] - 30, float(roundInfo[roundLine][1]))
            currIter += 1
            if currIter == int(roundInfo[roundLine][3]):
                currIter = 0
                nextTime = Info.acTime + float(roundInfo[roundLine][4]) * 1000
                roundLine += 1
            else:
                nextTime = Info.acTime + float(roundInfo[roundLine][2]) * 1000
        elif playing and len(Info.enemies) == 0 and len(Info.particles) == 0:
            playing = False
            nextTime = Info.acTime
            roundLine += 1
            Info.rounds += 1
            startPause = Info.acTime
            startLine = roundLine


        if time - manaTimer > 3000:
            for i in Info.champions:
                if i.mana < i.maxmana:
                    i.mana += 1
            manaTimer = time
        for i in Info.champions:
            if i.tick(mousePos, click) == 2:
                deselect = False
            if i.target is not None and time - Info.atkTimers[i] > i.atkspd * 1000:
                i.fire()
                Info.atkTimers[i] = time
            for j in i.projects:
                j.tick()
        for i in Info.enemies:
            if time - Info.atkTimers[i] > i.atkspd * 1000:
                Info.atkTimers[i] = time
                if (i.slow[0] > 0 or i.slow[1] < Info.acTime) and i.target is not None:
                    i.fire()
            if i.tick(mousePos, click) == 2:
                deselect = False
        if deselect:
            Info.selected = None
        if Info.summoning is not None:
            Info.selected = Info.summoning
        if Info.selected is None or not isinstance(Info.selected, Champion) or Info.summoning is not None:
            Info.buttDict["sell"] = None
            Info.buttDict["use"] = None
        elif Info.buttDict["sell"] is None:
            Info.buttDict["sell"] = Button(1125, 0, 100, 40, screen,
                                           label=pygame.font.SysFont("Microsoft Yahei UI Light", 30).render("Sell", 1, (255, 255, 255)))
            Info.buttDict["use"] = Button(1075, 0, 200, 40, screen, ability=True)
        for i in Info.enemies:
            i.draw(screen)
        for i in Info.champions:
            if i.target is not None:
                i.target.draw(screen)
        for i in Info.champions:
            i.draw(screen)
            for j in i.projects:
                j.draw(screen)
        for i in Info.particles[:]:
            pygame.draw.circle(screen, i[5], (int(i[0]), int(i[1])), i[4])
            i[0] += i[2]
            i[1] += i[3]
            if i[6] < Info.acTime:
                Info.particles.remove(i)
        for i in Info.poison:
            for j in Info.poison[i][:]:
                j.tick(screen)
        pygame.draw.rect(screen, (0, 0, 255), (0, 550, 1200, 100))
        drew = False
        hovering = None
        summClicked = False
        if playing:
            Info.buttDict["start"] = None
        for i in Info.buttDict:
            if isinstance(Info.buttDict[i], SummButton):
                val = Info.buttDict[i].tick(mousePos, click)
                if val >= 1:
                    sidebar.draw(screen, Info.buttDict[i].champy, hover=True)
                    hovering = Info.buttDict[i].champy
                    Info.buttDict["sell"] = None
                    Info.buttDict["use"] = None
                    drew = True
                    if val == 2:
                        Info.summoning = Info.buttDict[i].Champ(mousePos[0], mousePos[1], summ=True)
                        summClicked = True
        if not drew and Info.summoning is None:
            sidebar.draw(screen, Info.selected)
        elif not drew:
            sidebar.draw(screen, Info.selected, hover=True)
        pygame.draw.rect(screen, (0, 0, 255), (1050, 0, 250, 200))
        beLbl = pygame.font.SysFont("Microsoft Yahei UI Light", 30).render("Blue Essence: " + str(Info.be), 1,(255, 255, 255))
        timeLbl = pygame.font.SysFont("Microsoft Yahei UI Light", 30).render(
            "Time Played: " + str(time // 60000).zfill(2) + ":" + str(time // 1000 % 60).zfill(2), 1,(255, 255, 255))
        roundLbl = pygame.font.SysFont("Microsoft Yahei UI Light", 40).render(
            "Round " + str(Info.rounds), 1, (255, 255, 255))
        screen.blit(beLbl, (1070, 20))
        screen.blit(timeLbl, (1070, 25 + beLbl.get_height()))
        screen.blit(roundLbl, (1070,  30 + beLbl.get_height() + timeLbl.get_height()))
        for i in Info.buttDict:
            if Info.buttDict[i] is not None:
                if Info.buttDict[i].tick(mousePos, click):
                    if i == "use" and Info.selected.mana >= Info.selected.actCost and Info.selected.canUse:
                        Info.selected.actCd = (time, Info.selected.actCd[1])
                        Info.selected.mana -= Info.selected.actCost
                        Info.selected.useAbility()
                    if i == "sell":
                        Info.be += Info.selected.be
                        Info.champions.remove(Info.selected)
                        Info.selected = None
                        Info.buttDict["sell"] = None
                        Info.buttDict["use"] = None
                        break
                    if i == "quit":
                        exit()
                    if i == "start":
                        playing = True
        if not playing:
            pauseTime = pygame.time.get_ticks() - startPause
        if Info.summoning is not None and not summClicked:
            valid = True
            for i in Info.pathareas:
                if i.collidepoint(mousePos):
                    valid = False
            if mousePos[0] > 1050 or mousePos[1] > 550 or valid and Info.summoning.ranged or not (valid or Info.summoning.ranged):
                    Info.summoning.tick(mousePos, click)
                    Info.summoning.draw(screen)
                    if click:
                        if mousePos[0] < 1050 and mousePos[1] < 550:
                            Info.selected = Info.summoning.Champ(Info.summoning.x,
                                                                 Info.summoning.y)
                            Info.be -= Info.summoning.be
                        else:
                            Info.selected = None
                        Info.summoning = None
        if "quit" not in Info.buttDict.keys():
            Info.buttDict["quit"] = Button(1070, 80 + beLbl.get_height() + timeLbl.get_height(), 70, 50, screen,
                                           label=pygame.font.SysFont("Microsoft Yahei UI Light", 30).render("Quit", 1, (255, 255, 255)))
        if "start" not in Info.buttDict.keys() or Info.buttDict["start"] is None and not playing:
            Info.buttDict["start"] = Button(1160, 80 + beLbl.get_height() + timeLbl.get_height(), 130, 50, screen,
                                            label=pygame.font.SysFont("Microsoft Yahei UI Light", 30).render("Start Round", 1, (255, 255, 255)), color=(0, 200, 0))

        pygame.display.update()
        pygame.time.Clock().tick(60)



def pause():
    global mouse
    global mousePos
    global click
    global minSpawnTimer
    global manaTimer
    global time
    global hovering
    while True:
        screen.fill((200, 30, 150))
        screen.blit(img, (0, 0))
        mousePos = pygame.mouse.get_pos()
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        # for i in Info.enemypath:
        #     pygame.draw.rect(screen, (255, 0, 0), (i[0] - 5, i[1] - 5, 10, 10))
        for i in Info.enemies:
            i.draw(screen)
        for i in Info.champions:
            i.draw(screen)
            for j in i.projects:
                j.draw(screen)
        pygame.draw.rect(screen, (0, 0, 255), (0, 550, 1200, 100))
        if Info.summoning is None and hovering is None:
            sidebar.draw(screen, Info.selected)
        else:
            sidebar.draw(screen, hovering, hover=True)
        for i in Info.buttDict:
            if Info.buttDict[i] is not None:
                if Info.buttDict[i].tick(mousePos, click):
                    pass
        pygame.draw.rect(screen, (0, 0, 255), (1050, 0, 250, 200))
        beLbl = pygame.font.SysFont("Microsoft Yahei UI Light", 30).render("Blue Essence: " + str(Info.be), 1,
                                                                           (255, 255, 255))
        timeLbl = pygame.font.SysFont("Microsoft Yahei UI Light", 30).render(
            "Time Played: " + str(time // 60000).zfill(2) + ":" + str(time // 1000 % 60).zfill(2), 1, (255, 255, 255))
        screen.blit(beLbl, (1070, 20))
        screen.blit(timeLbl, (1070, 25 + beLbl.get_height()))
        pygame.draw.rect(screen, (200, 200, 200), (width // 2 - 250, height // 2 - 150, 500, 300))
        pauseLbl = pygame.font.SysFont("Microsoft Yahei UI Light", 50).render("Paused", 1, (255, 255, 255))
        screen.blit(pauseLbl, ((width - pauseLbl.get_width()) // 2, height // 2 - 120))
        pygame.display.update()
        pygame.time.Clock().tick(60)


def exit():
    global time
    Info.playTime = time
    datadic = {}
    datadic["champions"] = []
    for i in Info.champions:
        datadic["champions"].append({"name": i.name.replace(" ", ""), "x": i.x, "y": i.y, "hp": i.hp, "mana": i.mana})
        if i.name == "Nasus":
            datadic["champions"][len(datadic["champions"])-1]["Qbonus"] = i.Qbonus
    datadic["be"] = Info.be
    datadic["playTime"] = Info.playTime
    datadic["rounds"] = Info.rounds
    with open("state.txt", "w") as outfile:
        outfile.seek(0)
        # json.dump(datadic, outfile)
    sys.exit()

play()
