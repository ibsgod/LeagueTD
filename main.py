import sys
import os
import pygame
import json

from Ashe import Ashe
from Button import Button
from Champion import Champion
from Draven import Draven
from Info import Info
from Lulu import Lulu
from MasterYi import MasterYi
from Minion import Minion
from Nasus import Nasus
from Nexus import Nexus
from Sidebar import Sidebar
from Singed import Singed
from Sona import Sona
from SummButton import SummButton

pygame.init()
pygame.mixer.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
width = 1300
height = 650
screen = pygame.display.set_mode((width, height))
screen.fill((0, 0, 50))
Info.screen = screen
click = False
mousePos = None
sidebar = Sidebar()
manaTimer = 0
currentTime = 0
hovering = None
playing = False
data = ""
img = pygame.image.load("bg.png")
Info.rounds = 1
roundLine = 0
currIter = 0
nextTime = 0
startLine = 0
roundInfo = 0
nexHp = 1
nexus = None
placeSound = pygame.mixer.Sound("place.wav")


try:
    with open("state.txt") as file:
        data = json.load(file)
except:
    pass


with open("rounds.txt") as file:
    roundInfo = file.readlines()
    space = lambda x: x.split(' ')
    removeNewLine = lambda x: x.replace('\n', '')
    roundInfo = list(map(removeNewLine, roundInfo))
    roundInfo = list(map(space, roundInfo))

def menu():
    global click
    global mousePos
    global roundInfo
    global roundLine
    global currIter
    global nextTime
    global startLine
    global data
    global menuTime
    global startmenuTime
    global nexHp
    while True:
        if len(Info.buttDict) == 0:
            Info.buttDict["newGame"] = Button((1300 - 400) / 2, 375, 400, 100, screen,
                                              label=pygame.font.SysFont("Microsoft Yahei UI Light", 50).render(
                                                  "New Game", 1, (255, 255, 255)))
            Info.buttDict["loadGame"] = Button((1300 - 400) / 2, 500, 400, 100, screen,
                                               label=pygame.font.SysFont("Microsoft Yahei UI Light", 50).render(
                                                   "Load Game", 1, (255, 255, 255)))
            if len(data) == 0:
                Info.buttDict["loadGame"].color = (100, 100, 100)
        screen.fill((200, 30, 150))

        click = False
        mousePos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        Info.champions.clear()

        for i in Info.buttDict:
            if Info.buttDict[i].tick(mousePos, click):
                if i == "newGame":
                    Info.rounds = 1
                    Info.be = 1000
                    Info.acTime = 0
                    roundLine = 0
                    currIter = 0
                    nextTime = 0
                    startLine = 0
                    play()
                    try:
                        with open("state.txt") as file:
                            data = json.load(file)
                    except:
                        pass
                    break
                if i == "loadGame" and len(data) > 0:
                    if len(data) > 0:
                        Info.be = data["be"]
                        Info.acTime = data["acTime"]
                        Info.rounds = data["rounds"]
                        startLine = data["startLine"]
                        roundLine = data["startLine"]
                        nexHp = data["nexHp"]
                        for i in data["champions"]:
                            c = eval(i["name"])(i["x"], i["y"], hp=i["hp"], mana=i["mana"])
                            if i["name"] == "Nasus":
                                c.Qbonus = i["Qbonus"]
                    play()
                    try:
                        with open("state.txt") as file:
                            data = json.load(file)
                    except:
                        pass
                    break

        pygame.display.update()
        pygame.time.Clock().tick(60)

