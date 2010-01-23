#from zzt import *
from Dictionaries import *
import Tyger
import pygame

#Tyger.Spawn("empty", 32, Tyger.black, Tyger.bgblack, (24, y), 0, 0, 0, 0, 0, 0)
#To spawn an empty

#position is the position in the array of stat objects

#Random integer shortcut! ie rnd(1,100)
rnd = lambda min, max: Tyger.random.randint(min, max)

def activate(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, world, allboards, screen):
    #Thingsdict[name]
    #print board.room[x][y].name
    #Check if it's a valid cycle for the Element to move on
    
    #print Tyger.options[0]
    if health > 0 and board.room[board.statcoords[0][0]][board.statcoords[0][1]].name == "player":
        try:
            if cycles % board.room[x][y].cycle != 0:
                return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
        except ZeroDivisionError:
            if board.room[x][y].name == "passage":
                return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
            #print "Divided by 0! " + str(board.room[x][y].name) + "'s cycle is seen as: " + str(board.room[x][y].cycle)
            #print str(board.room[x][y])
            return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
    
    if board.room[x][y].name == "player" and health > 0:
        #print str(board.statcoords[0])
        return Player(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, allboards, screen)
    elif board.room[x][y].name == "monitor":
        return Monitor(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, world, allboards, screen)
    elif board.room[x][y].name == "object":
        return Object(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed)
    elif board.room[x][y].name == "bullet":
        #print "Bullet time."
        return Bullet(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed)
    elif board.room[x][y].name == "pusher":
        #print "Whatever"
        return Pusher(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed)
    elif board.room[x][y].name == "bomb":
        return Bomb(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed) #What makes me a good demoman?
    elif board.room[x][y].name == "blinkwall":
        return Blink(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed)
    return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
    
def Player(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, allboards, screen):
    #Reduce your energizer and change graphics accordingly
    if ecycles != 0:
        ecycles = ecycles - 1
        
        #Energizer Colors
        EnerDict = {0:Tyger.bgdarkgreen, 1:Tyger.bgdarkpurple, 2:Tyger.bgdarkblue, 3:Tyger.bgdarkred, 4:Tyger.bggray, 5:Tyger.bgdarkcyan, 6:Tyger.bgdarkyellow}
        
        #print str(board.room[x][y].background)
        #Update char (alternate between char 1 and 2)
        if board.room[x][y].character == 1 or ecycles == 0:
            board.room[x][y].character = 2            
        else:
            board.room[x][y].character = 1
        
        #Update color
        board.room[x][y].background = EnerDict[cycles % 7]
        if ecycles == 0:
            board.room[x][y].background = Tyger.bgdarkblue
    
    #Pausing
    if input == "p":
        print "PAUSED"
        pygame.event.clear()
        event = pygame.event.wait()
        print str(event) + " 000"
   
    #Cheating
    if input == "cheat":
        print "CHEATS"
        return Cheats(ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board, x, y)
    #Board switching
    if (input == "up" and (x-1 < 0)) or (input == "down" and (x+1 > 24)) or (input == "left" and (y-1 < 0)) or (input == "right" and (y+1 > 59)): #Walking off the edge
        ammo, torches, health, tcycles, ecycles, gems, score, keys, timepassed, input, board = ChangeBoard(board, input, allboards, x, y, screen, ammo, torches, gems, score, health, keys, tcycles, ecycles, timepassed)
        return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board

    #Shooting
    if input == "shootup" or input == "shootdown" or input == "shootleft" or input == "shootright":
            if ammo > 0 and (board.playerbullets + 1 <= board.shots) and (((x-1 >= 0) and input == "shootup") or ((x+1 <= 25) and input == "shootdown") or ((y-1 >= 0) and input == "shootleft") or ((y+1 <= 60) and input == "shootright")): #also make sure you can shoot another bullet (as in a 5th bullet when the limit is 4)
                #print "Playerbullets: " + str(board.playerbullets)
                tile = board.room[x-(input == "shootup")+(input == "shootdown")][y-(input == "shootleft")+(input == "shootright")]
                
                #Handle spawning a bullet if you should
                if tile.name == "empty":
                    bullet = Tyger.Spawn("bullet", 248, Tyger.white, Tyger.bgblack, tile.coords, ((input=="shootright") - (input=="shootleft")), ((input=="shootdown") - (input=="shootup")), 1, 0, 0, 0)
                elif tile.name == "fake" or tile.name == "water":
                    board.roomunder[x-(input == "shootup")+(input == "shootdown")][y-(input == "shootleft")+(input == "shootright")] = board.room[x-(input == "shootup")+(input == "shootdown")][y-(input == "shootleft")+(input == "shootright")]
                    bullet = Tyger.Spawn("bullet", 248, Tyger.white, board.room[x-(input == "shootup")+(input == "shootdown")][y-(input == "shootleft")+(input == "shootright")].background, tile.coords, ((input=="shootright") - (input=="shootleft")), ((input=="shootdown") - (input=="shootup")), 1, 0, 0, 0)
                else: #Otherwise we can't spawn a bullet
                    return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
                
                ammo = ammo - 1
                board.playerbullets = board.playerbullets + 1
                board.room[x-(input == "shootup")+(input == "shootdown")][y-(input == "shootleft")+(input == "shootright")] = bullet
                board.statcoords.append((x-(input == "shootup")+(input == "shootdown"), y-(input == "shootleft")+(input == "shootright")))
            else:
                if board.shots == 0:
                    print "Can't shoot in this place!"
                if ammo < 1:
                    print "Not enough ammo!"
                return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
    #Moving
    if input == "up":
        targetA = x-1
        targetB = y
    elif input == "down":
        targetA = x+1
        targetB = y
    elif input == "left":
        targetA = x
        targetB = y-1
    elif input == "right":
        targetA = x
        targetB = y+1
    else:
        return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board

    if CollisionDict[board.room[targetA][targetB].name] == "walkable": #If the player didn't attempt to walk off the border
        board.roomunder[targetA][targetB] = board.room[targetA][targetB] #Put the space to be overwritten on the under layer
        board.room[targetA][targetB] = board.room[board.statcoords[0][0]][board.statcoords[0][1]] #The player occupies two tiles at once, quantum physics itc.
        #Replace old tile with what was underneath it
        board.room[board.statcoords[0][0]][board.statcoords[0][1]] = board.roomunder[board.statcoords[0][0]][board.statcoords[0][1]]
        board.statcoords[0] = (targetA, targetB)
        return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
    elif CollisionDict[board.room[targetA][targetB].name] == "DieItem": #We need to handle this based on what you've bumped into
        return DieItem(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, board.room[targetA][targetB].name, allboards, screen)
    elif CollisionDict[board.room[targetA][targetB].name] == "InvisWall": #Invisible wall
        return Invisible(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, board.room[targetA][targetB].name)   
    elif CollisionDict[board.room[targetA][targetB].name] == "Passage": #Passage
        return Passage(board, input, allboards, x, y, screen, ammo, torches, gems, score, health, keys, tcycles, ecycles, timepassed, targetA, targetB, flags)
    elif CollisionDict[board.room[targetA][targetB].name] == "Touch": #Object (scroll?)
        OOP_Send(board.room[targetA][targetB], ":touch")
        #Tyger.Dprint("successful :touch")
        return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
    elif CollisionDict[board.room[targetA][targetB].name] == "Push": #Pushing
        if board.room[targetA][targetB].name == "bomb" and board.room[targetA][targetB].param1 == 0: #If it's a bomb, activate it.
            board.room[targetA][targetB].param1 = 9
            board.room[targetA][targetB].character = 57
            print "Bomb activated!"
            return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board #Bombs don't move when you first light them
        return Push(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed)
    return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board

def DieItem(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, item, allboards, screen):
    injured = False
    
    #Update stats
    ammo = ammo + 5*(item == "ammo")
    torches = torches + 1*(item == "torch")
    gems = gems + 1*(item == "gem")
    score = score + 10*(item == "gem")
    health = health + 1*(item == "gem")
    
    if item == "energizer":
        ecycles = 75
        
    if ecycles == 0:
            health = health - 10*(item == "lion" or item == "tiger" or item =="bear" or item == "ruffian" or item == "head" or item == "segment" or item == "bullet" or item == "star")
            if item == "lion" or item == "tiger" or item =="bear" or item == "ruffian" or item == "head" or item == "segment" or item == "bullet" or item == "star":
                injured = True
    
    #Keys
    if board.room[x+(input=="down")-(input=="up")][y+(input=="right")-(input=="left")].name == "key":
        slot = KeyDict[board.room[x+(input=="down")-(input=="up")][y+(input=="right")-(input=="left")].foregroundcolor]
        if keys[slot] == 1:
            print "You already have this key!!!!"
            return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
        print "Got a " + board.room[x+(input=="down")-(input=="up")][y+(input=="right")-(input=="left")].foregroundcolor + " key."
        keys[slot] = 1
        
    #Doors
    if board.room[x+(input=="down")-(input=="up")][y+(input=="right")-(input=="left")].name == "door":
        slot = DoorDict[board.room[x+(input=="down")-(input=="up")][y+(input=="right")-(input=="left")].backgroundcolor]
        if keys[slot] == 0:
            print "The door is locked!"
            return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
        keys[slot] = 0
        print "Door opened!"
    
    #Pretend to be an empty so the player can walk on you
    #And kill the stat
    DestroyStat(board, x+(input=="down")-(input=="up"), y+(input=="right")-(input=="left"))
    board.room[x+(input=="down")-(input=="up")][y+(input=="right")-(input=="left")] = Tyger.Spawn("empty", 32, Tyger.black, Tyger.bgblack, (24, y), 0, 0, 0, 0, 0, 0)
    
    if board.zap == 1 and injured == True:
        #Move player to enterX/enterY coords
        print "Welp " + str(board.enterX) + " | " + str(board.enterY)
        board.room[board.enterY][board.enterX] = board.room[x][y]
        board.statcoords[0] = (board.enterY, board.enterX)
        board.room[x][y] = board.roomunder[x][y]
        
        #Reset the Time remaining
        timepassed = 0
        return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
    
    #print "REFERENCE ---------------------------------------------------------"
    #print str(board.room[x+(input=="down")-(input=="up")][y+(input=="right")-(input=="left")])
    #Make the player try to move again onto the tile which is now an "empty"
    Player(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, allboards, screen)
    return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board

def Invisible(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, item):
    board.room[x+(input=="down")-(input=="up")][y+(input=="right")-(input=="left")].name = "normal"
    if board.room[x+(input=="down")-(input=="up")][y+(input=="right")-(input=="left")].param1 > 0:
        board.room[x+(input=="down")-(input=="up")][y+(input=="right")-(input=="left")].character = board.room[x+(input=="down")-(input=="up")][y+(input=="right")-(input=="left")].param1
    else:
        board.room[x+(input=="down")-(input=="up")][y+(input=="right")-(input=="left")].character = 178
    board.room[x+(input=="down")-(input=="up")][y+(input=="right")-(input=="left")].image = Tyger.makeimage(board.room[x+(input=="down")-(input=="up")][y+(input=="right")-(input=="left")].character, board.room[x+(input=="down")-(input=="up")][y+(input=="right")-(input=="left")].foreground, board.room[x+(input=="down")-(input=="up")][y+(input=="right")-(input=="left")].background)
    return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board

