#!/usr/bin/python

#HEY IMPORTANT: print str(allboards[0].room[24][59])
#THOSE ARE THE MAX DIMENSIONS FOR 2D ARRAYS THAT ARE ZZT BOARDS YOU IDIOT.
#196 torch cycles per torch?
#75 energizer cycles per energizer?

import pygame
import os
import math
import string
import binascii
import random
from pygame.locals import *
from sys import exit
from sys import argv

#Get the external files related to Tyger
from Dictionaries import *      #Dictionaries
from Hud import *               #HUD and minhud features
from Title import *             #Title screen for world/save selecting
from Elements import *          #Handling of every element
from Gfx import *               #Graphics

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

#------------------------------------------------------------------------------------------------------------
#   Tyger
#------------------------------------------------------------------------------------------------------------

#Check for essential files.
Error = None

#Debug file
logfile = open("Tyger.log", "w")

#Read in settings
options = []
try:
    config  = open("tyger.cfg", "r")
    
    while True:
        setting = config.readline()
        if setting == "":
            break
        options.append(setting.split("=")[1][1:-1])
    
except IOError:
    print "ERROR - File tyger.cfg not found!"
    print "Using default values instead."
    Error = "  ####    W    A    R    N    I    N    G\n########\n########            Tyger is currently\n########            unable to find the\n  ####              file:\n$                       tyger.cfg  \n  ####    Without this file you will be\n  ####    unable to access some settings.\n"
    options.append("min")
    options.append("False")
    options.append("False")
    options.append("False")
    options.append("False")
    options.append("Tyger")
    options.append("Full")

hud = options[0] #Set up the HUD variable
    
print "OPTIONS: ", options
#paldir  = "gfx/" #Set directory for pallete

#paldir  = "gfx/cga/"

#Determine base resolution
if hud != "min":
    res = (640, 350)
else:
    res = (480, 364)

global framerate
framerate = 10 #Maximum frames per second
#framerate = 9.1032548384 #Maximum frames per second
""" Quantum P on ZZT's framerate:
I immediately remembered reading DOS programming tutorials about the PIT timer, because it has a wacky frequency: 1.193182 MHz.
If you divide that by 65536 (2^16), you get 18.2 Hz. 546 cycles/min = 9.1 cycles/sec = half of 18.2 Hz. It's not proof, but it's
enough of a coincidence to convince me.
So i guess ZZT's frame rate ought to be 9.1032548384 frames/sec.
Though I can think of advantages with picking 10 frames/sec (ideal numbers vs. subtle familiarity of speed). 
"""

#Load default graphics
if hud == "min":
    status = pygame.image.load("gfx/minhud.png")
else:
    status = pygame.image.load("gfx/sidebar.png")

digits   = pygame.image.load("gfx/digitsmin.png")     #Digits for HUD
keyimg   = pygame.image.load("gfx/keysmin.png")       #Keys for HUD
darkness = pygame.image.load("gfx/darkness.png")

#Foreground Colors
global blue
blue, green, cyan, red, purple, yellow, white, black, gray, darkblue, darkgreen, darkcyan, darkred, darkpurple, darkyellow, darkgray = InitFG("gfx/")

#Background colors
bgblue, bggreen, bgcyan, bgred, bgpurple, bgyellow, bgwhite, bgblack, bggray, bgdarkblue, bgdarkgreen, bgdarkcyan, bgdarkred, bgdarkpurple, bgdarkyellow, bgdarkgray = InitBG("gfx/")

#Setup the game clock
clock = pygame.time.Clock()
time_passed = clock.tick(60)

#globals
allboards = []
world = None

#Command line game launching
cmdline = []
for arg in argv[1:]:
    cmdline.append(arg)
print cmdline
if len(cmdline) == 0:
    cmdline = ["none"]

