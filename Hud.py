import pygame
from pygame.locals import *
from sys import exit

def drawhud(screen, RESOLUTION, FSCREEN, hud, health, ammo, torches, tcycles, ecycles, gems, score, keys, timepassed):
    if hud == "min":
        status = pygame.image.load("gfx/minhud.png").convert()
        digits = pygame.image.load("gfx/digitsmin.png").convert()
        keyimg = pygame.image.load("gfx/keysmin.png").convert()
        screen.blit(status, (0,350))
    else:
        status = pygame.image.load("gfx/sidebar.png").convert()
        digits = pygame.image.load("gfx/digits.png").convert()
        keyimg = pygame.image.load("gfx/keys.png").convert()
        screen.blit(status, (480,0))
    image = updatehud(status, hud, digits, health, ammo, torches, tcycles, ecycles, gems, score, keys, timepassed, keyimg)
    if hud == "min":
        screen.blit(image, (0,350))
    else:
        screen.blit(image, (480,0))
    return image

def updatehud(status, hud, digits, health, ammo, torches, tcycles, ecycles, gems, score, keys, timepassed, keyimg):
    
    #Make counter strings
    health = str(health)
    ammo = str(ammo)
    torches = str(torches)
    tcycles = str(tcycles)
    gems = str(gems)
    score = str(score)
    timepassed = str(timepassed)
    
    #Show energizer time remaining if the board has no time limit.
    if timepassed == "0":
        timepassed = str(ecycles)
        
    #Temp image to create for each digit/key
    tempimage = pygame.Surface((8, 14))
    
    #Fix negatives
    if int(health) < 0:
        health = "0"
    if int(ammo) < 0:
        ammo = "0"
    if int(torches) < 0:
        torches = "0"
    if int(tcycles) < 0:
        tcycles = "0"
    if int(gems) < 0:
        gems = "0"
    if int(score) < 0:
        score = "0"
    if int(timepassed) < 0:
        timepassed = "0"
    if int(ecycles) < 0:
        ecycles ="0"
    
    if hud == "min":
        #Repeat for other counters
        #print "Keys? " + str(keys)
        #Health
        for x in range(0, len(health)):#grab each digit and blit it to the appropriate position
            position = int(health[x])*8 #Coordinate of the individual digit
            subsect = Rect(position, 0, 8, 14)
            tempimage.blit(digits, (0,0), subsect)
            status.blit(tempimage, (8*x+16,0))
        
        #Ammmo
        for x in range(0, len(ammo)):#grab each digit and blit it to the appropriate position
            position = int(ammo[x])*8 #Coordinate of the individual digit
            subsect = Rect(position, 0, 8, 14)
            tempimage.blit(digits, (0,0), subsect)
            status.blit(tempimage, (8*x+80,0))
        
        #Torches
        for x in range(0, len(torches)):#grab each digit and blit it to the appropriate position
            position = int(torches[x])*8 #Coordinate of the individual digit
            subsect = Rect(position, 0, 8, 14)
            tempimage.blit(digits, (0,0), subsect)
            status.blit(tempimage, (8*x+144,0))
            
        #Torch Cycles
        for x in range(0, len(tcycles)):#grab each digit and blit it to the appropriate position
            position = int(tcycles[x])*8 #Coordinate of the individual digit
            subsect = Rect(position, 0, 8, 14)
            tempimage.blit(digits, (0,0), subsect)
            status.blit(tempimage, (8*x+192,0))
            
        #Gems
        for x in range(0, len(gems)):#grab each digit and blit it to the appropriate position
            position = int(gems[x])*8 #Coordinate of the individual digit
            subsect = Rect(position, 0, 8, 14)
            tempimage.blit(digits, (0,0), subsect)
            status.blit(tempimage, (8*x+240,0))
            
        #Score
        for x in range(0, len(score)):#grab each digit and blit it to the appropriate position
            position = int(score[x])*8 #Coordinate of the individual digit
            subsect = Rect(position, 0, 8, 14)
            tempimage.blit(digits, (0,0), subsect)
            status.blit(tempimage, (8*x+304,0))
            
        #Timepassed
        for x in range(0, len(timepassed)):#grab each digit and blit it to the appropriate position
            position = int(timepassed[x])*8 #Coordinate of the individual digit
            subsect = Rect(position, 0, 8, 14)
            tempimage.blit(digits, (0,0), subsect)
            status.blit(tempimage, (8*x+432,0))
            
        #Keys
        for x in range(0, 7): #7 keys
            if keys[x] == 1: #If you have this key, get it to draw
                position = x*8 #Coordinate of the individual digit
                subsect = Rect(position, 0, 8, 14)
                tempimage.blit(keyimg, (0,0), subsect)
                status.blit(tempimage, (8*x+352,0))
        
    else:
        #Health
        for x in range(0, len(health)):#grab each digit and blit it to the appropriate position
            position = int(health[x])*8 #Coordinate of the individual digit
            subsect = Rect(position, 0, 8, 14)
            tempimage.blit(digits, (0,0), subsect)
            #status.blit(tempimage, (96,14*x+98))
            status.blit(tempimage, (8*x+96, 98))
        
        #Ammmo
        for x in range(0, len(ammo)):#grab each digit and blit it to the appropriate position
            position = int(ammo[x])*8 #Coordinate of the individual digit
            subsect = Rect(position, 0, 8, 14)
            tempimage.blit(digits, (0,0), subsect)
            status.blit(tempimage, (8*x+96, 112))
        
        #Torches
        for x in range(0, len(torches)):#grab each digit and blit it to the appropriate position
            position = int(torches[x])*8 #Coordinate of the individual digit
            subsect = Rect(position, 0, 8, 14)
            tempimage.blit(digits, (0,0), subsect)
            status.blit(tempimage, (8*x+96, 126))
            
        #Torch Cycles
        for x in range(0, len(tcycles)):#grab each digit and blit it to the appropriate position
            if int(tcycles) == 0:
                break
            position = int(tcycles[x])*8 #Coordinate of the individual digit
            subsect = Rect(position, 0, 8, 14)
            tempimage.blit(digits, (0,0), subsect)
            status.blit(tempimage, (8*x+120, 126))
            
        #Gems
        for x in range(0, len(gems)):#grab each digit and blit it to the appropriate position
            position = int(gems[x])*8 #Coordinate of the individual digit
            subsect = Rect(position, 0, 8, 14)
            tempimage.blit(digits, (0,0), subsect)
            status.blit(tempimage, (8*x+96, 140))
            
        #Score
        for x in range(0, len(score)):#grab each digit and blit it to the appropriate position
            position = int(score[x])*8 #Coordinate of the individual digit
            subsect = Rect(position, 0, 8, 14)
            tempimage.blit(digits, (0,0), subsect)
            status.blit(tempimage, (8*x+96,154))
            
        #Timepassed
        for x in range(0, len(timepassed)):#grab each digit and blit it to the appropriate position
            if int(timepassed) == 0:
                break
            position = int(timepassed[x])*8 #Coordinate of the individual digit
            subsect = Rect(position, 0, 8, 14)
            tempimage.blit(digits, (0,0), subsect)
            status.blit(tempimage, (8*x+96, 84))
            
        #Keys
        for x in range(0, 7): #7 keys
            if keys[x] == 1: #If you have this key, get it to draw
                position = x*8 #Coordinate of the individual digit
                subsect = Rect(position, 0, 8, 14)
                tempimage.blit(keyimg, (0,0), subsect)
                status.blit(tempimage, (8*x+96, 168))
    return status