def Bullet(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed):
    bullet = board.room[x][y]
    #print str(bullet.xstep) + "/" + str(bullet.ystep)
    if bullet.xstep > 127:
        None
        bullet.xstep = bullet.xstep-65536
    if bullet.ystep > 127:
        None
        bullet.ystep = bullet.ystep-65536
    #print str(bullet.xstep) + "/" + str(bullet.ystep)
    #print str((x+bullet.ystep)) + "or" + str(y+bullet.xstep) + "or" + str(x+bullet.ystep) + " or " + str(y+bullet.xstep) #If you're going over an edge
    if (x+bullet.ystep > 24) or (y+bullet.xstep > 59) or (x+bullet.ystep < 0) or (y+bullet.xstep < 0): #If you're going over an edge
        board.room[x][y] = board.roomunder[x][y] #Destroy the old bullet.
        board.statcoords[position] = "pop" #Destroy the stat
        board.playerbullets = board.playerbullets - (bullet.param1 == 0) #Reduce playerbullet count if applicable.
    elif BulletDict[board.room[x+bullet.ystep][y+bullet.xstep].name] == "solid": #Check for ricochets to deflect off of
        if abs(bullet.ystep) < 2 and abs(bullet.xstep) < 2: #Seriously, check for ricochets.
            move = False
            if board.room[x+bullet.xstep][y+bullet.ystep].name == "ricochet" or board.room[x+bullet.xstep][y+bullet.ystep*-1].name == "ricochet": #Travel N/S, bounce E/W
                #print "T south, B E/W"
                temp = bullet.xstep
                bullet.xstep = bullet.ystep
                bullet.ystep = temp
                move = True
            elif board.room[x-bullet.xstep][y-bullet.ystep].name == "ricochet" or board.room[x+bullet.xstep*-1][y+bullet.ystep].name == "ricochet": #Travel E/W, bounce N/S
                #print "T E/W, B N/S"
                temp = bullet.ystep
                bullet.ystep = bullet.xstep
                bullet.xstep = temp
                move = True
            if move:
                Bullet(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed) #Move again if you're deflecting
            else:
                board.room[x][y] = board.roomunder[x][y] #Destroy the old bullet.
                board.statcoords[position] = "pop" #Destroy the stat
                board.playerbullets = board.playerbullets - (bullet.param1 == 0) #Reduce playerbullet count if applicable.
    elif BulletDict[board.room[x+bullet.ystep][y+bullet.xstep].name] == "walkable": #The bullet can move here no problem.
        board.roomunder[x+bullet.ystep][y+bullet.xstep] = board.room[x+bullet.ystep][y+bullet.xstep] #Put what's about to be covered on the under array
        bullet.background = board.room[x+bullet.ystep][y+bullet.xstep].background #Update graphic in case of fake wall giving us a background
        board.room[x+bullet.ystep][y+bullet.xstep] = bullet #Move the bullet into the new location.
        board.room[x][y] = board.roomunder[x][y] #Destroy the old bullet.
        board.statcoords[position] = (x+bullet.ystep, y+bullet.xstep) #Update stat location
    elif BulletDict[board.room[x+bullet.ystep][y+bullet.xstep].name] == "hurt": #Haha you got shot what's the matter with you
        if ecycles == 0:
            health = health - 10 #Way to go
            if board.zap == 1:
                #Move player to enterX/enterY coords
                board.room[board.enterY][board.enterX] = board.room[board.statcoords[0][0]][board.statcoords[0][1]]
                board.room[board.statcoords[0][0]][board.statcoords[0][1]] = board.roomunder[board.statcoords[0][0]][board.statcoords[0][1]]
                board.statcoords[0] = (board.enterY, board.enterX)
        board.room[x][y] = board.roomunder[x][y] #Destroy the old bullet.
        board.statcoords[position] = "pop" #Destroy the stat
        board.playerbullets = board.playerbullets - (bullet.param1 == 0) #Reduce playerbullet count if applicable.
    elif BulletDict[board.room[x+bullet.ystep][y+bullet.xstep].name] == "destroy":
        shot = board.room[x+bullet.ystep][y+bullet.xstep].name
        score = score + (shot=="lion")+(shot=="bear")+(shot=="head")+(shot=="segment") + (2*(shot=="ruffian"))+(2*(shot=="tiger"))+(2*(shot=="segment" and board.room[x+bullet.ystep][y+bullet.xstep].follownum == 65535)) #Add score for killing built-ins
        
        #Destroy the stat of the destroyed object if it has stats.
        DestroyStat(board, x+bullet.ystep, y+bullet.xstep)
        board.room[x+bullet.ystep][y+bullet.xstep] = board.roomunder[x][y] #Wrong. Destroy what got shot by drawing what's beneath it
        #If you shot a creature its stat needs to be destroyed as well
        board.room[x][y] = board.roomunder[x][y] #Destroy the old bullet.
        board.statcoords[position] = "pop" #Destroy the stat
        board.playerbullets = board.playerbullets - (bullet.param1 == 0) #Reduce playerbullet count if applicable.
        
    elif BulletDict[board.room[x+bullet.ystep][y+bullet.xstep].name] == "ricochet":
        board.room[x][y].xstep = -1 * board.room[x][y].xstep
        board.room[x][y].ystep = -1 * board.room[x][y].ystep
        #Make it move again 
        board.roomunder[x+bullet.ystep][y+bullet.xstep] = board.room[x+bullet.ystep][y+bullet.xstep] #Put what's about to be covered on the under array
        bullet.background = board.room[x+bullet.ystep][y+bullet.xstep].background #Update graphic in case of fake wall giving us a background
        board.room[x+bullet.ystep][y+bullet.xstep] = bullet #Move the bullet into the new location.
        board.room[x][y] = board.roomunder[x][y] #Destroy the old bullet.
        board.statcoords[position] = (x+bullet.ystep, y+bullet.xstep) #Update stat location
    elif BulletDict[board.room[x+bullet.ystep][y+bullet.xstep].name] == "Shot":
        OOP_Send(board.room[x+bullet.ystep][y+bullet.xstep], ":shot") #Send the object to the label
        board.room[x][y] = board.roomunder[x][y] #Destroy the old bullet.
        board.statcoords[position] = "pop" #Destroy the stat
        board.playerbullets = board.playerbullets - (bullet.param1 == 0) #Reduce playerbullet count if applicable.
    return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board

def Monitor(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, world, allboards, screen):
    if input == "p":
        Tyger.playgame(world, allboards, screen)
        input = "playgame"
    return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board

def UnderOver(underID, underColor, coords):
    #Create an element based on what's underneath
    underColor = hex(underColor)[2:].upper()
    tile = Tyger.Element(IdDict[underID], CharDict[underID], Tyger.getFg(underColor), Tyger.getBg(underColor), coords)
    if tile.name == "empty":
        tile.image = Tyger.makeimage(tile.character, Tyger.black, Tyger.bgblack) #But change its graphic
    return tile
    #name="empty", character=32, foreground=black, background=bgblack, coords=(0,0), param1 = 0, param2 = 0, param3 = 0):
    #= zzt.Element()

def DestroyStat(board, x, y):
    #Does anything have these coordinates?
    for temp in range(0, len(board.statcoords)):
        if board.statcoords[temp] == (x, y):
            board.statcoords[temp] = "pop"
            break
            
def UpdateStat(board, x, y, a, b):
    #Does anything have these coordinates?
    #print "Updating Stat..." + str(x) + ", " + str(y)
    for temp in range(0, len(board.statcoords)):
        if board.statcoords[temp] == (x, y):
            #print "Updated!" + str(x) + "," + str(y) + " is now: " + str(a) + "," + str(b)
            board.statcoords[temp] = (a, b)
            break
    
def ChangeBoard(board, input, allboards, x, y, screen, ammo, torches, gems, score, health, keys, tcycles, ecycles, timepassed):
    #See which way you're headed
    if input == "up":
        i1 = 24
        i2 = y
        destination = board.boardnorth
    if input == "down":
        i1 = 0
        i2 = y
        destination = board.boardsouth
    if input == "left":
        i1 = x
        i2 = 59
        destination = board.boardwest
    if input == "right":
        i1 = x
        i2 = 0
        destination = board.boardeast
        
   
    if destination <= 0:
        return ammo, torches, health, tcycles, ecycles, gems, score, keys, timepassed, input, board
    #Check what's occupying the space we want to move to
    
    #A key you already have or a door with a key you don't have
    if (allboards[destination].room[i1][i2].name == "key"):
        slot = KeyDict[allboards[destination].room[i1][i2].foregroundcolor]
        if keys[slot] == 1:
            print "Couldn't walk due to double keys"
            return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
    if (allboards[destination].room[i1][i2].name == "door"):
        slot = DoorDict[allboards[destination].room[i1][i2].backgroundcolor]
        print str(slot) + " this door."
        if keys[slot] == 0:
            print "Couldn't walk due to door"
        else:
            allboards[destination].room[i1][i2] = Tyger.Spawn("empty", 32, Tyger.black, Tyger.bgblack, (i1, i2), 0, 0, 0, 0, 0, 0) #Destroy the door
            keys[slot] = 0
            return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
            
    #Unlit bombs.
    if (allboards[destination].room[i1][i2].name == "bomb" and allboards[destination].room[i1][i2].param1 == 0):
        allboards[destination].room[i1][i2].param1 = 9
    
    #A player.
    if (allboards[destination].room[i1][i2].name == "player"):
        allboards[destination].room[i1][i2] = Tyger.Spawn("empty", 32, Tyger.black, Tyger.bgblack, (i1, i2), 0, 0, 0, 0, 0, 0)
    
    #Other items
    if allboards[destination].room[i1][i2].name == "ammo" or allboards[destination].room[i1][i2].name == "torch" or allboards[destination].room[i1][i2].name == "gem" or allboards[destination].room[i1][i2].name == "forest":
        item = allboards[destination].room[i1][i2].name
        print "Item: " + item
        ammo = ammo + 5*(item == "ammo")
        print "Ammo: " + str(ammo)
        torches = torches + 1*(item == "torch")
        gems = gems + 1*(item == "gem")
        score = score + 10*(item == "gem")
        health = health + 1*(item == "gem")
        
        if ecycles == 0:
            print "Magic"
            health = health - 10*(item == "lion" or item == "tiger" or item =="bear" or item == "ruffian" or item == "head" or item == "segment")
        allboards[destination].room[i1][i2] = Tyger.Spawn("empty", 32, Tyger.black, Tyger.bgblack, (i1, i2), 0, 0, 0, 0, 0, 0)
    #If we're just walking onto empty space
    if (CollisionDict[allboards[destination].room[i1][i2].name]) == "walkable": #No work needed
        allboards[destination].roomunder[i1][i2] = allboards[destination].room[i1][i2] #Place the empty/fake beneath where the player will soon be
        
        #Destroy the destination board's current player location. This is probably the worst line of code ever.
        allboards[destination].room[allboards[destination].statcoords[0][0]][allboards[destination].statcoords[0][1]] = UnderOver(allboards[destination].room[allboards[destination].statcoords[0][0]][allboards[destination].statcoords[0][1]].underID, allboards[destination].room[allboards[destination].statcoords[0][0]][allboards[destination].statcoords[0][1]].underColor, allboards[destination].statcoords[0])
        allboards[destination].statcoords[0] = (i1, i2) #Update the stat information for the new player's location
        allboards[destination].room[i1][i2] = Tyger.Spawn("player", 2, Tyger.white, Tyger.bgdarkblue, (i1, i2), 0, 0, 1, 0, 0, 0) #Spawn a new player
        
        #Update the desination board's enterX/Y coords for being zapped
        allboards[destination].enterY = i1
        allboards[destination].enterX = i2
        
        #Now jump to the correct board.
        board = allboards[destination]
        timepassed = 0
    return ammo, torches, health, tcycles, ecycles, gems, score, keys, timepassed, input, board
    

