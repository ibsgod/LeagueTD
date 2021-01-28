import random
import sys
import os
import pygame
import json

from Ashe import Ashe
from Button import Button
from Champion import Champion
from Darius import Darius
from Draven import Draven
from Info import Info
from Katarina import Katarina
from Lulu import Lulu
from MasterYi import MasterYi
from Minion import Minion
from Nasus import Nasus
from Nexus import Nexus
from Shaco import Shaco
from Sidebar import Sidebar
from Singed import Singed
from Sona import Sona
from SummButton import SummButton
from Swain import Swain

# initial values for game and setting up game window
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
# variables for processing round data
roundLine = 0
currIter = 0
nextTime = 0
startLine = 0
roundInfo = 0
nexHp = 10
nexus = None
endless = None
placeSound = pygame.mixer.Sound("place.wav")
bg = pygame.image.load("menuscreen.png")
title = pygame.image.load("title.png").convert_alpha()
sb = pygame.image.load("sidebar.png")

# loading game data if it exists
try:
    with open("state.txt") as file:
        data = json.load(file)
except:
    pass

try:
    with open("highscore.txt") as file:
        Info.highscore = int(file.readline())
except:
    pass
# loading rounds data
with open("rounds.txt") as file:
    roundInfo = file.readlines()
    space = lambda x: x.split(' ')
    removeNewLine = lambda x: x.replace('\n', '')
    roundInfo = list(map(removeNewLine, roundInfo))
    roundInfo = list(map(space, roundInfo))
# main menu
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
    global endless
    while True:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        pygame.mixer.music.set_volume(1)
        # initializing objects from custom Button class
        if len(Info.buttDict) == 0:
            Info.buttDict["newGame"] = Button(325, 375, 300, 100, screen,
                                              label=pygame.font.SysFont("Microsoft Yahei UI Light", 50).render(
                                                  "New Game", True,(255, 255, 255)))
            Info.buttDict["loadGame"] = Button(325, 500, 300, 100, screen,
                                               label=pygame.font.SysFont("Microsoft Yahei UI Light", 50).render(
                                                   "Load Game", True,(255, 255, 255)))
            Info.buttDict["endless"] = Button(675, 375, 300, 100, screen,
                                               label=pygame.font.SysFont("Microsoft Yahei UI Light", 50).render(
                                                   "Endless", True,(255, 255, 255)))
            Info.buttDict["quitGame"] = Button(675, 500, 300, 100, screen,
                                               label=pygame.font.SysFont("Microsoft Yahei UI Light", 50).render(
                                                   "Quit", True,(255, 255, 255)))
            if len(data) == 0:
                Info.buttDict["loadGame"].color = (100, 100, 100)
        screen.fill((200, 30, 150))
        screen.blit(bg, (0, 0))
        title.set_alpha(min(int(pygame.time.get_ticks()/10), 255))
        screen.blit(title, ((1300 - title.get_width())/2, 100))
        click = False
        mousePos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        Info.champions.clear()
        # checking for button clicks
        for i in Info.buttDict:
            if Info.buttDict[i].tick(mousePos, click):
                if i == "newGame":
                    endless = False
                    Info.rounds = 1
                    Info.be = 10
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
                    endless = False
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
                if i == "endless":
                    endless = True
                    Info.be = 20
                    Info.acTime = 0
                    play()
                    with open("highscore.txt") as file:
                        Info.highscore = int(file.readline())
                    break
                if i == "quitGame":
                    sys.exit()

        pygame.display.update()
        pygame.time.Clock().tick(60)
