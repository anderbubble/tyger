import pygame
import os
import glob
from pygame.locals import *
from Tyger import *

def titlescreen(screen, RESOLUTION):
    #Get a list of all .zzt files
    games = glob.glob("*.[Zz][Zz][Tt]")
    saves = glob.glob("*.[Ss][Aa][Vv]")
    
    """
    if os.name == "posix": #More like if os.name == "posix": print "YOSPOS Bitch!"
        gamesB = glob.glob("*.ZZT") #LUNIX IS CASE SENSITIVE.
        savesB = glob.glob("*.SAV")
        games = (games+gamesB).sort #Concat. arrays and sort. Problem solved.
        saves = (saves+savesB).sort
    """
    
    #titlescreen = pygame.image.load("gfx/Titleboard.png").convert() #Load the title screen
    title = os.open("Tyger.brd", os.O_RDONLY | os.O_BINARY)
    board = Board(title, 0)
    board.room[board.statcoords[0][0]][board.statcoords[0][1]] = Element("monitor", 32, gray, bgblack, board.statcoords[0])
    screen = pygame.display.set_mode(RESOLUTION) #NOFRAME alt param
    #screen.blit(titlescreen, (0,0))
    drawboard(screen, board)
    pygame.display.update()
    print "# Games/Saves: " + str(len(games)) + "/" + str(len(saves))
    
    mode = "games" #Set games/saves mode for which titles to render
    
    #Make sure there are 5 games in the array, repeating the data otherwise
    x = 0
    while len(games) < 5:
        games.append(games[x])
        x += 1
        
    gamelist = [] #selected images for all games.
    gamelistdesel = [] #deselected images for all games
    
    for y in range(0, len(games)):#For every game in the list...
        tempimg = pygame.Surface((64, 14)) #Create a surface that can contain 8 characters of text
        tempimg.fill(bgdarkblue)
        tempimg2 = pygame.Surface((64, 14)) #Create a surface that can contain 8 characters of text
        tempimg2.fill(bgdarkblue)
        for x in range(0, len(games[y])-4): #Then for every character of text in that list... (chopping off the .zzt)
            tempchar = makeimage(int(binascii.hexlify(games[y][x]), 16), blue, bgdarkblue)
            #Char is then produced properly...
            tempimg.blit(tempchar, (x*8,0)) #Loop ends when image is finished
        gamelistdesel.append(tempimg)
        for x in range(0, len(games[y])-4): #Then for every character of text in that list... (chopping off the .zzt)
            tempchar2 = makeimage(int(binascii.hexlify(games[y][x]), 16), cyan, bgdarkblue)
            #Char is then produced properly...
            tempimg2.blit(tempchar2, (x*8,0)) #Loop ends when image is finished
        gamelist.append(tempimg2)
    
    x = 0
    while len(saves) < 5:
        saves.append(saves[x])
        x += 1
        
    savelist = [] #selected images for all games.
    savelistdesel = [] #deselected images for all games
    
    for y in range(0, len(saves)):#For every game in the list...
        tempimg = pygame.Surface((64, 14)) #Create a surface that can contain 8 characters of text
        tempimg.fill(bgdarkblue)
        tempimg2 = pygame.Surface((64, 14)) #Create a surface that can contain 8 characters of text
        tempimg2.fill(bgdarkblue)
        for x in range(0, len(saves[y])-4): #Then for every character of text in that list... (chopping off the .sav)
            tempchar = makeimage(int(binascii.hexlify(saves[y][x]), 16), gray, bgdarkblue)
            #Char is then produced properly...
            tempimg.blit(tempchar, (x*8,0)) #Loop ends when image is finished
        savelistdesel.append(tempimg)
        for x in range(0, len(saves[y])-4): #Then for every character of text in that list... (chopping off the .sav)
            tempchar2 = makeimage(int(binascii.hexlify(saves[y][x]), 16), green, bgdarkblue)
            #Char is then produced properly...
            tempimg2.blit(tempchar2, (x*8,0)) #Loop ends when image is finished
        savelist.append(tempimg2)
        
    #Now we can draw the 5 games to the screen.
    center = 0
    drawgames(center, screen, gamelist, gamelistdesel)
    
    #Now we get input!
    while 1:
        event = pygame.event.wait()
        if event.type == QUIT or event.type == MOUSEBUTTONUP:
            exit()
        if event.type == KEYDOWN:
            if event.key == K_F10:
                exit()
            if event.key == K_UP: #Previous game
                center -= 1
                if (mode == "games" and center < 0):
                    center = len(gamelist)-1
                if (mode == "saves" and center < 0):
                    center = len(savelist)-1
            if event.key == K_DOWN: #Next game
                center += 1
                if (mode == "games" and center >= len(gamelist)) or (mode == "saves" and center >= len(savelist)):
                    center = 0
            if event.key == K_RETURN: #Play game/save
                break
            if event.key == K_r: #Load a save
                mode = "saves"
                center = 0
            if event.key == K_w: #Load a world
                mode = "games"
            if mode == "games":
                drawgames(center, screen, gamelist, gamelistdesel)
            else:
                drawsaves(center, screen, savelist, savelistdesel)
            
    #Play the game selected
    if mode == "games":
        return str(games[center])
    else:
        return str(saves[center])
            
def drawgames(center, screen, gamelist, gamelistdesel):
    
    #Just draw the center game
    screen.blit(gamelist[center], (208,168))
    
    #Games above
    if center-1 < 0:
        screen.blit(gamelistdesel[len(gamelistdesel)-1], (208,154))
        screen.blit(gamelistdesel[len(gamelistdesel)-2], (208,140))
    else:
        screen.blit(gamelistdesel[center-1], (208,154))
        if center-2 < 0:
            screen.blit(gamelistdesel[len(gamelistdesel)-1], (208,140))
        else:
            screen.blit(gamelistdesel[center-2], (208,140))
    
    
    #Games below
    if center+1 >= len(gamelistdesel):
        screen.blit(gamelistdesel[0], (208,182))
        screen.blit(gamelistdesel[1], (208,196))
    else:
        screen.blit(gamelistdesel[center+1], (208,182))
        if center+2 >= len(gamelistdesel):
            screen.blit(gamelistdesel[0], (208,196))
        else:
            screen.blit(gamelistdesel[center+2], (208,196))
            
            
    #THIS TOOK LIKE TWO HOURS MY GOD.
    pygame.display.update()
    
def drawsaves(center, screen, savelist, savelistdesel):
    
    #Just draw the center save
    print "Center is: " + str(center)
    screen.blit(savelist[center], (208,168))
    
    #Saves above
    if center-1 < 0:
        screen.blit(savelistdesel[len(savelistdesel)-1], (208,154))
        screen.blit(savelistdesel[len(savelistdesel)-2], (208,140))
    else:
        screen.blit(savelistdesel[center-1], (208,154))
        if center-2 < 0:
            screen.blit(savelistdesel[len(savelistdesel)-1], (208,140))
        else:
            screen.blit(savelistdesel[center-2], (208,140))
    
    
    #Saves below
    if center+1 >= len(savelistdesel):
        screen.blit(savelistdesel[0], (208,182))
        screen.blit(savelistdesel[1], (208,196))
    else:
        screen.blit(savelistdesel[center+1], (208,182))
        if center+2 >= len(savelistdesel):
            screen.blit(savelistdesel[0], (208,196))
        else:
            screen.blit(savelistdesel[center+2], (208,196))
            
            
    #THIS TOOK LIKE TWO HOURS MY GOD.
    pygame.display.update()