def Passage(board, input, allboards, x, y, screen, ammo, torches, gems, score, health, keys, tcycles, ecycles, timepassed, targetA, targetB, flags):
    #Find the board we're to travel to and the important passage color
    destination = board.room[targetA][targetB].param3
    color = board.room[targetA][targetB].background
    
    #Is there a passage on this board with a matching background of the one we entered?
    passage = False
    for temp in range(0, len(allboards[destination].statcoords)):
        target = allboards[destination].statcoords[temp]
        if allboards[destination].room[target[0]][target[1]].name == "passage" and allboards[destination].room[target[0]][target[1]].background == color:
            passage = True
            break
            
    if passage == False: #There's no passage on the destination board that meets our requirements
        target = allboards[destination].statcoords[0] #We'll have to place you where the player is standing instead    
    #Destroy the destination board's current player location. This is probably the worst line of code ever and yet I have to use it again.
    allboards[destination].room[allboards[destination].statcoords[0][0]][allboards[destination].statcoords[0][1]] = UnderOver(allboards[destination].room[allboards[destination].statcoords[0][0]][allboards[destination].statcoords[0][1]].underID, allboards[destination].room[allboards[destination].statcoords[0][0]][allboards[destination].statcoords[0][1]].underColor, allboards[destination].statcoords[0])
    
    allboards[destination].statcoords[0] = target #Update the stat information for the new player's location
    
    if passage == True: #If there is a passage we have to put it on the under layer so the player doesn't crush it with his fat.
        allboards[destination].roomunder[target[0]][target[1]] = allboards[destination].room[target[0]][target[1]]
    
    #Then spawn the player in the proper position
    allboards[destination].room[target[0]][target[1]] = Tyger.Spawn("player", 2, Tyger.white, Tyger.bgdarkblue, (target[0], target[1]), 0, 0, 1, 0, 0, 0) #Spawn a new player
    
    #Now jump to the correct board.
    board = allboards[destination]
    input = "null"
    
    #Set time and things
    timepassed = 0
    board.enterY = target[0]
    board.enterX = target[1]
    
    return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board

def Push(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, xstep=1, ystep=1):
    #print "We must poosh little boulder " + input + " " + str(xstep) + " " + str(ystep)
    offA = 0
    offB = 0
    crush = False
    xstep = abs(xstep)
    ystep = abs(ystep)
    results = [board.room[x][y]] #Place the element that's pushing in the array
    #print "Push func: Input = " + str(xstep) + " | " + str(ystep)
    
    if input == "n":
        input = "up"
    elif input == "s":
        input = "down"
    elif input == "w":
        input = "left"
    elif input == "e":
        input = "right"
    
    while True:
        if input=="up":
            offA = offA - ystep
        elif input=="down":
            offA = offA + ystep
        elif input=="left":
            offB = offB - xstep
        elif input=="right":
            offB = offB + xstep
        elif input=="NW":
            offA = offA - ystep
            offB = offB - xstep
        elif input=="SW":
            offA = offA + ystep
            offB = offB - xstep
        elif input=="NE":
            offA = offA - ystep
            offB = offB + xstep
        elif input=="SE":
            offA = offA + ystep
            offB = offB + xstep
        
        #print str(x+offA) + " " + str(y+offB)
        if (x+offA) > 24 or (y+offB) > 59 or (x+offA) < 0 or (y+offB) < 0: #Check for the board edge
            if crush == False:
                break
            if crush == True:
                results.append(Tyger.Spawn("normal", 42, Tyger.white, Tyger.bgdarkblue, (666, 777), 0, 0, 0, 0, 0, 0)) #Pretend there's a normal wall instead of an infinite void. Clever girl.
        else:
            #print "Moving along" + board.room[x+offA][y+offB].name + " | " + PushDict[results[-1].name]
            results.append(board.room[x+offA][y+offB]) #Add the next element to the array
        if (results[-1].name == "sliderns" and (input == "left" or input == "right")) or (results[-1].name == "sliderew" and (input == "up" or input == "down")):
            break
        if PushDict[results[-1].name] == "stop":
            #Can we crush something instead?
            if crush == True:
                #Crush that shit
                results.reverse() #Flip the array
                for temp in range(0, len(results)):
                    if PushDict[results[temp].name] == "crush":
                        results[temp].name = "empty"
                        results.reverse() #Flip the array back to normal
                        statpos = len(results)-temp #The item about to be crushed might have stats to be removed.
                        if input == "up" or input == "down":
                            DestroyStat(board, x+statpos, y)
                        else:
                            DestroyStat(board, x, y+statpos)
                        break
                Push(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed)
                break
                #print str(results.pop())
                #force = True
            else:
                break #Fuck it we're not doing shit
        elif PushDict[results[-1].name] == "push":
            #print "Push it to the limit " + results[-1].name
            continue
        if PushDict[results[-1].name] == "go":
            #Pop the last element as it's a fake or empty and MEANINGLESS.
            results.pop()
            while len(results) > 0:
                board.room[x+offA][y+offB] = results[-1]
                #print "Updating stats"
                if input == "right" or input == "down":
                    UpdateStat(board, x+(len(results)-1)*(offA > 0), y+(len(results)-1)*(offB > 0), x+offA, y+offB)
                elif input == "up":
                    UpdateStat(board, x-(len(results)-1)*(offA <= 0), y*(offB <= 0), x+offA, y+offB)
                elif input == "left":
                    UpdateStat(board, x*(offA <= 0), y-(len(results)-1)*(offB <= 0), x+offA, y+offB) #Why I can't combine Left and Up I will never understand.
                if input=="up":
                    offA = offA + ystep
                elif input=="down":
                    offA = offA - ystep
                elif input=="left":
                    offB = offB + xstep
                elif input=="right":
                    offB = offB - xstep
                results.pop() #Pop the used element
            board.room[x][y] = board.roomunder[x][y]
            #print str(board.statcoords) + "Done pushing?"
            break
        elif PushDict[results[-1].name] == "crush":
            #print "Crushable something found"
            crush = True
            continue
    
    return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
    
    
    
def Pusher(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed):
    pushdir = "TBA"
    
    #Fix those odd overflowing numbers
    if board.room[x][y].xstep > 127:
        board.room[x][y].xstep = board.room[x][y].xstep-65536
    if board.room[x][y].ystep > 127:
        board.room[x][y].ystep = board.room[x][y].ystep-65536
     
    #Figure out which direction to push in
    #print str(pushdir) + " in pusher func"
    #print board.room[x][y].name
    #print str(board.room[x][y].xstep)
    #print str(board.room[x][y].ystep)
    if (board.room[x][y].xstep < 0) and (board.room[x][y].ystep == 0):
        pushdir = "left"
    elif (board.room[x][y].xstep > 0) and (board.room[x][y].ystep == 0):
        pushdir = "right"
    elif (board.room[x][y].ystep < 0) and (board.room[x][y].xstep == 0):
        pushdir = "up"
    elif (board.room[x][y].ystep > 0) and (board.room[x][y].xstep == 0):
        pushdir = "down"
    elif (board.room[x][y].xstep < 0) and (board.room[x][y].ystep < 0):
        pushdir = "NW"
    elif (board.room[x][y].xstep < 0) and (board.room[x][y].ystep > 0):
        pushdir = "SW"
    elif (board.room[x][y].xstep > 0) and (board.room[x][y].ystep < 0):
        pushdir = "NE"
    elif (board.room[x][y].xstep > 0) and (board.room[x][y].ystep > 0):
        pushdir = "SE"
    else:
        return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
    
    #print "Sending Push function " + pushdir
    Push(board, x, y, pushdir, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, board.room[x][y].xstep, board.room[x][y].ystep)
    return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
    
def Bomb(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed): #What makes me a good demoman?
    #print "If I were a bad demoman, I wouldn't be sittin here discussin it with ya now would I?"
    if board.room[x][y].param1 == 0: #If it's not activated there isn't anything to do.
        return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board #KA-BEWM
    elif board.room[x][y].param1 == 1: #Ya appear to have trodden on a mine!
        #print "Ohhh they're gonna haf-ta glue you back together... IN HELL. " + str(rnd(1,100))
        health = Explode(board, x, y, health, ecycles)
        board.room[x][y].param1 = -1
    elif board.room[x][y].param1 == -1: #Cleanup
        CleanBomb(board, x, y)
        return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board #Ahm gonna be all over ya, like shingles!
    else: #Couldn't ya see the bloody bomb?!
        board.room[x][y].param1 = board.room[x][y].param1 - 1 #Decrease the fuse
        
    #Update timer character
    if board.room[x][y].param1 + 48 > 255:
        board.room[x][y].character = board.room[x][y].param1 + 48 - 255
    else:
        board.room[x][y].character = board.room[x][y].param1 + 48
        if board.room[x][y].param1 == 1 or board.room[x][y].param1 == -1:
            board.room[x][y].character = 11
    return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board #Ahm drunk, YOU don't have an excuse!
    
