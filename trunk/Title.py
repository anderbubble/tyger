import pygame
import os
import glob
from pygame.locals import *
from Tyger import *

def titlescreen(screen, RESOLUTION, Error=None):
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
    #title = os.open("Tyger.brd", os.O_RDONLY | os.O_BINARY) OLD
    title = open_binary("Tyger.brd")
    board = Board(title, 0)
    board.room[board.statcoords[0][0]][board.statcoords[0][1]] = Element("monitor", 32, gray, bgblack, board.statcoords[0])
    screen = pygame.display.set_mode(RESOLUTION) #NOFRAME alt param
    #screen.blit(titlescreen, (0,0))
    drawboard(screen, board, 0)
    pygame.display.update()
    print "# Games/Saves: " + str(len(games)) + "/" + str(len(saves))
    
    mode = "games" #Set games/saves mode for which titles to render
    
    #Make sure there are 5 games in the array, repeating the data otherwise
    x = 0
    if len(games) > 0:
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
    else:
        mode = "saves"
        if len(saves) > 0:
            Error = "  ####    W    A    R    N    I    N    G\n########\n########            Tyger is currently\n########            unable to find any\n  ####              valid ZZT files!\n\n  ####    Because of this you may only\n  ####    load saves at this time.\n"
            Oop.TextBox(Error, "@Tyger has encountered an error...", screen)
        else:
            Error = "  ####    W    A    R    N    I    N    G\n########\n########            Tyger is currently\n########            unable to find any\n  ####              games or saves!\n\n  ####    Please place any games in your\n  ####    Tyger folder. You can find new\n          ZZT and Tyger worlds at:\n\n$    http://zzt.belsambar.net \n"
            Oop.TextBox(Error, "@Tyger has encountered an error...", screen)
            mode = None
        drawboard(screen, board, tcycles)
        pygame.display.update()
    
    x = 0
    if len(saves) > 0:
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
    if mode != None:
        if mode == "games":
            drawgames(center, screen, gamelist, gamelistdesel, games)
        elif mode == "saves":
            drawgames(center, screen, savelist, savelistdesel, saves)
    
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
            if event.key == K_r and len(saves) > 0: #Load a save
                mode = "saves"
                center = 0
            if event.key == K_w: #Load a world
                mode = "games"
            if mode == "games":
                drawgames(center, screen, gamelist, gamelistdesel, games)
            elif mode == "saves":
                drawsaves(center, screen, savelist, savelistdesel, saves)
            
    #Play the game selected
    if mode == "games":
        return str(games[center])
    elif mode == "saves":
        return str(saves[center])
            
def drawgames(center, screen, gamelist, gamelistdesel, games):
    
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

    #Game name
    tempimg = pygame.Surface((8*42, 14)) #Create a surface for the title
    tempimg.fill(Tyger.bgdarkblue)
    screen.blit(tempimg, (72, 210))
    image, coords = GameName(games, center)
    screen.blit(image, coords)
    
    
    
    #THIS TOOK LIKE TWO HOURS MY GOD.
    pygame.display.update()
    
def drawsaves(center, screen, savelist, savelistdesel, saves):
    
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
            
    #Game Names
    tempimg = pygame.Surface((8*42, 14)) #Create a surface for the title
    tempimg.fill(Tyger.bgdarkblue)
    screen.blit(tempimg, (72, 210))
    image, coords = GameName(saves, center)
    screen.blit(image, coords)
    
    #THIS TOOK LIKE TWO HOURS MY GOD.
    pygame.display.update()
  
def GameName(games, center):
    #Default Games
    GameDict = {"TOWN":("1f", "Town of ZZT"), "CITY":("5e", "Underground City of ZZT"), "CAVES":("08", "The Caves of ZZT"), "DUNGEONS":("1f", "The Dungeons of ZZT"), "DEMO":("5f", "Demo of the ZZT World Editor"), "TOUR":("cf", "Guided Tour of ZZT's Other Worlds"), "PHYSICS":("0a", "The Physics Behind ZZT")}

    #Game Name
    game = open(games[center], "r")
    game.seek(261)
    #game.seek(261)
    #print "ABC", game.read(50)
    color = hex(ord(game.read(1)))[2:]
    if len(color) == 1:
        color = color + "0"
    length = game.read(1)
    if length == "":
        length = 0
    game.read(1)
    name = game.read(ord(length))
    game.close()
    #print color, ord(length), name

    #print "Name", name
    #print "Color", color
    #print "Length", ord(length)
    if (name == "") or (color == "00") or (ord(length)== 0) or (ord(length) > 42):
        #print games[center][:-4]
        if GameDict.has_key(games[center][:-4]):
            color, name = GameDict[games[center][:-4]]
        else:
            tempimg = pygame.Surface((8*42, 14)) #Create a surface for the title
            tempimg.fill(Tyger.bgdarkblue)
            return tempimg, (72, 210)
        
    #print name, int(color), int(length)
    
    tempimg = pygame.Surface((8*len(name), 14)) #Create a surface for the title
    tempimg.fill(Tyger.bgdarkblue)    
    
    for x in range(0, len(name)): #Then for every character of text in that list... (chopping off the .zzt)
        tempchar = Tyger.makeimage(ord(name[x]), Tyger.getFg(color), Tyger.getBg(color)) #Create the character
        tempimg.blit(tempchar, (x*8,0)) #Stamp it onto the surface for the line
    
    #Proper Centering
    coord = 72 + (4*(42-len(name)))
    offset = (42 - len(name)) / 2
    if (offset % 2) != 0:
        coord = coord + 4
    #print offset, "OFFSET"
    
        
    return tempimg, (coord, 210)