def main():
    RESOLUTION = res
    FSCREEN = False
    
    #pygame.init()
    pygame.display.set_caption("Tyger")
    icon = pygame.image.load("gfx/tyger.png")
    pygame.display.set_icon(icon)
    screen = pygame.display.set_mode(RESOLUTION) #NOFRAME alt param
    
    #Force an error for debugging...
    #Error = "  ####    W    A    R    N    I    N    G\n########\n########            Tyger is currently\n########            unable to find the\n  ####              file:\n$                       tyger.cfg  \n  ####    Without this file you will be\n  ####    unable to access some settings.\n"
    #Error = "  ####    W    A    R    N    I    N    G\n########\n########            Tyger is currently\n########            unable to find any\n  ####              valid ZZT files!\n\n  ####    Because of this you may only\n  ####    load saves at this time.\n"
    #Error = "  ####    W    A    R    N    I    N    G\n########\n########            Tyger is currently\n########            unable to find any\n  ####              games or saves!\n\n  ####    Please place any games in your\n  ####    Tyger folder. You can find new\n          ZZT and Tyger worlds at:\n\n$    http://zzt.belsambar.net \n"
    
    
    #Check for any errors
    if Error != None:
        Oop.TextBox(Error, "@Tyger has encountered an error...", screen)
    
    #Do the whole title screen thing for Tyger
    if cmdline[len(cmdline[0])-4:] == ".sav" or cmdline[0][len(cmdline[0])-4:] == ".zzt":
        zztfile = cmdline[0]
    else:
        zztfile = titlescreen(screen, RESOLUTION, Error)

    #Start a new game
    #world, board, currentboard, allboards, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed = NewGame(zztfile, screen, RESOLUTION, FSCREEN, hud)
    world, board, currentboard, allboards, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, blue, green, cyan, red, purple, yellow, white, black, gray, darkblue, darkgreen, darkcyan, darkred, darkpurple, darkyellow, darkgray, bgblue, bggreen, bgcyan, bgred, bgpurple, bgyellow, bgwhite, bgblack, bggray, bgdarkblue, bgdarkgreen, bgdarkcyan, bgdarkred, bgdarkpurple, bgdarkyellow, bgdarkgray = NewGame(zztfile, screen, RESOLUTION, FSCREEN, hud)
    #return world, board, currentboard, allboards, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, blue, green, cyan, red, purple, yellow, white, black, gray, darkblue, darkgreen, darkcyan, darkred, darkpurple, darkyellow, darkgray, bgblue, bggreen, bgcyan, bgred, bgpurple, bgyellow, bgwhite, bgblack, bggray, bgdarkblue, bgdarkgreen, bgdarkcyan, bgdarkred, bgdarkpurple, bgdarkyellow, bgdarkgray
    #Double the resolution if running in 2x mode
    if options[2] == "True":
        if hud != "min":
            RESOLUTION = (640*((options[2]=="True") +1), 350*((options[2]=="True") +1))
        else:
            RESOLUTION = (480*((options[2]=="True") +1), 364*((options[2]=="True") +1))
        screen = pygame.display.set_mode(RESOLUTION)
    
    #MAIN GAME LOOP
    #pygame.display.set_caption("Tyger - " + zztfile + " - " + world.gamename + " - " + board.title)
    
    #Time and input initial variables
    seconds = 0
    cycles = 0
    input = "null" 

    #Set up quicksave name
    savename = world.gamename
    
    #Screenshots and Screenrecords
    games = glob.glob("screenshots\\" + world.gamename + "*.png")
    scrnum = len(games)  #Screenshot number
    capture = len(glob.glob("record\\" + world.gamename + "*.png"))
    record = False
    
    #MAIN GAME LOOP
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == MOUSEBUTTONUP and event.button == 1):
                exit()
            if event.type == KEYDOWN:
                if event.key == K_F4:                               #Fullscreen toggle
                    FSCREEN = not FSCREEN
                    if FSCREEN:
                        pygame.mouse.set_visible(False)
                        screen = pygame.display.set_mode(RESOLUTION, FULLSCREEN)
                    else:
                        pygame.mouse.set_visible(True)
                        screen = pygame.display.set_mode(RESOLUTION)
                    drawhud(screen, RESOLUTION, FSCREEN, hud, health, ammo, torches, tcycles, ecycles, gems, score, keys, timepassed)
                        
                if event.key == K_KP_PLUS or event.key == K_EQUALS: #Board cycle for debugging
                    currentboard = currentboard + 1
                    if currentboard > world.boards:
                        currentboard = 0
                    imageUnload(board)
                    board = allboards[currentboard]
                    print str(board)
                if event.key == K_KP_MINUS or event.key == K_MINUS: #Board cycle for debugging
                    currentboard = currentboard - 1
                    if currentboard < 0:
                        currentboard = world.boards
                    imageUnload(board)
                    board = allboards[currentboard]
                    print str(board)
                if event.key == K_F3: #Save and continue
                    savename = Tyger.TypedInput("$Saved Game Name: \n!;\n", "@Saving...", screen)
                    savename = savename.lower()
                    SaveGame(savename, allboards, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, board, world)
                if event.key == K_F5: #Take screenshot
                    screenshot = "screenshots/" + world.gamename + "-" + str(scrnum) + ".png"
                    pygame.image.save(screen, screenshot)
                    scrnum = scrnum + 1
                    Dprint("\nSaved screenshot as " + screenshot)
                if event.key == K_F11: #Save and quit.
                    SaveGame(savename, allboards, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, board, world)
                    print "Game saved..."
                    #exit()
                if event.key == K_F10: #Ragequit to world selection.
                    if hud != "min":
                        RESOLUTION = (640, 350)
                    else:
                        RESOLUTION = (480, 364)
                    screen = pygame.display.set_mode(RESOLUTION)
                    zztfile = titlescreen(screen, RESOLUTION)
                    world, board, currentboard, allboards, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, blue, green, cyan, red, purple, yellow, white, black, gray, darkblue, darkgreen, darkcyan, darkred, darkpurple, darkyellow, darkgray, bgblue, bggreen, bgcyan, bgred, bgpurple, bgyellow, bgwhite, bgblack, bggray, bgdarkblue, bgdarkgreen, bgdarkcyan, bgdarkred, bgdarkpurple, bgdarkyellow, bgdarkgray = NewGame(zztfile, screen, RESOLUTION, FSCREEN, hud)
                    #world, board, currentboard, allboards, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed = NewGame(zztfile, screen, RESOLUTION, FSCREEN, hud)
                    if options[2] == "True":
                        if hud != "min":
                            RESOLUTION = (640*((options[2]=="True") +1), 350*((options[2]=="True") +1))
                        else:
                            RESOLUTION = (480*((options[2]=="True") +1), 364*((options[2]=="True") +1))
                    screen = pygame.display.set_mode(RESOLUTION)
                    pygame.display.set_caption("Tyger")
                    seconds, cycles = 0, 0
                    input = "null" 
                    continue
                #27 3N 4S 5E 6W
                
                #Read keys
                if event.key == K_RIGHT or pygame.key.get_pressed()[275]:
                    input = "right"
                    if pygame.key.get_pressed()[303] or pygame.key.get_pressed()[304]:
                        input = "shootright"
                elif event.key == K_LEFT or pygame.key.get_pressed()[276]:
                    input = "left"
                    if pygame.key.get_pressed()[303] or pygame.key.get_pressed()[304]:
                        input = "shootleft"
                elif event.key == K_UP or pygame.key.get_pressed()[273]:
                    input = "up"
                    if pygame.key.get_pressed()[303] or pygame.key.get_pressed()[304]:
                        input = "shootup"
                elif event.key == K_DOWN or pygame.key.get_pressed()[274]:
                    input = "down"
                    if pygame.key.get_pressed()[303] or pygame.key.get_pressed()[304]:
                        input = "shootdown"
                elif event.key == K_p:
                    input = "p"
                elif event.key == K_SLASH and (pygame.key.get_pressed()[303] or pygame.key.get_pressed()[304]):
                    input = "cheat"
                else:
                    input = "null"
                    
            #Element click mode
            
            if event.type == KEYUP:
                if event.key == K_RIGHT or event.key == K_LEFT or event.key == K_UP or event.key == K_DOWN:
                    input = "null"
            
            if event.type == MOUSEBUTTONUP and event.button == 3:
                getinfo(pygame.mouse.get_pos(), board, screen)
        
        #Timing
        #Death speedup:
        if health < 1 or board.room[board.statcoords[0][0]][board.statcoords[0][1]].name == "RIP":
            Oop.MessageLine("GAME OVER - PRESS ESCAPE", screen, board, priority="High")
            global framerate
            framerate = framerate*10
        time = clock.tick(framerate)
        seconds = seconds + (time/1000.0)
        cycles = cycles + (time/100.0)
        if cycles >= 256:
            cycles = 1
            time = 0
        intcycles = int(cycles)
            
        #Process what each stat element is going to do this cycle
        temp = 0
        while temp < len(board.statcoords):
            if board.statcoords[temp] == "pop":
                temp = temp + 1
                continue
            x,y = board.statcoords[temp] #Get the coordinates of this element
            #print "Stat thing at: " + str(board.room[x][y].name)
            ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board= activate(board, x, y, input, temp, intcycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, world, allboards, screen)
            temp = temp + 1
        #input = "null"
        
        #Erase any stats that no longer exist.
        try:
            while True:
                board.statcoords.remove("pop")
                #print "Popped"
        except ValueError:
            0 #We're clean
        
        #Update the time passed for timed boards
        if (board.timelimit != 0) and (intcycles % 10 == 0):
            timepassed = timepassed + 1
            if timepassed >= board.timelimit:
                health = health - 10
                timepassed = 0
        
        if input == "playgame" or input == "p":
            if input == "playgame":
                imageUnload(board)
                board = allboards[world.startboard]
            input = "null"
        
        drawboard(screen, board)
        drawhud(screen, RESOLUTION, FSCREEN, hud, health, ammo, torches, tcycles, ecycles, gems, score, keys, (board.timelimit - timepassed))
        
        #print str(options[2]) + "---------------------------"
        #print str(screen) + "Pre zoom screen"
        if options[2] == "True": #If we want double screen
            #double = pygame.transform.scale2x(screen)
            double = pygame.transform.scale(screen, (screen.get_width()*2, screen.get_height()*2))
            screen.blit(double, (0,0))
            #print str(screen) + "Post zoom"
        pygame.display.update()
        #screenshot = "screenshots/" + world.gamename + "-" + str(scrnum) + ".png"
        #if input != "null" and record == True:
        if record == True:
            capture = capture + 1
            pygame.image.save(screen, "record/" + world.gamename + " - " + str(capture)+".png")
        #pygame.display.set_caption("Tyger - " + zztfile + " - " + world.gamename + " - " + board.title)
        #pygame.display.set_caption("Time: " + str(time) + " Seconds: " + str(seconds) + "Cycles?: " +str(cycles) + "/" + str(intcycles))
        #print "Time: " + str(time) + " Seconds: " + str(seconds) + "Cycles?: " +str(cycles)
        