def Explode(board, x, y, health, ecycles):
    #24,59
    
    
    
    for offset in range(-4, 5):
        #Check for borders
        if x-4 < 0: #If the top row of the explosion will be offscreen
            break #Move to the next row
        if y+offset < 0 or y+offset > 59: #If the leftmost column of the explosion will be offscreen
            continue #Move to the next column
        if BombDict[board.room[x-4][y+offset].name] == "boom": #If the thing is destroyed
            DestroyStat(board, x-4, y+offset) #Destroy its stat
            #Pick a random color for the breakable wall
            if board.roomunder[x-4][y+offset].name == "fake": #If the lion or whatever is on a fake wall
                board.room[x-4][y+offset] = board.roomunder[x-4][y+offset]
            else:
                board.room[x-4][y+offset] = Tyger.Spawn("breakable", 177, Tyger.random.sample([Tyger.blue, Tyger.green, Tyger.cyan, Tyger.red, Tyger.purple, Tyger.yellow, Tyger.white], 1)[0], Tyger.bgblack, (24, y), 0, 0, 0, 0, 0, 0)
        elif BombDict[board.room[x-4][y+offset].name] == "bombed": #If the thing is an object
            print "YOU'RE ALL BLOODY DEAD"
        elif BombDict[board.room[x-4][y+offset].name] == "hurt" and ecycles == 0: #They'll haf-ta bury what's left of ya' in a soup can!
            health = health - 10
    
    for offset in range(-5, 6):
        #Check for borders
        if x-3 < 0: #If the top row of the explosion will be offscreen
            break #Move to the next row
        if y+offset < 0 or y+offset > 59: #If the leftmost column of the explosion will be offscreen
            continue #Move to the next column
        if BombDict[board.room[x-3][y+offset].name] == "boom": #If the thing is destroyed
            DestroyStat(board, x-3, y+offset) #Destroy its stat
            #Pick a random color for the breakable wall
            if board.roomunder[x-3][y+offset].name == "fake": #If the lion or whatever is on a fake wall
                board.room[x-3][y+offset] = board.roomunder[x-3][y+offset]
            else:
                board.room[x-3][y+offset] = Tyger.Spawn("breakable", 177, Tyger.random.sample([Tyger.blue, Tyger.green, Tyger.cyan, Tyger.red, Tyger.purple, Tyger.yellow, Tyger.white], 1)[0], Tyger.bgblack, (24, y), 0, 0, 0, 0, 0, 0)
        elif BombDict[board.room[x-3][y+offset].name] == "bombed": #If the thing is an object
            print "YOU'RE ALL BLOODY DEAD"
        elif BombDict[board.room[x-3][y+offset].name] == "hurt": #They'll haf-ta bury what's left of ya' in a soup can!
            health = health - 10

    for offset in range(-6, 7):
        #Check for borders
        if x-2 < 0: #If the top row of the explosion will be offscreen
            break #Move to the next row
        if y+offset < 0 or y+offset > 59: #If the leftmost column of the explosion will be offscreen
            continue #Move to the next column
        if BombDict[board.room[x-2][y+offset].name] == "boom": #If the thing is destroyed
            DestroyStat(board, x-2, y+offset) #Destroy its stat
            #Pick a random color for the breakable wall
            if board.roomunder[x-2][y+offset].name == "fake": #If the lion or whatever is on a fake wall
                board.room[x-2][y+offset] = board.roomunder[x-2][y+offset]
            else:
                board.room[x-2][y+offset] = Tyger.Spawn("breakable", 177, Tyger.random.sample([Tyger.blue, Tyger.green, Tyger.cyan, Tyger.red, Tyger.purple, Tyger.yellow, Tyger.white], 1)[0], Tyger.bgblack, (24, y), 0, 0, 0, 0, 0, 0)
        elif BombDict[board.room[x-2][y+offset].name] == "bombed": #If the thing is an object
            print "YOU'RE ALL BLOODY DEAD"
        elif BombDict[board.room[x-2][y+offset].name] == "hurt": #They'll haf-ta bury what's left of ya' in a soup can!
            health = health - 10    
    
    for offset in range(-6, 7):
        #Check for borders
        if x-1 < 0: #If the top row of the explosion will be offscreen
            break #Move to the next row
        if y+offset < 0 or y+offset > 59: #If the leftmost column of the explosion will be offscreen
            continue #Move to the next column
        if BombDict[board.room[x-1][y+offset].name] == "boom": #If the thing is destroyed
            DestroyStat(board, x-1, y+offset) #Destroy its stat
            #Pick a random color for the breakable wall
            if board.roomunder[x-1][y+offset].name == "fake": #If the lion or whatever is on a fake wall
                board.room[x-1][y+offset] = board.roomunder[x-1][y+offset]
            else:
                board.room[x-1][y+offset] = Tyger.Spawn("breakable", 177, Tyger.random.sample([Tyger.blue, Tyger.green, Tyger.cyan, Tyger.red, Tyger.purple, Tyger.yellow, Tyger.white], 1)[0], Tyger.bgblack, (24, y), 0, 0, 0, 0, 0, 0)
        elif BombDict[board.room[x-1][y+offset].name] == "bombed": #If the thing is an object
            print "YOU'RE ALL BLOODY DEAD"
        elif BombDict[board.room[x-1][y+offset].name] == "hurt": #They'll haf-ta bury what's left of ya' in a soup can!
            health = health - 10   
    
    for offset in range(-7, 8):
        #Check for borders
        if x < 0: #If the top row of the explosion will be offscreen
            break #Move to the next row
        if y+offset < 0 or y+offset > 59: #If the leftmost column of the explosion will be offscreen
            continue #Move to the next column
        if BombDict[board.room[x][y+offset].name] == "boom": #If the thing is destroyed
            DestroyStat(board, x, y+offset) #Destroy its stat
            #Pick a random color for the breakable wall
            if board.roomunder[x][y+offset].name == "fake": #If the lion or whatever is on a fake wall
                board.room[x][y+offset] = board.roomunder[x][y+offset]
            else:
                board.room[x][y+offset] = Tyger.Spawn("breakable", 177, Tyger.random.sample([Tyger.blue, Tyger.green, Tyger.cyan, Tyger.red, Tyger.purple, Tyger.yellow, Tyger.white], 1)[0], Tyger.bgblack, (24, y), 0, 0, 0, 0, 0, 0)
        elif BombDict[board.room[x][y+offset].name] == "bombed": #If the thing is an object
            print "YOU'RE ALL BLOODY DEAD"
        elif BombDict[board.room[x][y+offset].name] == "hurt": #They'll haf-ta bury what's left of ya' in a soup can!
            health = health - 10   
    
    for offset in range(-4, 5):
        #Check for borders
        if x+4 > 24: #If the top row of the explosion will be offscreen
            break #Move to the next row
        if y+offset < 0 or y+offset > 59: #If the leftmost column of the explosion will be offscreen
            continue #Move to the next column
        if BombDict[board.room[x+4][y+offset].name] == "boom": #If the thing is destroyed
            DestroyStat(board, x+4, y+offset) #Destroy its stat
            #Pick a random color for the breakable wall
            if board.roomunder[x+4][y+offset].name == "fake": #If the lion or whatever is on a fake wall
                board.room[x+4][y+offset] = board.roomunder[x+4][y+offset]
            else:
                board.room[x+4][y+offset] = Tyger.Spawn("breakable", 177, Tyger.random.sample([Tyger.blue, Tyger.green, Tyger.cyan, Tyger.red, Tyger.purple, Tyger.yellow, Tyger.white], 1)[0], Tyger.bgblack, (24, y), 0, 0, 0, 0, 0, 0)
        elif BombDict[board.room[x+4][y+offset].name] == "bombed": #If the thing is an object
            print "YOU'RE ALL BLOODY DEAD"
        elif BombDict[board.room[x+4][y+offset].name] == "hurt": #They'll haf-ta bury what's left of ya' in a soup can!
            health = health - 10
    
    for offset in range(-5, 6):
        #Check for borders
        if x+3 > 24: #If the top row of the explosion will be offscreen
            break #Move to the next row
        if y+offset < 0 or y+offset > 59: #If the leftmost column of the explosion will be offscreen
            continue #Move to the next column
        if BombDict[board.room[x+3][y+offset].name] == "boom": #If the thing is destroyed
            DestroyStat(board, x+3, y+offset) #Destroy its stat
            #Pick a random color for the breakable wall
            if board.roomunder[x+3][y+offset].name == "fake": #If the lion or whatever is on a fake wall
                board.room[x+3][y+offset] = board.roomunder[x+3][y+offset]
            else:
                board.room[x+3][y+offset] = Tyger.Spawn("breakable", 177, Tyger.random.sample([Tyger.blue, Tyger.green, Tyger.cyan, Tyger.red, Tyger.purple, Tyger.yellow, Tyger.white], 1)[0], Tyger.bgblack, (24, y), 0, 0, 0, 0, 0, 0)
        elif BombDict[board.room[x+3][y+offset].name] == "bombed": #If the thing is an object
            print "YOU'RE ALL BLOODY DEAD"
        elif BombDict[board.room[x+3][y+offset].name] == "hurt": #They'll haf-ta bury what's left of ya' in a soup can!
            health = health - 10

    for offset in range(-6, 7):
        #Check for borders
        if x+2 > 24: #If the top row of the explosion will be offscreen
            break #Move to the next row
        if y+offset < 0 or y+offset > 59: #If the leftmost column of the explosion will be offscreen
            continue #Move to the next column
        if BombDict[board.room[x+2][y+offset].name] == "boom": #If the thing is destroyed
            DestroyStat(board, x+2, y+offset) #Destroy its stat
            #Pick a random color for the breakable wall
            if board.roomunder[x+2][y+offset].name == "fake": #If the lion or whatever is on a fake wall
                board.room[x+2][y+offset] = board.roomunder[x+2][y+offset]
            else:
                board.room[x+2][y+offset] = Tyger.Spawn("breakable", 177, Tyger.random.sample([Tyger.blue, Tyger.green, Tyger.cyan, Tyger.red, Tyger.purple, Tyger.yellow, Tyger.white], 1)[0], Tyger.bgblack, (24, y), 0, 0, 0, 0, 0, 0)
        elif BombDict[board.room[x+2][y+offset].name] == "bombed": #If the thing is an object
            print "YOU'RE ALL BLOODY DEAD"
        elif BombDict[board.room[x+2][y+offset].name] == "hurt": #They'll haf-ta bury what's left of ya' in a soup can!
            health = health - 10    
    
    for offset in range(-6, 7):
        #Check for borders
        if x+1 > 24: #If the top row of the explosion will be offscreen
            break #Move to the next row
        if y+offset < 0 or y+offset > 59: #If the leftmost column of the explosion will be offscreen
            continue #Move to the next column
        if BombDict[board.room[x+1][y+offset].name] == "boom": #If the thing is destroyed
            DestroyStat(board, x+1, y+offset) #Destroy its stat
            #Pick a random color for the breakable wall
            if board.roomunder[x+1][y+offset].name == "fake": #If the lion or whatever is on a fake wall
                board.room[x+1][y+offset] = board.roomunder[x+1][y+offset]
            else:
                board.room[x+1][y+offset] = Tyger.Spawn("breakable", 177, Tyger.random.sample([Tyger.blue, Tyger.green, Tyger.cyan, Tyger.red, Tyger.purple, Tyger.yellow, Tyger.white], 1)[0], Tyger.bgblack, (24, y), 0, 0, 0, 0, 0, 0)
        elif BombDict[board.room[x+1][y+offset].name] == "bombed": #If the thing is an object
            print "YOU'RE ALL BLOODY DEAD"
        elif BombDict[board.room[x+1][y+offset].name] == "hurt" and ecycles == 0: #They'll haf-ta bury what's left of ya' in a soup can!
            health = health - 10
    
    return health
    