def play():
    global mousePos
    global click
    global manaTimer
    global hovering
    global playing
    global currIter
    global nextTime
    global roundLine
    global startLine
    global currentTime
    global nexus
    sidebar = Sidebar()
    manaTimer = 0
    currentTime = 0
    startTime = 0
    hovering = None
    playing = False
    nexus = Nexus(Info.enemypath[len(Info.enemypath)-1][0] - 35, Info.enemypath[len(Info.enemypath)-1][1] - 35, nexHp)
    Info.enemies.clear()
    Info.particles.clear()
    Info.poison.clear()
    Info.buttDict.clear()
    Info.buttDict["Ashe"] = SummButton(0, 550, screen, Ashe, img="asheicon.png")
    Info.buttDict["MasterYi"] = SummButton(150, 550, screen, MasterYi)
    Info.buttDict["Sona"] = SummButton(300, 550, screen, Sona)
    Info.buttDict["Lulu"] = SummButton(450, 550, screen, Lulu)
    Info.buttDict["Nasus"] = SummButton(600, 550, screen, Nasus)
    Info.buttDict["Singed"] = SummButton(750, 550, screen, Singed)
    Info.selected = None
    Info.summoning = None

    while True:
        screen.fill((200, 30, 150))
        screen.blit(img, (0, 0))
        mousePos = pygame.mouse.get_pos()
        currentTime = pygame.time.get_ticks()
        Info.playing = playing
        if playing:
            Info.acTime += pygame.time.get_ticks() - startTime
        startTime = currentTime
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        deselect = click and mousePos[0] < 1050 and mousePos[1] < 550
        if playing and (len(Info.enemies) == 0 or Info.acTime > nextTime) and roundInfo[roundLine][0] != '-':
            if roundInfo[roundLine][0] == "m":
                Minion(Info.enemypath[0][0] - 30, Info.enemypath[0][1] - 30, float(roundInfo[roundLine][1]))
            if roundInfo[roundLine][0] == "d":
                Draven(Info.enemypath[0][0] - 30, Info.enemypath[0][1] - 50, float(roundInfo[roundLine][1]))
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
            startLine = roundLine
        if manaTimer > Info.acTime:
            manaTimer = Info.acTime
        if Info.acTime - manaTimer > 3000:
            for i in Info.champions:
                if i.mana < i.maxmana:
                    i.mana += 1
            manaTimer = Info.acTime
        for i in Info.champions:
            if i.tick(mousePos, click) == 2:
                deselect = False
            if i.target is not None and Info.acTime - Info.atkTimers[i] > i.atkspd * 1000 and not (i.name == "Singed" and i.running):
                i.fire()
                Info.atkTimers[i] = Info.acTime
                if i.fireSound is not None:
                    i.fireSound.play()
            for j in i.projects:
                j.tick()
        if nexus.tick(mousePos, click) == 2:
            deselect = False
        for i in Info.enemies:
            if Info.acTime - Info.atkTimers[i] > i.atkspd * 1000:
                Info.atkTimers[i] = Info.acTime
                if (i.slow[0] > 0 or i.slow[1] < Info.acTime) and i.target is not None:
                    i.fire()
            for j in i.projects:
                j.tick()
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
        for i in Info.enemies:
            for j in i.projects:
                j.draw(screen)
        nexus.draw(screen)
        for i in Info.particles[:]:
            pygame.draw.circle(screen, i[5], (int(i[0]), int(i[1])), i[4])
            i[0] += i[2]
            i[1] += i[3]
            if i[6] < Info.acTime:
                Info.particles.remove(i)
        for i in Info.poison[:]:
            i.tick(screen)
        pygame.draw.rect(screen, (0, 0, 255), (0, 550, 1200, 100))
        drew = False
        hovering = None
        summClicked = False
        if playing:
            Info.buttDict["start"] = None
        else:
            Info.poison.clear()
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
            "Time Played: " + str(Info.acTime // 60000).zfill(2) + ":" + str(Info.acTime // 1000 % 60).zfill(2), 1,(255, 255, 255))
        roundLbl = pygame.font.SysFont("Microsoft Yahei UI Light", 40).render(
            "Round " + str(Info.rounds), 1, (255, 255, 255))
        screen.blit(beLbl, (1070, 20))
        screen.blit(timeLbl, (1070, 25 + beLbl.get_height()))
        screen.blit(roundLbl, (1070,  30 + beLbl.get_height() + timeLbl.get_height()))
        for i in Info.buttDict:
            if Info.buttDict[i] is not None:
                if Info.buttDict[i].tick(mousePos, click):
                    if i == "use" and playing and Info.selected.mana >= Info.selected.actCost and Info.selected.canUse:
                        Info.selected.actCd = (Info.acTime, Info.selected.actCd[1])
                        Info.selected.mana -= Info.selected.actCost
                        Info.selected.useAbility()
                        if Info.selected.abiSound is not None and Info.selected.name != "Nasus":
                            Info.selected.abiSound.play()
                    if i == "sell":
                        Info.be += Info.selected.be
                        Info.champions.remove(Info.selected)
                        Info.selected = None
                        Info.buttDict["sell"] = None
                        Info.buttDict["use"] = None
                        break
                    if i == "quit":
                        save()
                        Info.buttDict.clear()
                        return
                    if i == "start":
                        playing = True
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
                            Info.selected = Info.summoning.Champ(Info.summoning.x,Info.summoning.y)
                            Info.be -= Info.summoning.be
                            placeSound.play()
                        else:
                            Info.selected = None
                        Info.summoning = None
        if "quit" not in Info.buttDict.keys():
            Info.buttDict["quit"] = Button(1070, 80 + beLbl.get_height() + timeLbl.get_height(), 70, 50, screen,
                                           label=pygame.font.SysFont("Microsoft Yahei UI Light", 30).render("Quit", 1, (255, 255, 255)))
        if "start" not in Info.buttDict.keys() or Info.buttDict["start"] is None and not playing:
            Info.buttDict["start"] = Button(1160, 80 + beLbl.get_height() + timeLbl.get_height(), 130, 50, screen,
                                            label=pygame.font.SysFont("Microsoft Yahei UI Light", 30).render("Start Round", 1, (255, 255, 255)), color=(0, 200, 0))
        if nexus.hp <= 0:
            end(Info.rounds)
            return
        pygame.display.update()
        pygame.time.Clock().tick(60)

def save():
    datadic = {}
    datadic["champions"] = []
    for i in Info.champions:
        datadic["champions"].append({"name": i.name.replace(" ", ""), "x": i.x, "y": i.y, "hp": i.hp, "mana": i.mana})
        if i.name == "Nasus":
            datadic["champions"][len(datadic["champions"])-1]["Qbonus"] = i.Qbonus
    datadic["be"] = Info.be
    datadic["acTime"] = Info.acTime
    datadic["rounds"] = Info.rounds
    datadic["startLine"] = startLine
    datadic["nexHp"] = nexHp
    with open("state.txt", "w") as outfile:
        outfile.seek(0)
        json.dump(datadic, outfile)

def end(round):
    global click
    global mousePos
    global data
    with open("state.txt", "w") as outfile:
        outfile.truncate(0)
    data = ""
    rotTime = 0
    rotflip = 1
    while True:
        screen.fill((150, 0, 150))
        Info.buttDict.clear()
        Info.buttDict["menu"] = Button((1300 - 400) / 2, 375, 400, 100, screen,
                                          label=pygame.font.SysFont("Microsoft Yahei UI Light", 50).render(
                                              "Menu", 1, (255, 255, 255)))
        Info.buttDict["quit"] = Button((1300 - 400) / 2, 500, 400, 100, screen,
                                          label=pygame.font.SysFont("Microsoft Yahei UI Light", 50).render(
                                          "Quit", 1, (255, 255, 255)))
        mousePos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        if pygame.time.get_ticks() - rotTime > 500:
            rotflip *= -1
            rotTime = pygame.time.get_ticks()
        if round < 20:
            roundLbl = pygame.font.SysFont("Microsoft Yahei UI Light", 50).render("Oof! You lost on round " + str(round), 1, (255, 255, 255))
            screen.blit(roundLbl, (int((1300 - roundLbl.get_width())/2), int((650 - roundLbl.get_height())/3)))
            screen.blit(pygame.transform.rotate(pygame.image.load("pepehands.gif"), 20 * rotflip), (100, 100))
            screen.blit(pygame.transform.rotate(pygame.image.load("pepejuice.gif"), -30 * rotflip), (1000, 400))
            screen.blit(pygame.transform.rotate(pygame.image.load("pepesad.gif"), -30 * rotflip), (700, 30))
            screen.blit(pygame.transform.rotate(pygame.transform.scale(pygame.image.load("sadcat.png"), (184, 173)), 10 * rotflip), (70, 400))
        else:
            roundLbl = pygame.font.SysFont("Microsoft Yahei UI Light", 50).render(
                "POG! You did it!", 1, (255, 255, 255))
            screen.blit(roundLbl, (int((1300 - roundLbl.get_width()) / 2), int((650 - roundLbl.get_height()) / 3)))
            screen.blit(pygame.transform.rotate(pygame.image.load("pogchamp.png"), 20 * rotflip), (100, 100))
            screen.blit(pygame.transform.rotate(pygame.image.load("poggies.png"), -30 * rotflip), (1000, 400))
            screen.blit(pygame.transform.rotate(pygame.transform.scale(pygame.image.load("jojo.png"), (350, 200)), -30 * rotflip), (900, 30))
            screen.blit(pygame.transform.rotate(pygame.transform.scale(pygame.image.load("thumsbup.png"), (184, 173)),
                                                10 * rotflip), (70, 400))
        for i in Info.buttDict:
            if Info.buttDict[i].tick(mousePos, click):
                if i == "menu":
                    Info.buttDict.clear()
                    return
                if i == "quit":
                    sys.exit()
        pygame.display.update()
        pygame.time.Clock().tick(60)

menu()