class World(object):
    def __str__(self):
        part1 = "Number of boards (0): " + str(self.boards) +"\nAmmo: " + str(self.ammo) + "\nGems: " + str(self.gems) + "\nKeys: " +str(self.keys)
        part2 = "\nHealth: " + str(self.health) + "\nStart #: " + str(self.startboard) + "\nTorches: " + str(self.torches) + "\nT Cycles: "  + str(self.tcycles)
        part3 = "\nE Cycles: " + str(self.ecycles) + "\nScore: " + str(self.score) + "\n" + ("-"*15) + "\nGame name: " + self.gamename + " (" + str(self.gamenamelength) + " characters)"
        part4 = "\nFlag: " + str(self.flag) + "\nTime passed: " + str(self.timepassed) + "\nSave: " + str(self.issave)
        part5 = "\nTyger Game color: " + str(self.gamecolor) + "\nGame Length: " + str(self.gamelength)
        return part1+part2+part3+part4+part5
    
    def __init__(self, file):
        self.boards = read2(file)
        self.ammo = read2(file)
        self.gems = read2(file)
        self.keys = [0, 0, 0, 0, 0, 0, 0, 0]
        for x in range(0,7):
            self.keys[x] = read(file)
        self.health = read2(file)
        self.startboard = read2(file)
        self.torches = read2(file)
        self.tcycles = read2(file)
        self.ecycles = read2(file)
        read2(file) #Blank padding
        self.score = read2(file)
        
        #World Name
        self.gamenamelength = read(file)
        self.gamename = sread(file, 20)
        self.gamename = self.gamename[:self.gamenamelength]
        
        #Flags
        self.flaglength = []
        self.flag = []
        for x in range(0,10):
            self.flaglength.append(read(file))
            temp = sread(file, 20)
            temp = temp[:self.flaglength[x]]
            if temp != "":
                self.flag.append(temp)
            
        #Time
        self.timepassed = read2(file) #This is the time passed for a save on a timed board. this will = 12 when you have 8 seconds left on a 20 second timer
                                        #board time - time remaining = timepassed
        
        #Tyger specific Game Name
        self.gamecolor = read(file) #Game's color for Tyger world selection
        self.gamelength = read(file)
        
        #Save byte
        self.issave = bool(read(file)) #Let's be fancy and use a boolean
 
class Element(object):
    
    def __str__(self):
        part1 = "Name: " + self.name + "\n" + "Char: " + str(self.character) + "\n" + "Fore: " + str(self.foreground) + " " + str(self.foregroundcolor) +"\n" + "Back: " + str(self.background) + " " + str(self.backgroundcolor) + "\n" + "X/Y : " + str(self.coords)
        part2 = "\nX-Step: " + str(self.xstep) + "\nY-Step: " + str(self.ystep) + "\nCycle: " + str(self.cycle) + "\nParams 1-3: " + str(self.param1) + "/" + str(self.param2) + "/" + str(self.param3)
        part3 = "\nFollow/Lead #: " + str(self.follownum) + "/" + str(self.leadnum) + "\nUnder ID+Color: " + str(self.underID) + "/" + str(self.underColor) + "\nCurrent Line: " + str(self.line)
        part4 = "\nOOP-Length: " + str(self.oopLength) + "\n==========ZZT-OOP==========\n"
        return part1+part2+part3+part4+str(self.oop)
        #return self.name
    
    def __init__(self, name="empty", character=32, foreground=black, background=bgblack, coords=(0,0)):
        self.name = name
        self.character = character
        self.foreground = foreground
        self.foregroundcolor = gfx2color(foreground)
        self.background = background
        self.backgroundcolor = gfx2bgcolor(background)
        self.coords = coords
        #if name != "object":
        #self.image = makeimage(self.character, self.foreground, self.background)
        
        #Stat data
        self.xstep = 0
        self.ystep = 0
        self.cycle = 3
        
        self.param1 = 0
        self.param2 = 0
        self.param3 = 0
        
        self.follownum = 0
        self.leadnum = 0
        
        self.underID = 0
        self.underColor = 0
        
        self.line = 0
        self.oopLength = 0
        
        self.oop = None
        
        #self.image = makeimage(self.character, self.foreground, self.background)
        self.image = 0

def makeimage(character, foreground, background): #Returns a surface
    if character == 0:
        row = 0
    else:
        row = int(math.ceil(character/16.)-1)
    column = int(character-(16*row))
    
    #Fix for not 100% accurate formula which screws up every 16 chars
    if column == 16:
        column = 0
        row += 1
    #print str("Rendering char: " + str(character) + " from Row/Col: " + str(row) + "/" + str(column))
    
    Coords = Rect(column*8, row*14, 8, 14)
    image = pygame.Surface((8, 14))
    #Apply background
    try:
        image.fill(background)
    except TypeError:
        print str(background)
        background = (100,100,100,100)
        print "ERROR in function makeimage"
        image.fill(background)
    #Apply foreground
    image.blit(foreground, (0,0), Coords)
    #image.blit(foreground, (0,0))
    return image


def read(file):
    """Read one byte as an int"""
    try:
        #temp = int(binascii.hexlify(str(os.read(file, 1))), 16)
        temp = ord(os.read(file, 1))
        return temp
    except ValueError:
        return 0

def read2(file):
    """Read 2 bytes and convert to an integer"""
    try:
        part1 = binascii.hexlify(str(os.read(file, 1)))
        part2 = binascii.hexlify(str(os.read(file, 1)))
        return int(part2 + part1, 16)
    except ValueError:
        return 0

def hread(file):
    """Return a byte of Hex"""
    return binascii.hexlify(str(os.read(file, 1)))

def sread(file, num):
    """Read a string of chracters"""
    array = []
    temp = ""
    for x in range(0,num):
        array.append(binascii.hexlify(str(os.read(file, 1))))
    for x in range(0,num):
        #print str(array[x]) + " ARRAY"
        try:
            temp += chr(int(array[x], 16))
        except ValueError:
            temp += "X"
    #print "Temp sread: " + temp
    return temp

def printarray(array):
    for x in xrange(0,len(array)):
        Dprint(str(array[x]))
    return