def CleanBomb(board, x, y):
    #24,59
    for offset in range(-4, 5):
        #Check for borders
        if x-4 < 0: #If the top row of the explosion doesn't exist
            break #Move to the next row
        if y+offset < 0 or y+offset > 59: #If the leftmost column of the explosion doesn't exist
            continue #Move to the next column
        if board.room[x-4][y+offset].name == "breakable": #If there's some explosion here
            board.room[x-4][y+offset] = board.roomunder[x-4][y+offset]
    
    for offset in range(-5, 6):
        #Check for borders
        if x-3 < 0: #If the top row of the explosion doesn't exist
            break #Move to the next row
        if y+offset < 0 or y+offset > 59: #If the leftmost column of the explosion doesn't exist
            continue #Move to the next column
        if board.room[x-3][y+offset].name == "breakable": #If there's some explosion here
            board.room[x-3][y+offset] = board.roomunder[x-3][y+offset]

    for offset in range(-6, 7):
        #Check for borders
        if x-2 < 0: #If the top row of the explosion doesn't exist
            break #Move to the next row
        if y+offset < 0 or y+offset > 59: #If the leftmost column of the explosion doesn't exist
            continue #Move to the next column
        if board.room[x-2][y+offset].name == "breakable": #If there's some explosion here
            board.room[x-2][y+offset] = board.roomunder[x-2][y+offset]

    for offset in range(-6, 7):
        #Check for borders
        if x-1 < 0: #If the top row of the explosion doesn't exist
            break #Move to the next row
        if y+offset < 0 or y+offset > 59: #If the leftmost column of the explosion doesn't exist
            continue #Move to the next column
        if board.room[x-1][y+offset].name == "breakable": #If there's some explosion here
            board.room[x-1][y+offset] = board.roomunder[x-1][y+offset]
    
    for offset in range(-7, 8):
        #Check for borders
        if x < 0: #If the top row of the explosion doesn't exist
            break #Move to the next row
        if y+offset < 0 or y+offset > 59: #If the leftmost column of the explosion doesn't exist
            continue #Move to the next column
        if board.room[x][y+offset].name == "breakable": #If there's some explosion here
            board.room[x][y+offset] = board.roomunder[x][y+offset]

    for offset in range(-4, 5):
            #Check for borders
        if x+4 < 0: #If the top row of the explosion doesn't exist
            break #Move to the next row
        if y+offset < 0 or y+offset > 59: #If the leftmost column of the explosion doesn't exist
            continue #Move to the next column
        if board.room[x+4][y+offset].name == "breakable": #If there's some explosion here
            board.room[x+4][y+offset] = board.roomunder[x+4][y+offset]

    for offset in range(-5, 6):
            #Check for borders
        if x+3 < 0: #If the top row of the explosion doesn't exist
            break #Move to the next row
        if y+offset < 0 or y+offset > 59: #If the leftmost column of the explosion doesn't exist
            continue #Move to the next column
        if board.room[x+3][y+offset].name == "breakable": #If there's some explosion here
            board.room[x+3][y+offset] = board.roomunder[x+3][y+offset]

    for offset in range(-6, 7):
            #Check for borders
        if x+2 < 0: #If the top row of the explosion doesn't exist
            break #Move to the next row
        if y+offset < 0 or y+offset > 59: #If the leftmost column of the explosion doesn't exist
            continue #Move to the next column
        if board.room[x+2][y+offset].name == "breakable": #If there's some explosion here
            board.room[x+2][y+offset] = board.roomunder[x+2][y+offset]
    
    for offset in range(-6, 7):
            #Check for borders
        if x+1 < 0: #If the top row of the explosion doesn't exist
            break #Move to the next row
        if y+offset < 0 or y+offset > 59: #If the leftmost column of the explosion doesn't exist
            continue #Move to the next column
        if board.room[x+1][y+offset].name == "breakable": #If there's some explosion here
            board.room[x+1][y+offset] = board.roomunder[x+1][y+offset]
            
    #Lastly, destroy the bomb itself.
    DestroyStat(board, x, y)
    #print str(board.roomunder[x][y])
    board.room[x][y] = board.roomunder[x][y]
def Blink(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed):
    #Easier directional refences
    if board.room[x][y].xstep > 127:
        board.room[x][y].xstep = board.room[x][y].xstep-65536
    if board.room[x][y].ystep > 127:
        board.room[x][y].ystep = board.room[x][y].ystep-65536
    
    ns = board.room[x][y].ystep
    ew = board.room[x][y].xstep
    #Param 1 = Start time
    #Param 2 = Period
    #Param 3 = Time left?
    #Come up with what type of blink wall to blink into existence
    if (board.room[x][y].ystep == -1 or board.room[x][y].ystep == 1) and board.room[x][y].xstep == 0:
        wall = Tyger.Spawn("vertray", 186, board.room[x][y].foreground, board.room[x][y].background, (0, 0), 0, 0, 0, 0, 0, 0)
    else:
        wall = Tyger.Spawn("horizray", 205, board.room[x][y].foreground, board.room[x][y].background, (0, 0), 0, 0, 0, 0, 0, 0)
    
    #Set param3 timer to param1, start time
    #print str(board.room[x][y].param1) + " | " + str(board.room[x][y].param2) + " | " + str(board.room[x][y].param3) 
    #If we still have the initial delay...
    
    #board.room[x][y].param3 = board.room[x][y].param3 + 1 #Increase the wall's timer
    if board.room[x][y].param3 > (board.room[x][y].param1 + (board.room[x][y].param2) * 4):
        board.room[x][y].param3 = board.room[x][y].param1
    
    if board.room[x][y].param3 > board.room[x][y].param1: #If the current timer is more than the start time...
        #if ((board.room[x][y].param3 + 1) * 2)>= (board.room[x][y].param1 + board.room[x][y].param2): #And less than the start time + the period, turn the wall on
        print str(board.room[x][y].param3 - board.room[x][y].param1) + " < " + str((board.room[x][y].param2 + 1) + board.room[x][y].param1)
        if (board.room[x][y].param3 - board.room[x][y].param1) < (board.room[x][y].param2 + 1 + board.room[x][y].param1): #And less than the start time + the period, turn the wall on
            print "Line goes on"
            while board.room[x+ns][y+ew].name == "empty" or board.room[x+ns][y+ew].name == "gem" or board.room[x+ns][y+ew].name == "bullet" or board.room[x+ns][y+ew].name == "lion" or board.room[x+ns][y+ew].name == "tiger" or board.room[x+ns][y+ew].name == "bear" or board.room[x+ns][y+ew].name == "ruffian" or board.room[x+ns][y+ew].name == "head" or board.room[x+ns][y+ew].name == "segment":
                    if board.room[x+ns][y+ew].name == "player": #Handle player zapping
                        print "You got owned."
                    
                    board.playerbullets = board.playerbullets - ((board.room[x+ns][y+ew].param1 == 0)*board.room[x+ns][y+ew].name == "bullet") #Reduce playerbullet count if applicable.
                    DestroyStat(board, x+ns, y+ew) #Destroy the stat if necessary
                    board.room[x+ns][y+ew] = wall #Draw the wall
                    #Increase directional variables
                    if ns != 0:
                        ns = ns + board.room[x][y].ystep
                    if ew != 0:
                        ew = ew + board.room[x][y].xstep
        else:
            print "Line goes off"
            #Disable the ray
            while board.room[x+ns][y+ew].name == "horizray" or board.room[x+ns][y+ew].name == "vertray":
                if (board.room[x+ns][y+ew].name == "horizray" and wall.name == "vertray") or (board.room[x+ns][y+ew].name == "vertray" and wall.name == "horizray"):
                    break
                board.room[x+ns][y+ew] = Tyger.Spawn("empty", 32, Tyger.black, Tyger.bgblack, (x+ns, y+ew), 0, 0, 0, 0, 0, 0) #Erase the wall
                #Increase directional variables
                if ns != 0:
                    ns = ns + board.room[x][y].ystep
                if ew != 0:
                    ew = ew + board.room[x][y].xstep
    #print "Param 3 is " + str(board.room[x][y].param3)
    board.room[x][y].param3 = board.room[x][y].param3 + 1 #Increase the wall's timer
    """
    if board.room[x][y].param3 < board.room[x][y].param1:
        print "Trigger 1 " + str(board.room[x][y].param1) + " " + str(board.room[x][y].param2) + " " + str(board.room[x][y].param3)
        #Increase param3
        #print "Increasing P3. Was... " + str(board.room[x][y].param3)
        board.room[x][y].param3 = board.room[x][y].param3 + 1 #Eventually this wait time will end
        blah = board.room[x][y].param3 + 1 #Python why do i need both these lines for anything to occur?
        board.room[x][y].param3 = blah
        return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board #Be done with it?
        #print "New P3:" + str(board.room[x][y].param3)
    elif board.room[x][y].param3 == board.room[x][y].param1:
        print "Trigger 2 " + str(board.room[x][y].param1) + " " + str(board.room[x][y].param2) + " " + str(board.room[x][y].param3)
        #Starting time is over, we now need to loop the beam
        board.room[x][y].param3 = ((board.room[x][y].param2 + 1) * 2 + 1) + board.room[x][y].param1
        #print "Loop beam" + str(board.room[x][y].param3)
    if board.room[x][y].param3 > board.room[x][y].param2:
        #Now determin if the wall should be on or off
        print "Trigger 3 " + str(board.room[x][y].param1) + " " + str(board.room[x][y].param2) + " " + str(board.room[x][y].param3)
        if (board.room[x][y].param3 - board.room[x][y].param1) > (board.room[x][y].param2 + 1): #If the offset time is more than the period, take a shine of the laser beam
            #print str(x+ns) + " " + str(y+ew)
            while board.room[x+ns][y+ew].name == "empty" or board.room[x+ns][y+ew].name == "gem" or board.room[x+ns][y+ew].name == "bullet" or board.room[x+ns][y+ew].name == "lion" or board.room[x+ns][y+ew].name == "tiger" or board.room[x+ns][y+ew].name == "bear" or board.room[x+ns][y+ew].name == "ruffian" or board.room[x+ns][y+ew].name == "head" or board.room[x+ns][y+ew].name == "segment":
                if board.room[x+ns][y+ew].name == "player": #Handle player zapping
                    print "You got owned."
                
                board.playerbullets = board.playerbullets - ((board.room[x+ns][y+ew].param1 == 0)*board.room[x+ns][y+ew].name == "bullet") #Reduce playerbullet count if applicable.
                DestroyStat(board, x+ns, y+ew) #Destroy the stat if necessary
                board.room[x+ns][y+ew] = wall #Draw the wall
                #Increase directional variables
                if ns != 0:
                    ns = ns + board.room[x][y].ystep
                if ew != 0:
                    ew = ew + board.room[x][y].xstep
            #print "ON        " + str(board.room[x][y].param1) + " " + str(board.room[x][y].param2) + " " + str(board.room[x][y].param3)
        else:
            #Disable the ray
            while board.room[x+ns][y+ew].name == "horizray" or board.room[x+ns][y+ew].name == "vertray":
                if (board.room[x+ns][y+ew].name == "horizray" and wall.name == "vertray") or (board.room[x+ns][y+ew].name == "vertray" and wall.name == "horizray"):
                    break
                board.room[x+ns][y+ew] = Tyger.Spawn("empty", 32, Tyger.black, Tyger.bgblack, (x+ns, y+ew), 0, 0, 0, 0, 0, 0) #Erase the wall
                #Increase directional variables
                if ns != 0:
                    ns = ns + board.room[x][y].ystep
                if ew != 0:
                    ew = ew + board.room[x][y].xstep
            #print "OFF       " + str(board.room[x][y].param1) + " " + str(board.room[x][y].param2) + " " + str(board.room[x][y].param3)
        #Reduce the timer
        board.room[x][y].param3 = board.room[x][y].param3 - 1
    else:
        #Reduce the timer anyway?
        board.room[x][y].param3 = board.room[x][y].param3 - 1
    """
    return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
    