# main function for game loop
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
    nexus = Nexus(Info.enemypath[len(Info.enemypath)-1][0] - 100, Info.enemypath[len(Info.enemypath)-1][1] - 60, nexHp)
    Info.enemies.clear()
    Info.particles.clear()
    Info.poison.clear()
    Info.buttDict.clear()
    # creating objects of custom buttons for summoning champs
    Info.buttDict["Ashe"] = SummButton(0, 550, screen, Ashe)
    Info.buttDict["MasterYi"] = SummButton(150, 550, screen, MasterYi)
    Info.buttDict["Sona"] = SummButton(300, 550, screen, Sona)
    Info.buttDict["Lulu"] = SummButton(450, 550, screen, Lulu)
    Info.buttDict["Nasus"] = SummButton(600, 550, screen, Nasus)
    Info.buttDict["Singed"] = SummButton(750, 550, screen, Singed)
    Info.buttDict["Shaco"] = SummButton(900, 550, screen, Shaco)
    Info.selected = None
    Info.summoning = None
    if endless:
        pygame.mixer.music.load("mario.wav")
    else:
        pygame.mixer.music.load("kirby.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    # game loop
    while True:
        screen.fill((200, 30, 150))
        screen.blit(img, (0, 0))
        screen.blit(sb, (1050, 0))
        mousePos = pygame.mouse.get_pos()
        currentTime = pygame.time.get_ticks()
        Info.playing = playing
        # Info.acTime holds the game playtime, EXCLUDING any pauses
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
            # checking for keyboard input
            if event.type == pygame.KEYUP:
                try:
                    if int(pygame.key.name(event.key)) < 8:
                        yes = True
                        # summoning a champ if not already on map, using its ability if it is
                        for i in Info.champions:
                            if i.name == Info.champList[int(pygame.key.name(event.key))-1] and playing and i.mana >= i.actCost and i.canUse and Info.acTime - i.actCd[0] > i.actCd[1] * 1000:
                                i.actCd = (Info.acTime, i.actCd[1])
                                i.mana -= i.actCost
                                i.useAbility()
                                if i.abiSound is not None and i.name != "Nasus":
                                    if i.name == "Singed":
                                        i.abiSound.fadeout(500)
                                        if i.running:
                                            i.abiSound.play()
                                    else:
                                        i.abiSound.play()
                                yes = False
                                break
                        if yes:
                            Info.summoning = eval(Info.champList[int(pygame.key.name(event.key)) - 1].replace(" ", ""))(mousePos[0], mousePos[1], summ=True)
                            has = False
                            for i in Info.champions:
                                if isinstance(i, Info.summoning.Champ):
                                    has = True
                            if has or Info.be < Info.summoning.be:
                                Info.summoning = None
                                Info.selected = None
                            break
                except:
                    pass
                if event.key == pygame.K_m:
                    pygame.mixer.music.pause() if pygame.mixer.music.get_busy() else pygame.mixer.music.unpause()
        deselect = click and mousePos[0] < 1050 and mousePos[1] < 550
        # processing rounds.txt to create enemies for campaign mode
        if not endless:
            if playing and (len(Info.enemies) == 0 or Info.acTime > nextTime) and roundInfo[roundLine][0] != '-':
                if roundInfo[roundLine][0] == "m":
                    Minion(Info.enemypath[0][0] - 30, Info.enemypath[0][1] - 30, float(roundInfo[roundLine][1]))
                if roundInfo[roundLine][0] == "dr":
                    Draven(Info.enemypath[0][0] - 30, Info.enemypath[0][1] - 50, float(roundInfo[roundLine][1]))
                if roundInfo[roundLine][0] == "da":
                    Darius(Info.enemypath[0][0] - 30, Info.enemypath[0][1] - 50, float(roundInfo[roundLine][1]))
                if roundInfo[roundLine][0] == "k":
                    Katarina(Info.enemypath[0][0] - 30, Info.enemypath[0][1] - 50, float(roundInfo[roundLine][1]))
                if roundInfo[roundLine][0] == "s":
                    Swain(Info.enemypath[0][0] - 30, Info.enemypath[0][1] - 50, float(roundInfo[roundLine][1]))
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
        # random enemy generation if endless mode
        else:
            if playing:
                r = random.randint(1, 600 - min(int(Info.acTime/5000), 500))
                if r <= 10 or r <= 20 and Info.acTime < 20000:
                    Minion(Info.enemypath[0][0] - 30, Info.enemypath[0][1] - 30, random.randint(1, 1 + int(Info.acTime/5000)))
                elif r == 11:
                    Draven(Info.enemypath[0][0] - 30, Info.enemypath[0][1] - 50, random.randint(2, 2 + int(Info.acTime/5000)))
                elif r == 12:
                    Darius(Info.enemypath[0][0] - 30, Info.enemypath[0][1] - 50, random.randint(2, 5 + int(Info.acTime/5000)))
                elif r == 13:
                    Katarina(Info.enemypath[0][0] - 30, Info.enemypath[0][1] - 50, random.randint(2, 4 + int(Info.acTime/5000)))
                elif r == 14:
                    Swain(Info.enemypath[0][0] - 30, Info.enemypath[0][1] - 50, random.randint(2, 4 + int(Info.acTime / 5000)))
        # champions gan mana over time
        if manaTimer > Info.acTime:
            manaTimer = Info.acTime
        if Info.acTime - manaTimer > 3000:
            for i in Info.champions:
                if i.name != "Clone" and i.mana < i.maxmana:
                    i.mana += 1
            manaTimer = Info.acTime
        # calling the tick method for champions
        for i in Info.champions:
            if i.name == "Shaco" or i.name == "Clone":
                for j in i.boxes:
                    if j.tick(mousePos, click) == 2:
                        deselect = False
                    if j.target is not None and Info.acTime - Info.atkTimers[j] > j.atkspd * 1000:
                        j.animStart = Info.acTime
                        j.firing = True
                        Info.atkTimers[j] = Info.acTime
                    if j.target is not None and Info.acTime - Info.atkTimers[j] > j.atkspd * 500 and j.firing:
                        j.fire()
                        j.firing = False
                        if j.fireSound is not None:
                            j.fireSound.play()
                    if Info.playing:
                        for k in j.projects:
                            k.tick()
            if i.tick(mousePos, click) == 2:
                deselect = False
            # calling fire() on champions ready to attack
            if i.target is not None and Info.acTime - Info.atkTimers[i] > i.atkspd * 1000 and not (i.name == "Singed" and i.running):
                i.animStart = Info.acTime
                i.firing = True
                Info.atkTimers[i] = Info.acTime
            if i.target is not None and Info.acTime - Info.atkTimers[i] > i.atkspd * 500 and i.firing and not (i.name == "Singed" and i.running):
                i.fire()
                i.firing = False
                if i.fireSound is not None:
                    i.fireSound.play()
            # calling tick() on all projectiles
            if Info.playing:
                for j in i.projects:
                    j.tick()
        if nexus.tick(mousePos, click) == 2:
            deselect = False
        # calling tick() on all enemies
        for i in Info.enemies:
            # checking if enemy is stunned
            if (i.slow[0] > 0 or i.slow[1] < Info.acTime) and i.target is not None:
                if Info.acTime - Info.atkTimers[i] > i.atkspd * 1000:
                    Info.atkTimers[i] = Info.acTime
                    i.animStart = Info.acTime
                    i.firing = True
                if Info.acTime - Info.atkTimers[i] > i.atkspd * 500 and i.firing:
                    i.fire()
                    i.firing = False
                    if i.fireSound is not None:
                        i.fireSound.play()
            for j in i.projects:
                j.tick()
            if i.tick(mousePos, click) == 2:
                deselect = False
        # logic for selecting entities and summoning champs
        if deselect:
            Info.selected = None
        if Info.summoning is not None:
            Info.selected = Info.summoning
        # sidebar only appears when something is selected
        if Info.selected is None or not isinstance(Info.selected, Champion) or Info.selected.name == "Clone" or Info.summoning is not None:
            Info.buttDict["sell"] = None
            Info.buttDict["use"] = None
        elif Info.buttDict["sell"] is None:
            Info.buttDict["sell"] = Button(1125, 0, 100, 40, screen,
                                           label=pygame.font.SysFont("Microsoft Yahei UI Light", 30).render("Sell", True,(255, 255, 255)))
            Info.buttDict["use"] = Button(1075, 0, 200, 40, screen, ability=True)
        # drawing all entities to the screen
        for i in Info.enemies:
            i.draw(screen)
        for i in Info.champions:
            if i.target is not None:
                i.target.draw(screen)
        for i in Info.champions:
            i.draw(screen)
            for j in i.projects:
                j.draw(screen)
            if i.name == "Shaco" or i.name == "Clone":
                for j in i.boxes:
                    j.draw(screen)
                    for k in j.projects:
                        k.draw(screen)
        for i in Info.enemies:
            for j in i.projects:
                j.draw(screen)
        nexus.draw(screen)
        # draw all particles to screen
        for i in Info.particles[:]:
            pygame.draw.circle(screen, i[5], (int(i[0]), int(i[1])), i[4])
            if Info.playing:
                i[0] += i[2]
                i[1] += i[3]
            if i[6] < Info.acTime:
                Info.particles.remove(i)
        for i in Info.poison[:]:
            i.tick(screen)
        # draw the text when enemies are killed
        for i in Info.gaintext[:]:
            surf = pygame.Surface(i[0].get_size()).convert_alpha()
            surf.fill((255, 255, 255, 245))
            i[0].blit(surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(i[0], (i[1], i[2]))
            i[2] -= 1
            if i[3] <= Info.acTime:
                Info.gaintext.remove(i)
        drew = False
        hovering = None
        summClicked = False
        if playing:
            Info.buttDict["start"] = None
        else:
            Info.poison.clear()
        # checking for all summoning button clicks
        for i in Info.buttDict:
            if isinstance(Info.buttDict[i], SummButton):
                val = Info.buttDict[i].tick(mousePos, click)
                if val >= 1:
                    # showing champ info in sidebar if player hovers over champ in summoning bar
                    sidebar.draw(screen, Info.buttDict[i].champy, hover=True)
                    hovering = Info.buttDict[i].champy
                    Info.buttDict["sell"] = None
                    Info.buttDict["use"] = None
                    drew = True
                    if val == 2:
                        # creating champ object when summoning that follows mouse
                        Info.summoning = Info.buttDict[i].Champ(mousePos[0], mousePos[1], summ=True)
                        summClicked = True
        # showing info on sidebar
        if not drew and Info.summoning is None:
            sidebar.draw(screen, Info.selected)
        elif not drew:
            sidebar.draw(screen, Info.selected, hover=True)
        # GUI for top right
        beLbl = pygame.font.SysFont("Microsoft Yahei UI Light", 25).render("Blue Essence: " + str(Info.be), 1,(255, 255, 255))
        timeLbl = pygame.font.SysFont("Microsoft Yahei UI Light", 25).render(
            "Time Played: " + str(Info.acTime // 60000).zfill(2) + ":" + str(Info.acTime // 1000 % 60).zfill(2), 1,(255, 255, 255))
        if not endless:
            roundLbl = pygame.font.SysFont("Microsoft Yahei UI Light", 35).render(
                "Round " + str(Info.rounds) + "/20", True,(255, 255, 255))
        else:
            roundLbl = pygame.font.SysFont("Microsoft Yahei UI Light", 35).render(
                "Endless ", True,(255, 255, 255))
        screen.blit(beLbl, (1080, 30))
        screen.blit(timeLbl, (1080, 35 + beLbl.get_height()))
        screen.blit(roundLbl, (1080, 40 + beLbl.get_height() + timeLbl.get_height()))
        # checking for all non-summoning button clicks
        for i in Info.buttDict:
            if Info.buttDict[i] is not None:
                if Info.buttDict[i].tick(mousePos, click):
                    # using selected champ's ability
                    if i == "use" and playing and Info.selected.mana >= Info.selected.actCost and Info.selected.canUse:
                        Info.selected.actCd = (Info.acTime, Info.selected.actCd[1])
                        Info.selected.mana -= Info.selected.actCost
                        Info.selected.useAbility()
                        if Info.selected.abiSound is not None and Info.selected.name != "Nasus":
                            if Info.selected.name == "Singed":
                                Info.selected.abiSound.fadeout(500)
                                if Info.selected.running:
                                    Info.selected.abiSound.play()
                            else:
                                Info.selected.abiSound.play()
                    # selling selected champ
                    if i == "sell":
                        Info.be += Info.selected.be
                        Info.champions.remove(Info.selected)
                        Info.selected = None
                        Info.buttDict["sell"] = None
                        Info.buttDict["use"] = None
                        for j in Info.champions:
                            j.atkspd = j.oriatkspd
                        break
                    if i == "quit":
                        for i in Info.enemies:
                            if i.name == "Swain":
                                i.swainSound.stop()
                        save()
                        Info.buttDict.clear()
                        return
                    if i == "start":
                        playing = True
                    if i == "pause":
                        playing = not playing
                        if playing:
                            Info.buttDict[i].changeLabel(pygame.font.SysFont("Microsoft Yahei UI Light", 30).render(
                                                "Pause", True,(255, 255, 255)))
                        else:
                            Info.buttDict[i].changeLabel(pygame.font.SysFont("Microsoft Yahei UI Light", 30).render(
                                "Play", True,(255, 255, 255)))
        # creating a champion when a valid spot is chosen to summon
        if Info.summoning is not None and not summClicked:
            valid = False
            if not Info.summoning.ranged:
                for i in Info.pathareas:
                    if i.collidepoint(mousePos[0], mousePos[1] + 30):
                        valid = True
            else:
                for i in Info.towerspots:
                    if i.collidepoint(mousePos[0], mousePos[1] + 30):
                        valid = True
            if mousePos[0] > 1050 or mousePos[1] > 550 or valid:
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
        # if statements make sure that button objects are only created on first iteration of loop to prevent repetitive object creation
        if "quit" not in Info.buttDict.keys():
            Info.buttDict["quit"] = Button(1070, 85 + beLbl.get_height() + timeLbl.get_height(), 70, 50, screen,
                                           label=pygame.font.SysFont("Microsoft Yahei UI Light", 30).render("Quit", True,(255, 255, 255)))
        if not endless:
            if "start" not in Info.buttDict.keys() or Info.buttDict["start"] is None and not playing:
                Info.buttDict["start"] = Button(1160, 85 + beLbl.get_height() + timeLbl.get_height(), 130, 50, screen,
                                            label=pygame.font.SysFont("Microsoft Yahei UI Light", 30).render("Start Round", True,(255, 255, 255)), color=(0, 200, 0))
        elif endless and "pause" not in Info.buttDict.keys() or Info.buttDict["pause"] is None:
            Info.buttDict["pause"] = Button(1160, 85 + beLbl.get_height() + timeLbl.get_height(), 130, 50, screen,
                                            label=pygame.font.SysFont("Microsoft Yahei UI Light", 30).render(
                                                "Start", True,(255, 255, 255)), color=(0, 200, 0))
        # end game if nexus falls
        if nexus.hp <= 0:
            if not endless:
                end(Info.rounds)
            else:
                end(Info.acTime)
            return
        pygame.display.update()
        pygame.time.Clock().tick(60)
# saving game data when quitting
def save():
    if not endless:
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
    else:
        with open("highscore.txt", "w") as file:
            file.write(str(max(Info.highscore, Info.acTime)))
# end screen
def end(round):
    global click
    global mousePos
    global data
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    with open("state.txt", "w") as outfile:
        outfile.truncate(0)
    data = ""
    rotTime = 0
    rotflip = 1
    for i in Info.champions:
        if i.name == "Singed":
            i.abiSound.stop()
    if not endless and round < 20 or endless and Info.acTime <= Info.highscore:
            pygame.mixer.music.load("xeno.wav")
    else:
        pygame.mixer.music.load("pokemon.wav")
        pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
    while True:
        screen.fill((150, 0, 150))
        Info.buttDict.clear()
        Info.buttDict["menu"] = Button((1300 - 400) / 2, 375, 400, 100, screen,
                                          label=pygame.font.SysFont("Microsoft Yahei UI Light", 50).render(
                                              "Menu", True,(255, 255, 255)))
        Info.buttDict["quit"] = Button((1300 - 400) / 2, 500, 400, 100, screen,
                                          label=pygame.font.SysFont("Microsoft Yahei UI Light", 50).render(
                                          "Quit", True,(255, 255, 255)))
        mousePos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
            if event == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    pygame.mixer.music.pause() if pygame.mixer.music.get_busy() else pygame.mixer.music.unpause()
        if pygame.time.get_ticks() - rotTime > 500:
            rotflip *= -1
            rotTime = pygame.time.get_ticks()
        if not endless:
            if round < 20:
                roundLbl = pygame.font.SysFont("Microsoft Yahei UI Light", 50).render("Oof! You lost on round " + str(round), 1, (255, 255, 255))
                screen.blit(roundLbl, (int((1300 - roundLbl.get_width())/2), int((650 - roundLbl.get_height())/3)))
                screen.blit(pygame.transform.rotate(pygame.image.load("pepehands.gif"), 20 * rotflip), (100, 100))
                screen.blit(pygame.transform.rotate(pygame.image.load("pepejuice.gif"), -30 * rotflip), (1000, 400))
                screen.blit(pygame.transform.rotate(pygame.image.load("pepesad.gif"), -30 * rotflip), (700, 30))
                screen.blit(pygame.transform.rotate(pygame.transform.scale(pygame.image.load("sadcat.png"), (184, 173)), 10 * rotflip), (70, 400))
            else:
                roundLbl = pygame.font.SysFont("Microsoft Yahei UI Light", 50).render(
                    "POG! You did it!", True,(255, 255, 255))
                screen.blit(roundLbl, (int((1300 - roundLbl.get_width()) / 2), int((650 - roundLbl.get_height()) / 3)))
                screen.blit(pygame.transform.rotate(pygame.image.load("pogchamp.png"), 20 * rotflip), (5, 100))
                screen.blit(pygame.transform.rotate(pygame.image.load("poggies.png"), -30 * rotflip), (1000, 50))
                screen.blit(pygame.transform.rotate(pygame.transform.scale(pygame.image.load("jojo.png"), (350, 200)), -10 * rotflip), (900, 250))
                screen.blit(pygame.transform.rotate(pygame.transform.scale(pygame.image.load("thumsbup.png"), (184, 173)),
                                                    10 * rotflip), (50, 400))
        else:
            save()
            if Info.acTime > Info.highscore:
                roundLbl = pygame.font.SysFont("Microsoft Yahei UI Light", 50).render(
                    "New highscore! You lasted " + format(Info.acTime/1000, ".1f") + " seconds!", True,(255, 255, 255))
                screen.blit(roundLbl, (int((1300 - roundLbl.get_width()) / 2), int((650 - roundLbl.get_height()) / 3)))
                screen.blit(pygame.transform.rotate(pygame.image.load("pogchamp.png"), 20 * rotflip), (5, 100))
                screen.blit(pygame.transform.rotate(pygame.image.load("poggies.png"), -30 * rotflip), (1000, 50))
                screen.blit(pygame.transform.rotate(pygame.transform.scale(pygame.image.load("jojo.png"), (350, 200)),
                                                    -10 * rotflip), (900, 250))
                screen.blit(
                    pygame.transform.rotate(pygame.transform.scale(pygame.image.load("thumsbup.png"), (184, 173)),
                                            10 * rotflip), (50, 400))
            else:
                roundLbl = pygame.font.SysFont("Microsoft Yahei UI Light", 50).render(
                    "Oof! You lasted " + format(Info.acTime/1000, ".1f") + " seconds!", True,(255, 255, 255))
                screen.blit(roundLbl, (int((1300 - roundLbl.get_width()) / 2), int((650 - roundLbl.get_height()) / 3)))
                screen.blit(pygame.transform.rotate(pygame.image.load("pepehands.gif"), 20 * rotflip), (100, 100))
                screen.blit(pygame.transform.rotate(pygame.image.load("pepejuice.gif"), -30 * rotflip), (1000, 400))
                screen.blit(pygame.transform.rotate(pygame.image.load("pepesad.gif"), -30 * rotflip), (700, 30))
                screen.blit(pygame.transform.rotate(pygame.transform.scale(pygame.image.load("sadcat.png"), (184, 173)),
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