class Board(object):
    def __str__(self):
        part0 = "="*50 + " " + self.title + " " + "="*50
        part1 = "\nRoom size: " + str(self.size) + "\nTitle: " + self.title + " " + str(self.number)
        part2 = "\n# of Shots:" + str(self.shots) + "\nDark: " + str(self.dark) + "\nBoards NSWE: " + str(self.boardnorth) + " " + str(self.boardsouth) + " " + str(self.boardwest) + " " + str(self.boardeast)
        part3 = "\nEnter when Zapped?: " + str(self.zap) + "\nMessage + Length: " + self.msg + " (" + str(self.msglength) + ") "
        part4 = "\nEnter X/Y: " + str(self.enterX) + "/" + str(self.enterY)
        part5 = "\nTime Limit: " + str(self.timelimit)
        
        stat0 = "\n" + ("_"*20)
        stat1 = "\nStat Elements: " + str(self.statobjs)
        
        return (part0 + part1 + part2 + part3 + part4 + part5) + stat0 + stat1 + "\nPlayer bullets: " + str(self.playerbullets)
    
    def __init__(self, file, start, number=0):
        #file.seek(start)
        os.lseek(file, start, 0)
        self.size = read2(file)
        
        #Store number
        self.number = number
        
        #Create an empty array for the room, under layer, and drawing rules
        self.room = []
        self.roomunder = []
        self.render = []
        for x in xrange(0,25):
            self.room.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
            self.roomunder.append([Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element(),Element()])
            self.render.append([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
        #printarray(self.room)
        
        #Get the board title -        A title's maximum length is different depending on what your source is:
        self.titlelength = read(file)#ZZT's editor and ZZTAE use 34 characters, Kev-edit uses 42, Nano's ZZT file format says 33 then padding
        self.title = sread(file, 50) #if you use all the padding you get 50 possible characters so that's what I went with. This displays in ZZT's editor fine.
        self.title = self.title[:self.titlelength]
        
        #Now the fun starts
        done = False
        row = 0 #This is where we are located on the board
        col = 0 #at this moment.
        #element = 0
        while not done:
            number = read(file)     #There are this Many... || This is being stored as zero?!?!?!
            #Debug
            if number == 0:
                number = 1
            thing = read(file)      #of this Element...
            #print str(thing) + " is the thing."
            color = str(hread(file))      #in this Color...

            #And placed inside the correct spot of the array
            #print "Inserting into array... " + str(number)
            for x in range(0,number):
                if col >= 60:
                    col = 0
                    row += 1
                    if row >= 25:
                        done = True
                if done:
                    break
                #The element is created in basic form
                if thing < 47 or thing > 53: #If we're not dealing with text
                    element = Element(getElementName(thing), getElementChar(thing), getFg(color), getBg(color), (1,1))
                #print "HELLO" + str(element)
                else: #We are dealing with text
                    junk = str(int(thing)-46) + "0"
                #print junk + " is color"
                    if junk == "70": #in case of white text
                        junk = "00"
                    element = Element(getElementName(thing), int(color, 16), white, getBg(junk), (1,1))
                element.coords = (row, col)
                #print str(row) + " " + str([col]) + "= Current row/column"
                self.room[row][col] = element
                col += 1
            element = 0
        #Ok now we get some board details.
        #Move the file cursor back 3 spaces for some reason?
        os.lseek(file, -3, 1)
        
        self.shots = read(file) #Number of shots
        self.playerbullets = 0 #Bullets on the screen belonging to the player
        self.dark = read(file) #Board is dark?
        
        self.boardnorth = read(file) #Board # to north (hey that's odd you can't have a board edge go to the title screen)
        self.boardsouth = read(file) #Oh that's because it uses 0 for no board connected which is where the title screen is
        self.boardwest = read(file)
        self.boardeast = read(file)
        
        self.zap = read(file) #Restart when zapped?
        
        #Message to be displayed below (for saves really)
        self.msglength = read(file)
        self.msg = sread(file, 58) #48 characters for a message max
        self.msg = self.msg[:self.msglength]
        
        self.enterX = read(file) #Enter X/Y coords for re-enter when zapped
        self.enterY = read(file)
        
        self.timelimit = read2(file) #Time limit for the board
        
        #16 bytes of padding
        self.padding = sread(file, 16)
        
        #Read in Stats
        self.statobjs = read2(file) #Number of elements with stats on board
        self.statcoords = [] #Array containing the coordinates of all stat elementson the board.
        #Dprint("PADDING " + str(self.padding) + " AND " + str(self.statobjs))
        
        #print "STATS FOR " + self.title
        for _ in range(0,self.statobjs+1): #Assign stats to every element
            x = read(file)
            y = read(file) #Get the element's coordinates
            #print "Element's X/Y: " + str(x) + "/" + str(y)
            if x > 60 or y > 25:
                Dprint("ERROR. Stat not on board.")
                print x, y, self.title
                continue
                            #self.room[x][y] is an element
            self.statcoords.append((y-1,x-1)) #Add a tuple with the element's coords for future reference
            self.room[y-1][x-1].xstep = read2(file)
            self.room[y-1][x-1].ystep = read2(file)
            self.room[y-1][x-1].cycle = read2(file)
            self.room[y-1][x-1].param1 = read(file)
            self.room[y-1][x-1].param2 = read(file)
            self.room[y-1][x-1].param3 = read(file)
            self.room[y-1][x-1].follownum = read2(file)
            self.room[y-1][x-1].leadnum = read2(file)
            
            self.room[y-1][x-1].underID = read(file)
            self.room[y-1][x-1].underColor = read(file)
            #print "AN UNDERCOLOR", self.room[y-1][x-1].underColor
            #self.roomunder[y-1][x-1].foreground = getFg(str(self.room[y-1][x-1].underColor))
            #self.roomunder[y-1][x-1].background = getBg(str(self.room[y-1][x-1].underColor))
            
            #If it's a player bullet make sure we increase it so we can compare to the limit
            if self.room[y-1][x-1].param1 == 0 and self.room[y-1][x-1].name == "bullet":
                self.playerbullets = self.playerbullets + 1
            
            #Apply colors below
            self.roomunder[y-1][x-1] = Spawn(IdDict[self.room[y-1][x-1].underID], CharDict[self.room[y-1][x-1].underID], getFg(str(self.room[y-1][x-1].underColor)), getBg(str(self.room[y-1][x-1].underColor)), (y,x), 0, 0, 3, 0, 0, 0)
            #self.roomunder[y-1][x-1].underColor = self.room[y-1][x-1].underColor
            #print self.roomunder[y-1][x-1].underColor, "UNDERCOLOR!"
            
            sread(file, 4) #Pointer. No use for us here.
            
            self.room[y-1][x-1].line = read2(file) #Current line # of code to be executing.
            self.room[y-1][x-1].oopLength = read2(file) #Length of ZZT-OOP
            #print self.room[y-1][x-1].oopLength, "IS THE OOP LENGTH"
            if self.room[y-1][x-1].oopLength > 32767:
                print "Object is bound to something"
                self.room[y-1][x-1].oopLength = 0
            
            sread(file, 8) #8 bytes of padding. God Tim a 5.25" flopppy can only hold so much! Stop wasting space!
            #print "X/Y at the end here are: " + str(x) + "/" + str(y)
            #print str(self.room[y-1][x-1])
            tempOop = OopToArray(file, self.room[y-1][x-1].oopLength)
            #print str(x) + " " + str(y)
            #print len(self.room)
            #print len(self.room[0])
            if tempOop != "NO CODE":
                self.room[y-1][x-1].oop = tempOop
        return
    
def getElementName(id):
    try:
        return IdDict[id]
    except KeyError: #If the element doesn't exist we're going to make it a breakable wall with a ? char
        return "breakable"

def getElementChar(id):
    try:
        return CharDict[id] 
    except KeyError: #As above, make it a ? char
        return 63

def getFg(color):
    #print "COLOR:" + str(color)
    #if len(color) > 2:#Happens only with text
    #    return white
    #print str(color) + " IS THE COLOR"
    try:
        color[1]
    except IndexError:
        #Dprint("ERROR - COLOR DOESN'T EXIST USING BRIGHT RED INSTEAD")
        return red
    
    if color[1] == "9":
        return blue
    elif color[1] == "a":
        return green
    elif color[1] == "b":
        return cyan
    elif color[1] == "c":
        return red
    elif color[1] == "d":
        return purple
    elif color[1] == "e":
        return yellow
    elif color[1] == "f":
        return white
    elif color[1] == "0":
        return black
    elif color[1] == "1":
        return darkblue
    elif color[1] == "2":
        return darkgreen
    elif color[1] == "3":
        return darkcyan
    elif color[1] == "4":
        return darkred
    elif color[1] == "5":
        return darkpurple
    elif color[1] == "6":
        return darkyellow
    elif color[1] == "7":
        return gray
    elif color[1] == "8":
        return darkgray
    else:
        Dprint("ERROR - COLOR DOESN'T EXIST USING BRIGHT RED INSTEAD")
        return red

def getBg(color):
    try:
        color[1]
    except IndexError:
        #Dprint("ERROR - COLOR DOESN'T EXIST USING DARK RED INSTEAD")
        return bgdarkred
    
    if color[0] == "9":
        return bgblue
    elif color[0] == "a":
        return bggreen
    elif color[0] == "b":
        return bgcyan
    elif color[0] == "c":
        return bgred
    elif color[0] == "d":
        return bgpurple
    elif color[0] == "e":
        return bgyellow
    elif color[0] == "f":
        return bgwhite
    elif color[0] == "0":
        return bgblack
    elif color[0] == "1":
        return bgdarkblue
    elif color[0] == "2":
        return bgdarkgreen
    elif color[0] == "3":
        return bgdarkcyan
    elif color[0] == "4":
        return bgdarkred
    elif color[0] == "5":
        return bgdarkpurple
    elif color[0] == "6":
        return bgdarkyellow
    elif color[0] == "7":
        return bggray
    elif color[0] == "8":
        return bgdarkgray
    else:
        Dprint("ERROR - COLOR DOESN'T EXIST USING DARK RED INSTEAD")
        return bgdarkred
    

    

def gfx2color(foreground):
    if foreground == blue:
        return "blue"
    if foreground == green:
        return "green"
    if foreground == cyan:
        return "cyan"
    if foreground == red:
        return "red"
    if foreground == yellow:
        return "yellow"
    if foreground == purple:
        return "purple"
    if foreground == white:
        return "white"
    if foreground == black:
        return "black"
    if foreground == darkblue:
        return "darkblue"
    if foreground == darkgreen:
        return "darkgreen"
    if foreground == darkcyan:
        return "darkcyan"
    if foreground == darkred:
        return "darkred"
    if foreground == darkyellow:
        return "darkyellow"
    if foreground == darkpurple:
        return "darkpurple"
    if foreground == gray:
        return "gray"
    if foreground == darkgray:
        return "darkgray"    
    
    
    


def gfx2bgcolor(background):
    if background == bgblue:
        return "blue"
    if background == bggreen:
        return "green"
    if background == bgcyan:
        return "cyan"
    if background == bgred:
        return "red"
    if background == bgyellow:
        return "yellow"
    if background == bgpurple:
        return "purple"
    if background == bgwhite:
        return "white"
    if background == bgblack:
        return "black"
    if background == bgdarkblue:
        return "darkblue"
    if background == bgdarkgreen:
        return "darkgreen"
    if background == bgdarkcyan:
        return "darkcyan"
    if background == bgdarkred:
        return "darkred"
    if background == bgdarkyellow:
        return "darkyellow"
    if background == bgdarkpurple:
        return "darkpurple"
    if background == bggray:
        return "gray"
    if background == bgdarkgray:
        return "darkgray"
    "BAD BG"


def drawboard(screen, board):
    rendered = 0
    for col in xrange(0,25):
        for row in xrange(0,60):
            
            
            #Draw a dark room
            """
            if board.dark != 0 and (board.room[col][row].name != "player" and board.room[col][row].name != "passage" and board.room[col][row].name != "ammo"):
                #Are you in a lit area?
                try:
                    #lighting = LightDict[(abs(board.statcoords[0][0] - col), abs(board.statcoords[0][1] - row))]
                    lighting = LightDict[(abs(board.statcoords[0][0] - col), abs(board.statcoords[0][1] - row))]
                    if lighting == "Dark":
                        board.room[col][row].image = makeimage(176, darkgray, bgblack)
                        screen.blit(board.room[col][row].image, (row*8,col*14))
                        continue
                except KeyError:
                    board.room[col][row].image = makeimage(176, darkgray, bgblack)
                    screen.blit(board.room[col][row].image, (row*8,col*14))
                    continue
            #print "Dark room!"
            """
            #print str(col) + "/" + str(row)
            #if board.room[col][row].name == "object" or ((board.room[col][row].name == "solid" or board.room[col][row].name == "normal" or board.room[col][row].name == "breakable" or board.room[col][row].name == "water" or board.room[col][row].name == "fake") and board.room[col][row].param1 > 0):
            if board.room[col][row].name == "object" and (board.room[col][row].character != board.room[col][row].param1) and (board.render[col][row] != 0):
                board.room[col][row].character = board.room[col][row].param1
                board.room[col][row].image = makeimage(board.room[col][row].param1, board.room[col][row].foreground, board.room[col][row].background)
            elif board.room[col][row].name == "line" and (board.render[col][row] != 0):
                board.room[col][row].image, board.room[col][row].character = linewallrender(board.room, col, row)
            elif board.room[col][row].name == "empty" and (board.render[col][row] != 0):
                board.room[col][row].image = makeimage(board.room[col][row].character, black, bgblack)
            elif board.room[col][row].name == "pusher" and (board.render[col][row] != 0):
                if board.room[col][row].ystep < 0:
                    board.room[col][row].character = 30 #North
                elif board.room[col][row].ystep > 0:
                    board.room[col][row].character = 31 #South
                elif board.room[col][row].xstep < 0:
                    board.room[col][row].character = 17 #East
                elif board.room[col][row].xstep > 0:
                    board.room[col][row].character = 16 #West
                board.room[col][row].image = makeimage(board.room[col][row].character, board.room[col][row].foreground, board.room[col][row].background)
            else:
                if board.render[col][row] != 0:
                    board.room[col][row].image = makeimage(board.room[col][row].character, board.room[col][row].foreground, board.room[col][row].background)
            
            #Actually draw whatever needs to be drawn
            if (board.render[col][row] != 0) or options[6] == "Full":
                screen.blit(board.room[col][row].image, (row*8,col*14))
                if options[6] != "Full": #This if statement will be redundant when everything is ready for partial rendering. The line below will occur always eventually.
                    board.render[col][row] = 0
                rendered = rendered + 1
            
            if board.msg != "":
                #print "WHAT THE"
                #screen.blit(Oop.TextMessage, (232-((8*len(board.msg)/2)),336))
                offset = (round(len(board.msg) / 2.) - 1) * 8 #Calculate offset to center text
                if Oop.TextMessage == None:
                    Oop.MessageLine(board.msg, screen, board, priority="High") #DEBUG MAYBE
                screen.blit(Oop.TextMessage, ((240 - offset),336))
                
        pygame.display.set_caption("Tiles Rendered: " + str(rendered))
            
def OopToArray(file, oopLength):
    #Read the oop to a string IF THERE'S OOP TO READ
    if oopLength == 0:
        return "NO CODE"
    temp = sread(file, oopLength)
    #Dprint("Length: " + str(oopLength))
    #Dprint("TEMP IS " + str(temp))
    #array = temp.rsplit("\r") #I hope \r is carriage return like they say it is!
    array = temp.replace("\r", "\n")
    """ZZT's current instruction is how many characters into the oop not how many lines!"""
    return array

def getinfo(coords, board, screen):
    x, y = coords
    x = int(math.floor(x/8))
    y = int(math.floor(y/14))
    col = y
    row = x
    
    if x > 59 or y > 24:
        message = str(board)
        print str(board)
    #Dprint(str(x) + "," + str(y))
    #Dprint(str(board.room[y][x]))
    else:
        message = str(board.room[y][x])
        
        print message
        #cline = board.room[y][x].oop[board.room[y][x].line:board.room[y][x].line+10]
    Oop.TextBox(message, "-= Tyger Debug Info =-", screen)
    
    #redraw!
    #board.room[y][x].character = board.room[col][row].param1
    #board.room[y][x].image = makeimage(board.room[col][row].param1, board.room[col][row].foreground, board.room[col][row].background)
    #screen.blit(board.room[y][x].image, (row*8,col*14))
    
def linewallrender(room, col, row):
    n,s,e,w = 0,0,0,0
    
    #Check west for another line wall
    if row-1 < 0: #If you're on the border
        w = 1
    elif room[col][row-1].name == "line":
        w = 1
    
    #Check east for another line wall
    if row+1 >= 60: #If you're on the border
        e = 1
    elif room[col][row+1].name == "line":
        e = 1
        
    #Check south for another line wall
    if col+1 >= 25: #If you're on the border
        s = 1
    elif room[col+1][row].name == "line":
        s = 1
        
    #Check north for another line wall
    if col-1 < 0: #If you're on the border
        n = 1
    elif room[col-1][row].name == "line":
        n = 1
        
    return makeimage(LineDict[(n,s,e,w)], room[col][row].foreground, room[col][row].background), LineDict[(n,s,e,w)]

def customdata(custom):
    custom = "gfx\\" + custom.lower() + "\\"
    
    global blue
    global green
    global cyan
    global red
    global purple
    global yellow
    global white
    global black
    global gray
    global darkblue
    global darkgreen
    global darkcyan
    global darkred
    global darkpurple
    global darkyellow
    global darkgray

    global bgblue
    global bggreen
    global bgcyan
    global bgred
    global bgpurple
    global bgyellow
    global bgwhite
    global bgblack
    global bggray
    global bgdarkblue
    global bgdarkgreen
    global bgdarkcyan
    global bgdarkred
    global bgdarkpurple
    global bgdarkyellow
    global bgdarkgray
    
    #print "Testing", str(blue)
    #Foreground Colors
    blue, green, cyan, red, purple, yellow, white, black, gray, darkblue, darkgreen, darkcyan, darkred, darkpurple, darkyellow, darkgray = InitFG(custom)

    #Background colors
    bgblue, bggreen, bgcyan, bgred, bgpurple, bgyellow, bgwhite, bgblack, bggray, bgdarkblue, bgdarkgreen, bgdarkcyan, bgdarkred, bgdarkpurple, bgdarkyellow, bgdarkgray = InitBG(custom)

    return blue, green, cyan, red, purple, yellow, white, black, gray, darkblue, darkgreen, darkcyan, darkred, darkpurple, darkyellow, darkgray, bgblue, bggreen, bgcyan, bgred, bgpurple, bgyellow, bgwhite, bgblack, bggray, bgdarkblue, bgdarkgreen, bgdarkcyan, bgdarkred, bgdarkpurple, bgdarkyellow, bgdarkgray
    #Background colors
    #print "X"


def Dprint(text, file=logfile):
    file.write("\n" + text)
    file.flush()
    print "\n" + text
    
def NewGame(zztfile, screen, RESOLUTION, FSCREEN, hud):
    global framerate
    #framerate = 9.1032548384
    framerate = 10
    #framerate = 1
    loading = pygame.image.load("gfx/loading.png")
    screen.blit(loading, (192,154))
    pygame.display.update()
    #os.lseek(fd, pos, how)
    temp        = ""
    game        = None
    custom      = None
    #world       = None

    ammo        = 0
    torches     = 0
    health      = 0
    tcycles     = 0
    gems        = 0
    score       = 0
    keys        = 0
    timepassed  = 0
    
    #allboards   = []
    boardstartpos= 512

    #Time and input initial variables
    seconds = 0
    cycles = 0
    input = "null"
    
    #Open the ZZT file
    temp = ""
    #game = os.open(zztfile, os.O_RDONLY)
    #game = os.open(zztfile, os.O_RDONLY | os.O_BINARY)
    game = open_binary(zztfile)
    
    #Check if this is a valid ZZT file
    temp = read2(game)
    if temp != 65535 and temp != 12609:
        Dprint(str(temp) + "Invalid file")
        exit()
    else:
        Dprint("Valid ZZT file. Proceeding to load...")
    
    #Activate any custom graphics/palletes. Currently broken due to namespace.
    try:
        custom = open((zztfile[:-4]+".tyx"), "r")
        print "Loading custom data for", zztfile
        blue, green, cyan, red, purple, yellow, white, black, gray, darkblue, darkgreen, darkcyan, darkred, darkpurple, darkyellow, darkgray, bgblue, bggreen, bgcyan, bgred, bgpurple, bgyellow, bgwhite, bgblack, bggray, bgdarkblue, bgdarkgreen, bgdarkcyan, bgdarkred, bgdarkpurple, bgdarkyellow, bgdarkgray = customdata(zztfile[:-4])
    except IOError:
        Dprint("No custom data")
        if options[5] != "Tyger":
            print "Applying user font -", options[5]
            blue, green, cyan, red, purple, yellow, white, black, gray, darkblue, darkgreen, darkcyan, darkred, darkpurple, darkyellow, darkgray, bgblue, bggreen, bgcyan, bgred, bgpurple, bgyellow, bgwhite, bgblack, bggray, bgdarkblue, bgdarkgreen, bgdarkcyan, bgdarkred, bgdarkpurple, bgdarkyellow, bgdarkgray = customdata(options[5])
        else:
            blue, green, cyan, red, purple, yellow, white, black, gray, darkblue, darkgreen, darkcyan, darkred, darkpurple, darkyellow, darkgray, bgblue, bggreen, bgcyan, bgred, bgpurple, bgyellow, bgwhite, bgblack, bggray, bgdarkblue, bgdarkgreen, bgdarkcyan, bgdarkred, bgdarkpurple, bgdarkyellow, bgdarkgray = customdata("")
    
    #Get world data
    world = World(game)
    
    #DEBUG DISPLAY WORLD
    print str(world)
    
    #Create counters
    ammo        = world.ammo
    torches     = world.torches
    health      = world.health
    tcycles     = world.tcycles
    ecycles     = world.ecycles
    gems        = world.gems
    score       = world.score
    keys        = world.keys
    timepassed  = world.timepassed
    flags       = world.flag
    
    #Print World Information
    Dprint("*"*50)
    #Dprint(str(world))
    #Dprint("*"*50)
    
    #Board setup
    allboards           = []
    boardstartpos       = 512
    #Loop this for every board (world.boards for total # of boards)
    for x in range(0, world.boards+1):
        board = Board(game, boardstartpos, x)              #First board will always be at dec addr 512
        allboards.append(board)                         #Add the board to the final array of every room
        boardstartpos = boardstartpos + board.size + 2  #You have to include the 2 board size bytes since that's what we want to read next
    
    #Load the correct room to start playing in
    currentboard = 0
    board = allboards[currentboard]
    
    #Replace the player with a monitor
    board.room[board.statcoords[0][0]][board.statcoords[0][1]] = Element("monitor", 32, gray, bgblack, board.statcoords[0])
    board.room[board.statcoords[0][0]][board.statcoords[0][1]].cycle = 1
    
    #Draw the HUD!
    drawhud(screen, RESOLUTION, FSCREEN, hud, health, ammo, torches, tcycles, ecycles, gems, score, keys, timepassed)
    pygame.display.update()
    #Draw that board!
    drawboard(screen, board)

    pygame.display.set_caption("Tyger - " + zztfile + " - " + world.gamename + " - " + board.title)
    #return world, board, currentboard, allboards, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed
    return world, board, currentboard, allboards, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, blue, green, cyan, red, purple, yellow, white, black, gray, darkblue, darkgreen, darkcyan, darkred, darkpurple, darkyellow, darkgray, bgblue, bggreen, bgcyan, bgred, bgpurple, bgyellow, bgwhite, bgblack, bggray, bgdarkblue, bgdarkgreen, bgdarkcyan, bgdarkred, bgdarkpurple, bgdarkyellow, bgdarkgray
    
def playgame(world, allboards, screen):
    print "Playing"
    random.seed()
    print "RNG seeded"
    #print str(len(allboards))
    #print str(allboards)
    board = allboards[world.startboard]
    #Replace the first stat element with a player
    board.room[board.statcoords[0][0]][board.statcoords[0][1]] = Element("player", 2, white, bgdarkblue, board.statcoords[0])
    board.room[board.statcoords[0][0]][board.statcoords[0][1]].cycle = 1
    #Put whatever is beneath the player on the under layer
    #board.roomunder[board.statcoords[0][0]][board.statcoords[0][1]] = UnderOver(board.room[board.statcoords[0][0]][board.statcoords[0][1]].underID, board.room[board.statcoords[0][0]][board.statcoords[0][1]].underColor, board.room[board.statcoords[0][0]][board.statcoords[0][1]].coords)
    drawboard(screen, board)
    pygame.display.update()
    
def imageUnload(board):
    for col in xrange(0,25):
        for row in xrange(0,60):
            board.room[col][row].image = None #POIT.

def Spawn(name, character, foreground, background, coords, xstep, ystep, cycle, param1, param2, param3, follownum = "", leadnum = "", uID = 0, uColor = 0, line = 0, ooplength = 0, oop = None):
    temp = Element(name, character, foreground, background, coords)
    #print "Spawning... " + name
    #Stats
    temp.xstep = xstep
    temp.ystep = ystep
    temp.cycle = cycle
    temp.param1 = param1
    temp.param2 = param2
    temp.param3 = param3
    temp.follownum = follownum
    temp.leadnum = leadnum
    temp.underID = uID
    temp.underColor = uColor
    temp.line = line
    temp.oopLength = ooplength
    temp.oop = oop
    temp.image = makeimage(temp.character, temp.foreground, temp.background)
    return temp

def open_binary(path):
    flags = os.O_RDONLY
    if hasattr(os, 'O_BINARY'):
        flags = flags | os.O_BINARY
    return os.open(path, flags)

def SaveGame(name, allboards, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, board, world):
    if name == "":
        name = world.gamename
    save = open(name + ".sav", "wb")
    
    #Overflow array
    overflow = []
    
    #ZZT File bytes - 2 bytes
    save.write(chr(255)*2)
    
    print "Number of boards...", len(allboards)-1
    #Number of boards - 2 bytes
    if len(allboards)-1 <= 255:
        save.write(chr(len(allboards)-1))
        save.write(chr(0))
    else: #DOUBLECHECK
        temp = len(allboards)-1
        save.write(chr(temp%256))
        save.write(chr(temp/256))
        
    #Ammo - 2 bytes
    if ammo <= 32767:
        save.write(chr(ammo%256))
        save.write(chr(ammo/256))
    else:
        save.write(chr(255)*2)
        overflow.append(("ammo", ammo))
    
    #Gems - 2 bytes
    if gems <= 32767:
        save.write(chr(gems%256))
        save.write(chr(gems/256))
    else:
        save.write(chr(255)*2)
        overflow.append(("gems", gems))
        
    #Keys - 2 bytes
    for key in keys[:-1]:
        save.write(chr(key))
    if keys[7] > 0: #Black key
        overflow.append(("Blackkey", keys[7]))
        
    #Health - 2 bytes
    if health <= 32767:
        save.write(chr(health%256))
        save.write(chr(health/256))
    else:
        save.write(chr(255)*2)
        overflow.append(("health", health))
        
    #Startingboard - 2 bytes
    if board.number <= 255:
        save.write(chr(board.number))
        save.write(chr(0))
    else: #DOUBLECHECK
        save.write(chr(board.number%256))
        save.write(chr(board.number/256))
    
    #Torches
    if torches <= 32767:
        save.write(chr(torches%256))
        save.write(chr(torches/256))
    else:
        save.write(chr(255)*2)
        overflow.append(("torches", torches))
        
    #Torch Cycles
    if tcycles <= 32767:
        save.write(chr(tcycles%256))
        save.write(chr(tcycles/256))
    else:
        save.write(chr(255)*2)
        overflow.append(("tcycles", tcycles))
        
    #Energizer Cycles
    if ecycles <= 32767:
        save.write(chr(ecycles%256))
        save.write(chr(ecycles/256))
    else:
        save.write(chr(255)*2)
        overflow.append(("ecycles", ecycles))
        
    #Additonal save data Pt. 1
    save.write(chr(255)*2) #We'll go back to these bytes eventually
    
    #Score
    if score <= 32767:
        save.write(chr(score%256))
        save.write(chr(score/256))
    else:
        save.write(chr(255)*2)
        overflow.append(("score", score))
        
    #Game Name Length + Game Name
    save.write(chr(world.gamenamelength))
    padding = 20 - world.gamenamelength
    save.write(world.gamename)
    save.write(chr(0)*padding)
    
    #Flags
    print flags
    for flag in flags[:10]: #Store the first 10 flags
        if flag == "":
            save.write(21*chr(0))
        else:
            save.write(chr(len(flag)))
            save.write(flag[:20]) #20 Character limit is enforced
            if len(flag) < 20:
                save.write((20-len(flag))*chr(0))
    
    #Unused flags
    if len(flags) < 10:
        save.write((21*chr(0))*(10-len(flags)))
    
    #Extra Flags
    if len(flags) > 10:
        for flag in flags[10:]:
            overflow.append("flag", flag)
            
    #Time passed
    if timepassed <= 32767:
        save.write(chr(timepassed%256))
        save.write(chr(timepassed/256))
    else:
        save.write(chr(255)*2)
        overflow.append(("timepassed", timepassed))
        
    #Title Color/Length
    save.write(chr(world.gamecolor))
    save.write(chr(world.gamelength))
    
    #Save Byte
    save.write(chr(1))
    
    #Game name
    save.write(world.gamename)
    save.write((42-len(world.gamename))*chr(0))
    
    #Excess padding
    save.write(chr(0)*205)
    
    print save.tell()
    
    #----------------------------------------------------
    #Board Data
    #----------------------------------------------------
    for room in allboards:
        if room.number == board.number:
            overflow = SaveBoard(save, save.tell(), allboards, board, world, overflow)
        else:
            overflow = SaveBoard(save, save.tell(), allboards, room, world, overflow)
    
    return #Done saving
    
def SaveBoard(save, address, allboards, board, world, overflow):
    print "Saving board... \"", board.title, "\"", board.number
    #Since we need to backtrack it's easier to write values to variables first then concat. them later
    boardsize = 0
    print "Board size bytes are at:", address
    save.write(chr(255)*2)#DEBUG TEMPORARY LINE
    
    #Board title and length
    titlelength = chr(board.titlelength)
    title = board.title + (50-len(board.title))*chr(0)
    
    save.write(titlelength)#DEBUG TEMPORARY LINE
    save.write(title)#DEBUG TEMPORARY LINE
    
    #Now we work the magic...    
    elements = 0 #This counts to 1500
    times = 0
    oldbase = None
    
    while elements < 1500:
        x = elements / 60 #0-24
        y = elements % 60 #0-59
        
        base = (board.room[x][y].name, board.room[x][y].foregroundcolor, board.room[x][y].backgroundcolor) #This is the base element
        if (base == oldbase):
            #print "Match!", x, y
            times = times + 1 #How many times does the element occur
        else:
            if oldbase == None:
                times = times + 1
                #print "First element"
            
            if oldbase != None:
                #print base[0] + " isn't " + oldbase[0]
                #elements = elements + times
                #print "Writing:", times, oldbase[0]
                
                #Check for under 256 repetitions:
                if times < 256:
                    save.write(chr(times)) #Times the element occurs
                    save.write(chr(RevIDDict[oldbase[0]])) #ID of element
                    save.write(chr((RevColorDict[oldbase[2]]*16) + (RevColorDict[oldbase[1]]))) #Color of element
                    boardsize = boardsize + 3 #Increase board size!
                    #chr((RevIDDict[oldbase[1]]*16) + (RevIDDict[oldbase[2]]))
                else:
                    while times > 256:
                        save.write(chr(255)) #Max size
                        save.write(chr(RevIDDict[oldbase[0]])) #ID of element
                        save.write(chr((RevColorDict[oldbase[2]]*16) + (RevColorDict[oldbase[1]]))) #Color of element
                        boardsize = boardsize + 3 #Increase board size!
                        times = times - 255
                    save.write(chr(times)) #Max size
                    save.write(chr(RevIDDict[oldbase[0]])) #ID of element
                    save.write(chr((RevColorDict[oldbase[2]]*16) + (RevColorDict[oldbase[1]]))) #Color of element
                
                
                #Reset
                times = 1
            oldbase = base
            #print "Adding:", times, base[0]
            
            
        
        elements = elements + 1
    #-------------------------------------------------------------
        
    #Check for under 256 repetitions:
    print "Finishing:", times, base[0]
    if times < 256:
        save.write(chr(times)) #Times the element occurs
        save.write(chr(RevIDDict[base[0]])) #ID of element
        save.write(chr((RevColorDict[oldbase[2]]*16) + (RevColorDict[oldbase[1]]))) #Color of element
        boardsize = boardsize + 3 #Increase board size!
    else:
        while times > 256:
            save.write(chr(255)) #Max size
            save.write(chr(RevIDDict[base[0]])) #ID of element
            save.write(chr((RevColorDict[oldbase[2]]*16) + (RevColorDict[oldbase[1]]))) #Color of element
            boardsize = boardsize + 3 #Increase board size!
            times = times - 255
        save.write(chr(times)) #Max size
        save.write(chr(RevIDDict[base[0]])) #ID of element
        save.write(chr((RevColorDict[oldbase[2]]*16) + (RevColorDict[oldbase[1]]))) #Color of element
        boardsize = boardsize + 3 #Increase board size!
    
    print "DECIMAL LOCATION:", save.tell()
    #------------------------------------------------------------
    
    #Shots on board - 1 byte
    save.write(chr(board.shots))
    
    #Dark board - 1 byte
    save.write(chr(board.dark))
    
    #Boards connected - 1 byte each
    save.write(chr(board.boardnorth))
    save.write(chr(board.boardsouth))
    save.write(chr(board.boardwest))
    save.write(chr(board.boardeast))
    
    #Re-enter when Zapped - 1 byte
    save.write(chr(board.zap))
    
    #Message length + Message - 2 bytes + 58 bytes      DEBUG Wow something is up with this.
    if board.msglength > 0:
        save.write(chr(board.msglength-2))
        save.write(board.msg[1:-1])
        save.write(chr(0)*(58-len(board.msg[1:-1])))
    else:
        save.write(chr(0)*59) #No message
    #self.msg + " (" + str(self.msglength) + ") "
    
    #Enter X/Y - 1 byte each
    save.write(chr(board.enterX))
    save.write(chr(board.enterY))
    
    #Time limit - 2 bytes
    if board.timelimit <= 32767:
        save.write(chr(board.timelimit%256))
        save.write(chr(board.timelimit/256))
    else:
        save.write(chr(255)*2)
        overflow.append(("timelimit", timelimit))

    #More padding! - 16 bytes
    save.write(chr(0)*16)
    
    #-------------------------------------------------------------
    
    #Number of stat elements besides the player - 2 bytes
    save.write(chr((len(board.statcoords)-1)%256))
    save.write(chr((len(board.statcoords)-1)/256))
    
    for coords in board.statcoords:
        
        #Pre-emptive error prevention
        """if (board.room[coords[0]][coords[1]].xstep == ""):
            board.room[coords[0]][coords[1]].xstep = 0
        if (board.room[coords[0]][coords[1]].ystep == ""):
            board.room[coords[0]][coords[1]].ystep = 0
        """
        #X/Y Coordinates - 1 byte each
        save.write(chr(coords[1]+1)) #X-coord (Tyger uses 0-24. ZZT uses 1-25)
        save.write(chr(coords[0]+1)) #Y-coord (Tyger uses 0-59. ZZT uses 1-60)
        
        
        #X/Y-step - 2 bytes each
        save.write(chr(board.room[coords[0]][coords[1]].xstep/256))
        save.write(chr(board.room[coords[0]][coords[1]].xstep/256))
        save.write(chr(board.room[coords[0]][coords[1]].ystep%256))
        save.write(chr(board.room[coords[0]][coords[1]].ystep/256))
        
        #Cycle - 2 bytes
        save.write(chr(board.room[coords[0]][coords[1]].cycle%256))
        save.write(chr(board.room[coords[0]][coords[1]].cycle/256))
        
        #Parameters 1-3 - 1 byte each
        save.write(chr(board.room[coords[0]][coords[1]].param1))
        save.write(chr(board.room[coords[0]][coords[1]].param2))
        save.write(chr(board.room[coords[0]][coords[1]].param3))
        
        #Follow/Lead Number - 2 bytes each
        if board.room[coords[0]][coords[1]].follownum == "":
            board.room[coords[0]][coords[1]].follownum = 0
        if board.room[coords[0]][coords[1]].leadnum == "":
            board.room[coords[0]][coords[1]].leadnum = 0
        #print "TEST", board.room[coords[0]][coords[1]].follownum%256
        save.write(chr(board.room[coords[0]][coords[1]].follownum%256))
        save.write(chr(board.room[coords[0]][coords[1]].follownum/256))
        save.write(chr(board.room[coords[0]][coords[1]].leadnum%256))
        save.write(chr(board.room[coords[0]][coords[1]].leadnum/256))
        
        #Under ID/Color - 1 byte each
        save.write(chr(RevIDDict[board.roomunder[coords[0]][coords[1]].name]))
        save.write(chr((RevColorDict[board.roomunder[coords[0]][coords[1]].backgroundcolor]*16) + (RevColorDict[board.roomunder[coords[0]][coords[1]].foregroundcolor])))
       
        #Pointer Padding - 1 byte
        save.write(chr(0)*4)
        
        #Current Instruction - 2 bytes
        if board.room[coords[0]][coords[1]].line < 0:
            save.write(chr(0)*2)
        else:
            save.write(chr(board.room[coords[0]][coords[1]].line%256))
            save.write(chr(board.room[coords[0]][coords[1]].line/256))
        
        #ZZT-OOP Length - 2 bytes
        save.write(chr(board.room[coords[0]][coords[1]].oopLength%256))
        save.write(chr(board.room[coords[0]][coords[1]].oopLength/256))
        #board.room[coords[0]][coords[1]].xstep
        #board.room[coords[0]][coords[1]].ystep
    
        #Padding - 8 bytes
        save.write(chr(0)*8)
        
        #ZZT-OOP - Varies
        if board.room[coords[0]][coords[1]].oopLength > 0:
            oop = board.room[coords[0]][coords[1]].oop
            oop = oop.replace("\n", "\r") #Replace newlines with Carriage Returns as ZZT wants
            save.write(oop)
            
    #Write board size finally - 2 bytes
    end = save.tell()
    print "Board bytes are at: ", address
    print "ENDING LOCATION:", end
    print "ANSWER: 2258"
    truesize = end - address - 2
    print "True size:", truesize
    save.seek(address) #Jump backwards
    save.write(chr(truesize%256))
    save.write(chr(truesize/256))
    save.seek(end) #Jump forwards
    
    return overflow #Done.
    
def TypedInput(message, name, screen):
    userinput = ""
    coord = 0
    Oop.TextBox(message, name, screen, True)
    while 1:
        for event in pygame.event.get():
            if (event.type == KEYDOWN) and (event.key != K_RETURN): #Add a character
                if event.key == K_BACKSPACE:
                    userinput = userinput[:-1]
                    tempchar = Tyger.makeimage(32, Tyger.white, Tyger.bgdarkblue) #Create the character
                    coord = coord-1
                    if coord < 0:
                        coord = 0
                    screen.blit(tempchar, ((14+coord)*8,196)) #Stamp it onto the surface for the line
                else:
                    try: 
                        ord(event.unicode)
                        userinput = userinput + event.unicode
                        tempchar = Tyger.makeimage(ord(event.unicode), Tyger.white, Tyger.bgdarkblue) #Create the character
                        screen.blit(tempchar, ((14+coord)*8,196)) #Stamp it onto the surface for the line
                        coord = coord+1
                    except TypeError: 
                        None
                pygame.display.update()
                print userinput
            elif event.key == K_RETURN: #Submit string
                return userinput
if __name__ == '__main__': main()