def Cheats(ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board, x, y):
    cheat = raw_input("?")
    cheat = cheat.lower()
    
    if cheat == "ammo":
        ammo = ammo + 5
    elif cheat == "torches":
        torches = torches + 3
    elif cheat == "gems":
        gems = gems + 5
    elif cheat == "score":
        score = score + 100
    elif cheat == "health":
        health = health + 50
        board.room[board.statcoords[0][0]][board.statcoords[0][1]].name = "player"
    elif cheat == "dark": #World's dumbest cheat
        print "Lights out!"
    elif cheat == "-dark": #World's greatest cheat
        print "Lights on!"
    elif cheat == "keys":
        keys = [1, 1, 1, 1, 1, 1, 1, 1]
    elif cheat == "time":
        timepassed = timepassed - 30
    elif cheat == "zap":
        board.room[x-1][y] = Tyger.Spawn("empty", 32, Tyger.black, Tyger.bgblack, (24, y), 0, 0, 0, 0, 0, 0)
        board.room[x+1][y] = Tyger.Spawn("empty", 32, Tyger.black, Tyger.bgblack, (24, y), 0, 0, 0, 0, 0, 0)
        board.room[x][y-1] = Tyger.Spawn("empty", 32, Tyger.black, Tyger.bgblack, (24, y), 0, 0, 0, 0, 0, 0)
        board.room[x][y+1] = Tyger.Spawn("empty", 32, Tyger.black, Tyger.bgblack, (24, y), 0, 0, 0, 0, 0, 0)
        DestroyStat(board, x-1, y)
        DestroyStat(board, x+1, y)
        DestroyStat(board, x, y-1)
        DestroyStat(board, x, y+1)
    elif cheat == "idspispopd" or cheat == "noclip":
        global CollisionDict
        global ClipDict
        global NoClipDict
        
        if CollisionDict == ClipDict: #Turn on noclip
            CollisionDict = NoClipDict
            print "Noclip"
        else:
            CollisionDict = ClipDict
            print "Yesclip"
    elif cheat == "energized" or cheat == "iddqd":
        ecycles = -1
    elif cheat == "idfa" or cheat == "idkfa":
        ammo = 32767
        torches = 32767
        gems = 32767
        health = 32767
        if cheat == "idkfa":
            keys = [1, 1, 1, 1, 1, 1, 1, 1]
    elif cheat == "^^vv<><>bastart" or cheat == "^^vv<><>baselectstart":
        health = 3000
        board.room[board.statcoords[0][0]][board.statcoords[0][1]].name = "player"
    elif cheat == "count leaves":
        health = 6
        board.room[board.statcoords[0][0]][board.statcoords[0][1]].name = "player"
        ammo = 9
        torches = 1
        gems = 0
        score = 5
    elif cheat == "kill":
        board.room[board.statcoords[0][0]][board.statcoords[0][1]].name = "RIP"
    elif cheat == "explode":
        Explode(board, board.statcoords[0][0], board.statcoords[0][1], health, ecycles)
        board.room[board.statcoords[0][0]][board.statcoords[0][1]].name = "RIP"
    elif cheat[0] == "+":
        flags.append(cheat[1:])
        print str(flags)
    elif cheat[0] == "-":
        OOP_Clear(cheat[1:].upper(), flags)
    return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, "null", board
    
def OOP_Clear(flag, flags):
    #print "Before... " + str(flags)
    for x in range(0, len(flags)-1):
        if flag == flags[x]:
            flags.pop(x)
    #print str(flags)
    
def Object(board, x, y, input, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed):
    object = board.room[x][y]
    progress = 0
    Moved = True
    NoAdvance = False
    #IfCmd = False
    #Retry = False
    #print str(object.line)
    
    while progress < 33: #Only 33 non-cycle ending commands can be executed at once.
        progress = progress + 1
        
        #print object.oop
        if (object.oop == None) or (object.line == -1): #No oop, no work
            #print "Current line # is... " + str(object.line)
            break
        
        #print object.oop[object.line:]
        current = object.oop[object.line:].split("\n")[0]
        while current == "":
            #print "Yikes"
            object.line = object.line + 2
            if object.line >= object.oopLength:
                
                break
            #print "Line is... " + str(object.line + 1)
            #print str(object.oop[object.line + 1])
            current = object.oop[object.line:].split("\n")[0]
        if (object.line >= object.oopLength) or (object.line < 0):
            object.line = -1
            #print "Breaking"
            break
            
        if current[0] == "#" or current[0] == "/" or current[0] == "?" or current[0] == ":":
            current = current.lower()
        #print current + " " + str(object.line) + "           -Current command/line"
        
        #Interpret any possible command:
        
        if current.split(" ")[0] == "#become": #Ends!
            #print "I don't know shit, we gonna keep movin"
            board.room[x][y] = Tyger.Spawn("empty", 32, Tyger.black, Tyger.bgblack, (x, y), 0, 0, 0, 0, 0, 0) #TEMPORARILY MAKE #BECOME JUST #DIE
            DestroyStat(board, x, y)
        elif current.split(" ")[0] == "#bind": #
            print "A long body or tentacles are used to bind and squeeze the foe for two to five turns. It's super effective!\r"
        elif current.split(" ")[0] == "#change": #Continues
            print "THAT'S NOT #CHANGE WE CAN BELIEVE IN\r"
        elif current.split(" ")[0] == "#char": #Continues
            object.param1 = int(current.split(" ")[1])
        elif current.split(" ")[0] == "#clear": #Continues
            OOP_Clear(current.split(" ")[1].upper(), flags)
        elif current.split(" ")[0] == "#cycle": #Continues
            object.cycle = int(current.split(" ")[1])
        elif current.split(" ")[0] == "#die": #Ends!
            board.room[x][y] = Tyger.Spawn("empty", 32, Tyger.black, Tyger.bgblack, (x, y), 0, 0, 0, 0, 0, 0)
            DestroyStat(board, x, y)
            break
        elif current.split(" ")[0] == "#end": #Ends
            object.line = -1
            break
        elif current.split(" ")[0] == "#endgame": #Continues
            health = 0
        elif current.split(" ")[0] == "#give": #Continues
            #print str(current)
            if current.split(" ")[1] != "key":
                try:
                    ammo = ammo + (int(current.split(" ")[2]) * (current.split(" ")[1] == "ammo"))
                    torches = torches + (int(current.split(" ")[2]) * (current.split(" ")[1] == "torches"))
                    gems = gems + (int(current.split(" ")[2]) * (current.split(" ")[1] == "gems"))
                    score = score + (int(current.split(" ")[2]) * (current.split(" ")[1] == "score"))
                    health = health + (int(current.split(" ")[2]) * (current.split(" ")[1] == "health"))
                    timepassed = timepassed + (int(current.split(" ")[2]) * (current.split(" ")[1] == "time"))
                    #Special Tyger #gives
                    timepassed = timepassed - (int(current.split(" ")[2]) * (current.split(" ")[1] == "seconds"))
                    tcycles = tcycles + (int(current.split(" ")[2]) * (current.split(" ")[1] == "light"))
                    ecycles = ecycles + (int(current.split(" ")[2]) * (current.split(" ")[1] == "invuln"))
                except IndexError:
                    ecycles = 75 * (current.split(" ")[1] == "energizer")
            elif current.split(" ")[1] == "key":
                keys[KeyDict[current.split(" ")[2]]] = 1
        elif current.split(" ")[0] == "#go" or current.split(" ")[0] == "#try" or current.split(" ")[0][0] == "/" or current.split(" ")[0][0] == "?": #Ends
            #NoAdvance = False
            if current.split(" ")[0][0] == "/": #You're using / or ?
                command = current.split("/")[1:]
                #print str(command) + " is the / command"
            elif current.split(" ")[0][0] == "?":
                command = current.split("?")[1:]
                #print str(command) + " is the ? command"
            else: #You're using #go or #try
                #print "#Go/Try"
                command = current.split(" ")[1:]
            #print str(len(command)) + " length of commands"
            
            if len(command) == 1:
                try:
                    IsDirDict[command[-1]]#Check to see there's no afterthought command on the same line (as in /e/e#shoot e)
                except KeyError:
                    #print "Afterthought command"
                    command[-1] = command[-1].split("#")[0]
                    NoAdvance = True
                
            dir = ParseDir(command, x, y, board.statcoords[0][0], board.statcoords[0][1], object.xstep, object.ystep) #Get the raw direction "n", "s", "seek", etc.
            #print "I want to #go... " + dir
            #if board.room[x+(dir == "s")-(dir == "n")][y+(dir == "e")-(dir == "w")].name == "fake" or board.room[x+(dir == "s")-(dir == "n")][y+(dir == "e")-(dir == "w")].name == "empty":
            if ((x+(dir == "s")-(dir == "n")) < 0) or ((y+(dir == "e")-(dir == "w")) < 0) or ((x+(dir == "s")-(dir == "n")) > 24) or ((y+(dir == "e")-(dir == "w")) > 59): #Border checking
                Moved = False
                break
            
            if ObjectDict[board.room[x+(dir == "s")-(dir == "n")][y+(dir == "e")-(dir == "w")].name] == "walkable":
                board.roomunder[x+(dir == "s")-(dir == "n")][y+(dir == "e")-(dir == "w")] = board.room[x+(dir == "s")-(dir == "n")][y+(dir == "e")-(dir == "w")] #Put the fake on the under layer
                board.room[x+(dir == "s")-(dir == "n")][y+(dir == "e")-(dir == "w")] = object #Move the object
                board.room[x][y] = board.roomunder[x][y] #Destroy the old object and update its stat
                UpdateStat(board, x, y, x+(dir == "s")-(dir == "n"), y+(dir == "e")-(dir == "w"))
                Moved = True
                progress = 100 #Ok you're done parsing oop this cycle
                #print "OK I MOVED!"
                if current[0] == "#": #If you're #go-ing
                    NoAdvance = False
                #break
            elif ObjectDict[board.room[x+(dir == "s")-(dir == "n")][y+(dir == "e")-(dir == "w")].name] == "Push":
                #print "No pushing yet"
                Moved = False
                #print "Shove it!"
                #object.name = "player"
                #Push(board, x, y, dir, position, cycles, ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, board.room[x][y].xstep, board.room[x][y].ystep)
                #object.name = "object"
                #print "Left push"
                #Retry = False
                #break
            else: #If you can't walk here
                #print "Try something will ya"
                if current.split(" ")[0] == "#try":
                    try:
                        print str(IsDirDict[current.split(" ")[-1]])
                        #print "It is a direction"
                        Moved = True
                    except KeyError:
                        #print "It is not a direction..." + (":" + current.split(" ")[-1])
                        #You want to jump to this label.
                        OOP_Send(object, ":" + current.split(" ")[-1])
                        progress = 100
                        Moved = False
                else:
                    Moved = False
                    
            #/ and ? cleanup!
            if current[0] == "/" or current[0] == "?" and Moved == True: #Do some funny rewininding through the code so the automatic movement ahead makes you sync
                NoAdvance = True #We're going to advance the code manually
                #print "Current is..." + str(current) + " ... " + str(command)
                
                current = current[1:] #Get rid of the identifier for the command we already executed ie /n/s/e/w = n/s/e/w
                object.line = object.line + 1
                #print current + " is current!"
                #print current[0]
                while (current[0] != "/") and (current[0] != "?") and (current[0] != "#"):
                    object.line = object.line + 1
                    current = current[1:]
                    #print current + " is current"
                    if current == "":
                        #print "No more code!" + str(object.oop[18]) + str(object.oop[19]) + str(object.oop[20]) + str(object.oop[21]) + str(object.oop[22])
                        object.line = object.line + 1
                        break
                    #print (current[0] != "/") or (current[0] != "?") or (current[0] != "#")
                #object.line = object.line + len(current[1].split("/")
                #print str(object.line)
                """if NoAdvance == False:
                    object.line = object.line - len(current) - 1 + len(command[0]) + (len(command) != 1)
                    #object.line = object.line - len(current) - 1 + len(command[0]) + (len(command) != 1) #k
                    print str(object.line) + " not touched"
                    object.line = object.line - len(current) + len(command[0]) #end
                    print str(object.line) + " touched"
                    NoAdvance = True
                    print str(object.oop[object.line:])
                    #object.line = object.line - 1
                    
                if NoAdvance == True:
                    print "Here's what I think current is " + current + " " + str(object.line)
                    #print "Here's what current could be "  + str(object.oop[object.line:].split("\n")[0])
                    object.line = object.line + len(command[0].split("#")[0]) + 1
                    print "Future current: " + str(object.oop[object.line:].split("\n")[0])
                """    
            #break
        elif current.split(" ")[0] == "#if": #Continues
            result = False #I'm just going to assume you're a failure here.
            opposite = False #Today is NOT opposite day.
            Tyger.Dprint(str(Moved))
            #Break the if statement down
            statement = current.split(" ")[1:]
            #print str(statement)
            if statement[0] == "not": #If you want the not...
                opposite = True #Take the not.
                statement.pop(0) #And let's strip it to make things easier on ourselves
            
            #Check if your condition is builtin or a flag
            if statement[0] == "alligned" or statement[0] == "aligned":
                #condition = "alligned"
                if (x == board.statcoords[0][0]) or (y == board.statcoords[0][1]): #Are you aligned?
                    result = True
                    statement.pop(0) #Get rid of the condition
                    #next = Tyger.string.join(statement, " ") #Assemble the true command
                    #print "Results are... ", next
            elif statement[0] == "any":
                for col in xrange(0,25):
                    for row in xrange(0,60):
                        if board.room[col][row].name == statement[1]:
                            #print "Found " + statement[1]
                            result = True
                            break
                    if result == True:
                        break
                statement.pop(0) #Remove the any
                statement.pop(0) #Remove the item you searched
            
            elif statement[0] == "blocked":
                #condition = "blocked"
                statement.pop(0)
                #x = 1
                #Get the full direction
                rawdir = []
                while True:
                    #print "Top"
                    if statement[0] == "cw" or statement[0] == "ccw" or statement[0] == "rndpe" or statement[0] == "opp":
                        rawdir.append(statement[0])
                    else:
                        rawdir.append(statement[0])
                        break
                    #x = x + 1
                    statement.pop(0)
                    #print "Welp" + str(statement)
                    
                statement.pop(0)
                #print str(rawdir) + "is the raw dir" + "\n this is the command" + str(statement)
                dir = ParseDir(rawdir, x, y, board.statcoords[0][0], board.statcoords[0][1], object.xstep, object.ystep) #Find the direction to look at
                #print dir + "is dir"
                #print "Final statement: " + str(statement)
                
                if ((x+(dir == "s")-(dir == "n")) < 0) or ((y+(dir == "e")-(dir == "w")) < 0) or ((x+(dir == "s")-(dir == "n")) > 24) or ((y+(dir == "e")-(dir == "w")) > 59): #Border checking
                    result = False #Not blocked.
                else: #Actually check
                    if ObjectDict[board.room[x+(dir == "s")-(dir == "n")][y+(dir == "e")-(dir == "w")].name] == "solid" or ObjectDict[board.room[x+(dir == "s")-(dir == "n")][y+(dir == "e")-(dir == "w")].name] == "Push":
                        result = True #You're blocked!
            elif statement[0] == "contact":
                statement.pop(0) #Remove the contact
                if y-1 >= 0 and result == False: #Look left
                    if board.statcoords[0][1] == (y-1):
                        #print "Left contact!"
                        result = True
                if y+1 <= 59 and result == False: #Look right
                    if board.statcoords[0][1]  == (y+1):
                        result = True
                        #print "Right contact!"
                if x-1 >= 0 and result == False: #Look up
                    if board.statcoords[0][0] == (x-1):
                        #print "Up contact!"
                        result = True
                if x+1 <= 24 and result == False: #Look down
                    if board.statcoords[0][0] == (x+1):
                        #print "Down contact!"
                        result = True
                #if x-1 < 0 or ((y+(dir == "e")-(dir == "w")) < 0) or ((x+(dir == "s")-(dir == "n")) > 24) or ((y+(dir == "e")-(dir == "w")) > 59): #Border checking
                
            elif statement[0] == "energized":
                statement.pop(0)
                if ecycles != 0:
                    result = True
            else: #Flag
                for flag in flags:
                    if flag == statement[0].upper():
                        result = True
                        statement.pop(0) #Remove the flag name
                        #print "Flaggot"
                        break
            
            #Flip a NOT prefix
            if opposite == True:
                result = not result
            if result == True:
                next = Tyger.string.join(statement, " ") #Assemble the true command
                #Advance the code to the after command
                NoAdvance = True
                Moved = True #Maybe?
                
                object.line = object.line + len(current) - len(next)
                #print object.oop[object.line:].replace("\n", "\t") + " I advanced the code"
                if next[0] != "#" and next[0] != "/" and next[0] != "?":
                    next = ":" + next
                    OOP_Send(object, next)
                    #print "Adjusted!"
                #IfCmd = True
                
                
        elif current.split(" ")[0] == "#idle": #Ends
            progress = 100
        elif current.split(" ")[0] == "#lock": #Continues
            object.param2 = 1
        elif current.split(" ")[0] == "#play": #Continues
            print "I got my problems, and my problems they got me...\r"
        elif current.split(" ")[0] == "#put": #-
            print "POOT SENTRY HERE\r"
        elif current.split(" ")[0] == "#restart": #Continues
            object.line = 0
            continue
        elif current.split(" ")[0] == "#restore": #continues
            while object.oop.find("'" + current.split(" ")[1]) != -1:
                object.oop = object.oop.replace("'" + current.split(" ")[1], ":" + current.split(" ")[1])
                #print object.oop
        elif current.split(" ")[0] == "#set": #continues
            flags.append(current.split(" ")[1])
        elif current.split(" ")[0] == "#shoot" or current.split(" ")[0] == "#throwstar": #Ends
            progress = 100
            dir = ParseDir(current.split(" ")[1:], x, y, board.statcoords[0][0], board.statcoords[0][1], object.xstep, object.ystep) #Get the raw direction "n", "s", "seek", etc.
            #print "I want to #shoot... " + dir
            #if board.room[x+(dir == "s")-(dir == "n")][y+(dir == "e")-(dir == "w")].name == "fake" or board.room[x+(dir == "s")-(dir == "n")][y+(dir == "e")-(dir == "w")].name == "empty":
            if ((x+(dir == "s")-(dir == "n")) < 0) or ((y+(dir == "e")-(dir == "w")) < 0) or ((x+(dir == "s")-(dir == "n")) > 24) or ((y+(dir == "e")-(dir == "w")) > 59): #Border checking
                break
            
            #Can you shoot there?
            if board.room[x+(dir == "s")-(dir == "n")][y+(dir == "e")-(dir == "w")].name == "empty":
                board.roomunder[x+(dir == "s")-(dir == "n")][y+(dir == "e")-(dir == "w")] = board.room[x+(dir == "s")-(dir == "n")][y+(dir == "e")-(dir == "w")] #Put the fake/water on the under layer
                #Spawn the bullet/star
                if current.split(" ")[0] == "#throwstar":
                    board.room[x+(dir == "s")-(dir == "n")][y+(dir == "e")-(dir == "w")] = Tyger.Spawn("star", 47, Tyger.white, Tyger.bgblack, ((x-(input == "shootup")+(input == "shootdown")),(y-(input == "shootleft")+(input == "shootright"))), ((dir=="e") - (dir=="w")), ((dir=="s") - (dir=="n")), 1, 1, 0, 0)
                else:
                    board.room[x+(dir == "s")-(dir == "n")][y+(dir == "e")-(dir == "w")] = Tyger.Spawn("bullet", 248, Tyger.white, Tyger.bgblack, ((x-(input == "shootup")+(input == "shootdown")),(y-(input == "shootleft")+(input == "shootright"))), ((dir=="e") - (dir=="w")), ((dir=="s") - (dir=="n")), 1, 1, 0, 0)
                board.statcoords.append((x-(dir=="n")+(dir=="s"), y-(dir=="w")+(dir=="e"))) #Make the stat
            elif (board.room[x+(dir == "s")-(dir == "n")][y+(dir == "e")-(dir == "w")].name == "fake" or board.room[x+(dir == "s")-(dir == "n")][y+(dir == "e")-(dir == "w")].name == "water"):
                board.roomunder[x+(dir == "s")-(dir == "n")][y+(dir == "e")-(dir == "w")] = board.room[x+(dir == "s")-(dir == "n")][y+(dir == "e")-(dir == "w")] #Put the fake/water on the under layer
                #Spawn the bullet
                if current.split(" ")[0] == "#shoot":
                    board.room[x+(dir == "s")-(dir == "n")][y+(dir == "e")-(dir == "w")] = Tyger.Spawn("bullet", 248, Tyger.white, board.room[x-(dir == "n")+(dir == "s")][y-(dir == "w")+(dir == "e")].background, ((x-(input == "shootup")+(input == "shootdown")),(y-(input == "shootleft")+(input == "shootright"))), ((dir=="e") - (dir=="w")), ((dir=="s") - (dir=="n")), 1, 1, 0, 0)
                else:
                    board.room[x+(dir == "s")-(dir == "n")][y+(dir == "e")-(dir == "w")] = Tyger.Spawn("star", 47, Tyger.white, Tyger.bgblack, ((x-(input == "shootup")+(input == "shootdown")),(y-(input == "shootleft")+(input == "shootright"))), ((dir=="e") - (dir=="w")), ((dir=="s") - (dir=="n")), 1, 1, 0, 0)
                board.statcoords.append((x-(dir=="n")+(dir=="s"), y-(dir=="w")+(dir=="e"))) #Make the stat
            elif board.room[x+(dir == "s")-(dir == "n")][y+(dir == "e")-(dir == "w")].name == "player": #You got shot at point blank.
                health = health - 10
    
            #break
        elif current.split(" ")[0] == "#take": #Continues
            #print str(current)
            if current.split(" ")[1] != "key":
                try:
                    ammo = ammo - (int(current.split(" ")[2]) * (current.split(" ")[1] == "ammo"))
                    torches = torches - (int(current.split(" ")[2]) * (current.split(" ")[1] == "torches"))
                    gems = gems - (int(current.split(" ")[2]) * (current.split(" ")[1] == "gems"))
                    score = score - (int(current.split(" ")[2]) * (current.split(" ")[1] == "score"))
                    health = health - (int(current.split(" ")[2]) * (current.split(" ")[1] == "health"))
                    timepassed = timepassed - (int(current.split(" ")[2]) * (current.split(" ")[1] == "time"))
                    #Special Tyger #gives
                    timepassed = timepassed + (int(current.split(" ")[2]) * (current.split(" ")[1] == "seconds"))
                    tcycles = tcycles - (int(current.split(" ")[2]) * (current.split(" ")[1] == "light"))
                    ecycles = ecycles - (int(current.split(" ")[2]) * (current.split(" ")[1] == "invuln"))
                except IndexError:
                    ecycles = ecycles - 75 * (current.split(" ")[1] == "energizer")
            elif current.split(" ")[1] == "key":
                keys[KeyDict[current.split(" ")[2]]] = 0
        elif current.split(" ")[0] == "#unlock": #continues
            object.param2 = 0
        elif current.split(" ")[0] == "#walk": #Continues
            dir = ParseDir(current.split(" ")[1:], x, y, board.statcoords[0][0], board.statcoords[0][1], object.xstep, object.ystep) #Get the raw direction "n", "s", "seek", etc.
            object.xstep = WalkDict[dir][0]
            object.ystep = WalkDict[dir][1]
        elif current.split(" ")[0] == "#zap": #Continues
            object.oop = object.oop.replace(":" + current.split(" ")[1], "'" + current.split(" ")[1], 1)
        elif current.split(" ")[0] == "#send" or current.split(" ")[0][0] == "#":
            #print "SEND COMMAND", current
            """if IfCmd == True: #If this is an if command we just jump right to the label.
                print "Jumping to", current
                IfCmd = False
                command = ":" + current
                OOP_Send(object, command)"""
                
                
            if current.split(" ")[0] == "#send":
                #print current.split(" ")[1]
                command = current.split(" ")[1] #Reduce the command to an object and a label at most
            else:
                command = current[1:]
            #print str(command) + " is the #send without a #send"
            if command.find(":") == -1: #If it's just a label then it's for this object
                command = ":" + command
                #print "Ok jumping to " + command
                OOP_Send(object, command)
                NoAdvance = True
            else: #Otherwise we need to find the object and the label.
                name = command[:command.find(":")]
                label = command[command.find(":"):]
                #Find every object with that name
                #print "Have some objects " + name + ":" + label
                for position in board.statcoords: #Look at every stat on the screen
                    if position != "pop": #Check the stat isn't in limbo
                        if board.room[position[0]][position[1]].name == "object": #Check that you're looking at an object
                            if board.room[position[0]][position[1]].oop != None: #Check that the object has oop
                                code = board.room[position[0]][position[1]].oop.lower() #Read its name if it has one
                                code = code.split("\n")[0]
                                #print code
                                if code[1:] == name: #if the object and #send name match
                                    OOP_Send(board.room[position[0]][position[1]], label, True)
        else: #Message
            try:
                if current.split(" ")[0][0] != "#" and current.split(" ")[0][0] != "/" and current.split(" ")[0][0] != "?" and current.split(" ")[0][0] != "@" and current.split(" ")[0][0] != ":" and current.split(" ")[0][0] != "'":
                    print "--------------------" + current + "--------------------"
            except IndexError:
                print "--------------------" + current + "--------------------"
            progress = progress - 1
        
        #Move to the next line if you're still going
        
        #print str(object.line) + " " + str(Moved) + " " + str(NoAdvance)
        if object.line != -1 and Moved == True and NoAdvance == False:
            #print "Advancing code"
            object.line = object.line + len(current) + 1
        #print "Line is... " + str(object.line + 1)
        #print str(object.oop[object.line + 1])
        if object.line >= object.oopLength:
            object.line = -1
            break
        
        NoAdvance = False
        Moved = True #Maybe? Play Fridgeraid to find out for sure.
    #Post oop handling
    #if object.oopLength != 0:
        #print "Done OOPing about " + str(object.line) + " | " + str(object.oopLength)
    
    #Now get walking if you walk
    if object.xstep > 127:
        object.xstep = object.xstep-65536
    if object.ystep > 127:
        object.ystep = object.ystep-65536
    
    if object.xstep != 0 or object.ystep != 0: #If you need to walk
        if board.room[x+object.ystep][y+object.xstep].name == "fake" or board.room[x+object.ystep][y+object.xstep].name == "empty":
            board.roomunder[x+object.ystep][y+object.xstep] = board.room[x+object.ystep][y+object.xstep] #Put the fake on the under layer
            board.room[x+object.ystep][y+object.xstep] = object #Move the object
            board.room[x][y] = board.roomunder[x][y] #Destroy the old object and update its stat
            UpdateStat(board, x, y, x+object.ystep, y+object.xstep)
        else:
            OOP_Send(object, ":thud")
    
    return ammo, torches, health, flags, tcycles, ecycles, gems, score, keys, timepassed, input, board
    
def OOP_Send(object, label, extsend=False):
    if object.param2 == 1: #Check for a lock
        return
    if object.oop.lower().find(label) == -1 and extsend == True:
        return
    object.line = object.oop.lower().find(label) #Find the label
    #print "Jump to " + str(object.line)
    #x = raw_input("Press a key sir")


def ParseDir(input, x, y, Px, Py, xstep, ystep):
    #print "Input is... " + str(input) + " " + str(len(input))
    choices = []
    Tyger.Dprint(str(input))
    #blah = raw_input("Hit enter")
    if len(input) == 1:
        input = input[0].split(" ") #Fix for /opp seek
    if (input[0] == "n") or (input[0] == "s") or (input[0] == "e") or (input[0] == "w") or (input[0] == "i"):
        return input[0]
    elif input[0] == "flow":
        return FlowDict[(xstep,ystep)]
    elif input[0] == "seek":
        #if (Px == x):
        #    print "Matching X's!"
        if (Px < x): #If the player is to your left
            choices.append("n")
        elif (Px > x):
            choices.append("s")
        #if (Py == y):
        #    print "Matching Y's!"
        if (Py < y): #if the player is above you
            choices.append("w")
        elif (Py > y):
            choices.append("e")
        output = Tyger.random.sample(choices, 1)[0]
        return output
    elif input[0] == "rndns":
        return Tyger.random.sample(["n", "s"], 1)[0]
    elif input[0] == "rndne":
        return Tyger.random.sample(["n", "e"], 1)[0]
    elif input[0] == "rnd":
        return Tyger.random.sample(["n", "s", "e", "w"], 1)[0]
    elif input[0] == "cw":
        key = input[1]
        if key == "seek":
            key = ParseDir([input[1]], x, y, Px, Py, xstep, ystep)
        elif key == "flow":
            return CwDict[FlowDict[(xstep, ystep)]]
        elif key == "rndns":
            return Tyger.random.sample(["e", "w"], 1)[0] #cw from N/S is E/W
        elif key == "rndne":
            return Tyger.random.sample(["e", "s"], 1)[0] #cw from N/E is E/S
        elif key == "rnd":
            return Tyger.random.sample(["n", "s", "e", "w"], 1)[0] #I hate you.
        return CwDict[key]
    elif input[0] == "ccw":
        key = input[1]
        if key == "seek":
            key = ParseDir([input[1]], x, y, Px, Py, xstep, ystep)
        elif key == "flow":
            return CcwDict[FlowDict[(xstep, ystep)]]
        elif key == "rndns":
            return Tyger.random.sample(["e", "w"], 1)[0] #ccw from N/S is E/W
        elif key == "rndne":
            return Tyger.random.sample(["e", "s"], 1)[0] #ccw from N/E is E/S
        elif key == "rnd":
            return Tyger.random.sample(["n", "s", "e", "w"], 1)[0] #I hate you.
        return CcwDict[key]
    elif input[0] == "opp":
        key = input[1]
        if key == "seek":
            key = ParseDir([input[1]], x, y, Px, Py, xstep, ystep)
        elif key == "flow":
            return OppDict[FlowDict[(xstep, ystep)]]
        elif key == "rndns":
            return Tyger.random.sample(["n", "s"], 1)[0]
        elif key == "rndne":
            return Tyger.random.sample(["s", "w"], 1)[0]
        elif key == "rnd":
            return Tyger.random.sample(["n", "s", "e", "w"], 1)[0] #I hate you.
        return OppDict[key]
    elif input[0] == "rndp":
        key = input[1]
        if key == "seek":
            key = ParseDir([input[1]], x, y, Px, Py, xstep, ystep)
        elif key == "flow":
            return Tyger.random.sample(RndpDict[FlowDict[(xstep, ystep)]], 1)[0]
        elif key == "rndns":
            return Tyger.random.sample(["e", "w"], 1)[0]
        elif key == "rndne" or key == "rnd":
            return Tyger.random.sample(["n", "s", "e", "w"], 1)[0] #I hate you.
        return Tyger.random.sample(RndpDict[key], 1)[0]
    print "You sent an invalid direction, I'll just idle." + str(input[0]) + "|" + str(input[1])
    return "i"
    

