from Dictionaries import *
import pygame
import Tyger
import Elements
from pygame.locals import *
from sys import exit

global TextMessage
TextMessage = None

def Become(command, board, x, y):
    Elements.DestroyStat(board, x, y) #Destroy the old stat
    element = Tyger.Spawn("empty", 32, Tyger.black, Tyger.bgblack, (x, y), 0, 0, 0, 0, 0, 0) #TEMPORARILY MAKE #BECOME JUST #DIE
    return element

def Char(character):
    try:
        character = int(character)
    except ValueError:
        try:
            character = ord(character[0])
        except IndexError:
            character = 32
    return character

def Clear(flag, flags):
    #print "Clearing"
    #print "Before... " + str(flags)
    for x in range(0, len(flags)-1): #Find the flag if it exists
        if flag == flags[x]:
            flags.pop(x)
    #print str(flags)
    return flags
    
def CopyCode(board, name, object):
    for position in board.statcoords: #Look at every stat on the screen
        if position != "pop": #Check the stat isn't in limbo
            if board.room[position[0]][position[1]].name == "object": #Check that you're looking at an object
                if board.room[position[0]][position[1]].oop != None: #Check that the object has oop
                    code = board.room[position[0]][position[1]].oop.lower() #Read its name if it has one
                    code = code.split("\n")[0]
                    #print code
                    if code[1:] == name: #if the object and #send name match
                        object.oop = board.room[position[0]][position[1]].oop #Change the oop
                        object.line = 0 #Reset the object
                        object.oopLength = board.room[position[0]][position[1]].oopLength #Change the oop
                        return object
    return object
    
def Cycle(cycle, current):
    try:
        cycle = int(cycle)
        if (cycle >= 0) and (cycle <= 255): #Make sure the cycle's range is good
            #print "Setting cycle to", cycle
            return cycle
        else:
            return current
    except ValueError: #Invalid cycle, return the old cycle
        return current
    
def Die(board, x, y):
    element = Tyger.Spawn("empty", 32, Tyger.black, Tyger.bgblack, (x, y), 0, 0, 0, 0, 0, 0)
    Elements.DestroyStat(board, x, y)
    return element
    
def Give(ammo, torches, gems, score, health, timepassed, tcycles, ecycles, keys, current, board, NoAdvance):
    print "HEADS UP"
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
            if current.split(" ")[1] == "invuln":
                Send("#all:energize", board, None, -1, -1)
                return ammo, torches, gems, score, health, timepassed, tcycles, ecycles, keys, True
                #SendJump(board.room[position[0]][position[1]], label, True)
        except IndexError:
            ecycles = 75 * (current.split(" ")[1] == "energizer")
        except ValueError:
            return ammo, torches, gems, score, health, timepassed, tcycles, ecycles, keys, NoAdvance
    elif current.split(" ")[1] == "key":
        keys[KeyDict[current.split(" ")[2]]] = 1
    return ammo, torches, gems, score, health, timepassed, tcycles, ecycles, keys, NoAdvance

def Go(current, x, y, board, object, NoAdvance, Moved, progress):
    #print object.oop[0:15] + "IS THE OBJECT"
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
        
    dir = Elements.ParseDir(command, x, y, board.statcoords[0][0], board.statcoords[0][1], object.xstep, object.ystep) #Get the raw direction "n", "s", "seek", etc.
    #print "I want to #go... " + dir
    #if board.room[x+(dir == "s")-(dir == "n")][y+(dir == "e")-(dir == "w")].name == "fake" or board.room[x+(dir == "s")-(dir == "n")][y+(dir == "e")-(dir == "w")].name == "empty":
    
    if dir == "i":
        moved = False
        NoAdvance = True
        object.line = object.line + 2
        if object.oop[object.line] == "\n":
            object.line = object.line + 1
        #print "Idling line:", object.line, "Moved:", moved
        #print object.oop[object.line:object.line+15]
        print "IDLED."
        progress = 100
        
        return NoAdvance, Moved, progress
    
    if ((x+(dir == "s")-(dir == "n")) < 0) or ((y+(dir == "e")-(dir == "w")) < 0) or ((x+(dir == "s")-(dir == "n")) > 24) or ((y+(dir == "e")-(dir == "w")) > 59): #Border checking
        Moved = False
        return NoAdvance, Moved, progress
    
    if ObjectDict[board.room[x+(dir == "s")-(dir == "n")][y+(dir == "e")-(dir == "w")].name] == "walkable":
        board.roomunder[x+(dir == "s")-(dir == "n")][y+(dir == "e")-(dir == "w")] = board.room[x+(dir == "s")-(dir == "n")][y+(dir == "e")-(dir == "w")] #Put the fake on the under layer
        board.room[x+(dir == "s")-(dir == "n")][y+(dir == "e")-(dir == "w")] = object #Move the object
        board.room[x][y] = board.roomunder[x][y] #Destroy the old object and update its stat
        Elements.UpdateStat(board, x, y, x+(dir == "s")-(dir == "n"), y+(dir == "e")-(dir == "w"))
        Moved = True
        progress = 100 #Ok you're done parsing oop this cycle
        #print "OK I MOVED!"
        if current[0] == "#": #If you're #go-ing
            NoAdvance = False
        #break
    elif ObjectDict[board.room[x+(dir == "s")-(dir == "n")][y+(dir == "e")-(dir == "w")].name] == "Push":
        #print "No pushing yet"
        #Moved = True
        #print "Shove it!"
        #object.name = "player"
        Elements.Push(board, x, y, dir, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        if board.room[x][y].name == "object": #If you failed to move with pushing
            Moved = False
        else:
            Moved = True
            progress = 100 #These 30 million variables that determine how the code is advanced is the worst thing of all time.
        #print "Nope"
        #object.name = "object"
        #print "Left push"
        #Retry = False
        #break
    else: #If you can't walk here
        #print "Try something will ya"
        if current.split(" ")[0] == "#try":
            try:
                #print str(IsDirDict[current.split(" ")[-1]])
                #print "It is a direction"
                Moved = True
            except KeyError:
                #print "It is not a direction..." + (":" + current.split(" ")[-1])
                #You want to jump to this label.
                Oop.SendJump(object, ":" + current.split(" ")[-1])
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
            #print "do be do be do"
            object.line = object.line + 1
            current = current[1:]
            #print current + " is current"
            if current == "":
                #print "No more code!" + str(object.oop[18]) + str(object.oop[19]) + str(object.oop[20]) + str(object.oop[21]) + str(object.oop[22])
                object.line = object.line + 1
                return NoAdvance, Moved, progress
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
    return NoAdvance, Moved, progress

def If(current, object, x, y, board, ecycles, flags):
    result = False #I'm just going to assume you're a failure here.
    opposite = False #Today is NOT opposite day.
    #Tyger.Dprint(str(Moved))
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
    elif statement[0] == "any": #Not smart enough to understand color
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
        dir = Elements.ParseDir(rawdir, x, y, board.statcoords[0][0], board.statcoords[0][1], object.xstep, object.ystep) #Find the direction to look at
        #print dir + "is dir"
        #print "Final statement: " + str(statement)
        
        if ((x+(dir == "s")-(dir == "n")) < 0) or ((y+(dir == "e")-(dir == "w")) < 0) or ((x+(dir == "s")-(dir == "n")) > 24) or ((y+(dir == "e")-(dir == "w")) > 59): #Border checking
            result = True #Blocked by a border
        else: #Actually check
            if ObjectDict[board.room[x+(dir == "s")-(dir == "n")][y+(dir == "e")-(dir == "w")].name] == "solid" or ObjectDict[board.room[x+(dir == "s")-(dir == "n")][y+(dir == "e")-(dir == "w")].name] == "Push":
                result = True #You're blocked!
    elif statement[0] == "contact":
        statement.pop(0) #Remove the contact
        if y-1 >= 0 and result == False: #Look left
            if (board.statcoords[0][1] == (y-1)) and (board.statcoords[0][0] == x):
                #print "Left contact!"
                result = True
        if y+1 <= 59 and result == False: #Look right
            if (board.statcoords[0][1]  == (y+1)) and (board.statcoords[0][0] == x):
                result = True
                #print "Right contact!"
        if x-1 >= 0 and result == False: #Look up
            if (board.statcoords[0][0] == (x-1)) and (board.statcoords[0][1] == y):
                #print "Up contact!"
                result = True
        if x+1 <= 24 and result == False: #Look down
            if (board.statcoords[0][0] == (x+1)) and (board.statcoords[0][1] == y):
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
                print "Flaggot"
                break
        #print "Fla"
    
    #Remove any THEN's/
    if statement[0] == "then":
        print "--------------------------------POPPING A THEN!"
        statement.pop(0)
    
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
            SendJump(object, next)
            #print "Adjusted!"
        #IfCmd = True
    else:
        NoAdvance = False
        Moved = True
        #print "Line is:", object.line
    return NoAdvance, Moved, object

def Message(object, screen, board):
    NoAdvance = True    #We're going to advance the object's code manually
    breaking = False    #Breaking is whether or not we stopped reading a message due to a new command instead of end of code
    message = ""        #The formatted message begins empty of course
    lop = 0             #In the case of a multi-lined message this hits EOC we have to lop off an extra newline.
    Multiline = True    #I assume you have a textbox by default, not a flashing bottom of the screen message
    
    raw = object.oop[object.line:].split("\n")  #Get the raw code to find the message in
    
    #Find the correct end of the message
    for x in xrange(0,len(raw)):
        if raw[x] == "":
            message = message + "\n"
        elif raw[x][0] == "#" or raw[x][0] == "/" or raw[x][0] == "?" or raw[x][0] == ":" or raw[x][0] == "'": #If you found the end of the message
            breaking = True
            break #You're done finding the true message
        else:
            message = message + raw[x] + "\n"
    
    #If the message is one line, do a text box
    test = message.split("\n")
    #print "TEST!", test
    print len(test), test[1], breaking
    if (len(test) == 3 and test[1] == "" and test[2] == "" and breaking == False) or (len(test) == 2 and test[1] == "" and breaking == True):
        message = test[0]
        Multiline = False
    elif breaking == False:
        #print "===============lopping"
        message = message[:-1]
        lop = 1
    #print message + "-----------------"
    
    #At this point the message is properly split line by line!
    
    if Multiline:
        label = TextBox(message, object.oop.split("\n")[0], screen)
        if label != None:
            SendJump(object, label)
            return NoAdvance, object
    else:
        
        MessageLine(message, screen, board)
        #screen.blit(tempimg, (0,0))
        #pygame.display.update()
        #Tyger.message.append(tempimg)
        
        #print "MESSAGE MADE!", len(Tyger.message), str(Tyger.message)
        #MessageLine(message, screen, board)
    
    object.line = object.line + len(message) + lop #Advance the object's code appropriately
    return NoAdvance, object
    
def MessageLine(message, screen, board, priority="High"): #WIP!!!!
    if (priority == "High") or (priority == "Low" and Tyger.options[3] == "False"):
        board.msg = " " + message + " "
        board.msglength = len(message)
        tempimg = pygame.Surface((8*len(board.msg), 14)) #Create a surface for the message
        tempimg.fill(Tyger.bgdarkblue)    
        for x in range(0, len(board.msg)): #Then for every character of text in that list... (chopping off the .zzt)
            tempchar = Tyger.makeimage(ord(board.msg[x]), Tyger.green, Tyger.bgblack) #Create the character
            tempimg.blit(tempchar, (x*8,0)) #Stamp it onto the surface for the line
        
        board.statcoords.append((-1, -1))
        global TextMessage
        TextMessage = tempimg
    return

def Restore(oop, current):
    while oop.find("'" + current.split(" ")[1]) != -1:
        oop = oop.replace("'" + current.split(" ")[1], ":" + current.split(" ")[1])
    return oop

def Send(current, board, object, x, y):
    #print "SEND COMMAND", current
    #Send("#all:energize", board, None, -1, -1)
    if current.split(" ")[0] == "#send":
        #print current.split(" ")[1]
        command = current.split(" ")[1] #Reduce the command to an object and a label at most
    else:
        command = current[1:]
    #print str(command) + " is the #send without a #send"
    if command.find(":") == -1: #If it's just a label then it's for this object
        command = ":" + command
        #print "Ok jumping to " + command
        SendJump(object, command)
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
                        if code[1:] == name or name == "all": #if the object and #send name match
                            SendJump(board.room[position[0]][position[1]], label, True)
                        elif name == "others" and ((position[0], position[1]) != (x, y)):
                            SendJump(board.room[position[0]][position[1]], label, True)
    return False #This lets the object that did #send continue updating its code.
    
def SendJump(object, label, extsend=False):
    #print "SENDJUMP!"
    if (object.oop == None) or (object.param2 == 1) or (object.oop.lower().find("\n" + label) == -1 and extsend == True): #No oop or a lock
        #print "Oop", object.oop
        #print "P2:", object.param2
        return                                                                                                     #or external object lacks the label
    #print "Object Jumping to label", label, extsend
    object.line = object.oop.lower().find("\n" + label) #Find the label
    #print "Object line now:", object.line
    return

def Set(flag, flags):
    for x in range(0, len(flags)-1):
        if flag == flags[x]:
            return flags #Don't add a duplicate flag
    flags.append(flag.upper()) #Add the flag if it didn't exist before
    return flags
    
def Shoot(current, x, y, board, object, health):
    dir = Elements.ParseDir(current.split(" ")[1:], x, y, board.statcoords[0][0], board.statcoords[0][1], object.xstep, object.ystep) #Get the raw direction "n", "s", "seek", etc.
    #print "I want to #shoot... " + dir
    #if board.room[x+(dir == "s")-(dir == "n")][y+(dir == "e")-(dir == "w")].name == "fake" or board.room[x+(dir == "s")-(dir == "n")][y+(dir == "e")-(dir == "w")].name == "empty":
    if ((x+(dir == "s")-(dir == "n")) < 0) or ((y+(dir == "e")-(dir == "w")) < 0) or ((x+(dir == "s")-(dir == "n")) > 24) or ((y+(dir == "e")-(dir == "w")) > 59): #Border checking
        return health
    
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
            print "S.T.A.R.S."
        board.statcoords.append((x-(dir=="n")+(dir=="s"), y-(dir=="w")+(dir=="e"))) #Make the stat
    elif board.room[x+(dir == "s")-(dir == "n")][y+(dir == "e")-(dir == "w")].name == "player": #You got shot at point blank.
        health = health - 10
    return health

def Take(ammo, torches, gems, score, health, timepassed, tcycles, ecycles, keys, current):
    if current.split(" ")[1] != "key":
        try:
            if (ammo - int(current.split(" ")[2]) >= 0) and current.split(" ")[1] == "ammo":
                ammo = ammo - int(current.split(" ")[2])
                return ammo, torches, gems, score, health, timepassed, tcycles, ecycles, keys
            if (torches - int(current.split(" ")[2]) >= 0) and current.split(" ")[1] == "torches": 
                torches = torches - int(current.split(" ")[2])
                return ammo, torches, gems, score, health, timepassed, tcycles, ecycles, keys
            if (gems - int(current.split(" ")[2]) >= 0) and current.split(" ")[1] == "gems":
                gems = gems - int(current.split(" ")[2])
                return ammo, torches, gems, score, health, timepassed, tcycles, ecycles, keys
            if (score - int(current.split(" ")[2]) >= 0) and current.split(" ")[1] == "score":
                score = score - int(current.split(" ")[2])
                return ammo, torches, gems, score, health, timepassed, tcycles, ecycles, keys
            if (health - int(current.split(" ")[2]) >= 0) and current.split(" ")[1] == "health":
                health = health - int(current.split(" ")[2])
                return ammo, torches, gems, score, health, timepassed, tcycles, ecycles, keys
            if (timepassed - int(current.split(" ")[2]) >= 0) and current.split(" ")[1] == "time":
                timepassed = timepassed - int(current.split(" ")[2])
                return ammo, torches, gems, score, health, timepassed, tcycles, ecycles, keys
            
            #Special Tyger #gives
            #if (timepassed = timepassed + (int(current.split(" ")[2]) * (current.split(" ")[1] == "seconds")))
            if (current.split(" ")[1] == "seconds"):
                timepassed = timepassed + (int(current.split(" ")[2]) * (current.split(" ")[1] == "seconds"))
                return ammo, torches, gems, score, health, timepassed, tcycles, ecycles, keys
            if (tcycles - (int(current.split(" ")[2]) * (current.split(" ")[1] == "light"))) >= 0:
                tcycles = tcycles - (int(current.split(" ")[2]) * (current.split(" ")[1] == "light"))
                return ammo, torches, gems, score, health, timepassed, tcycles, ecycles, keys
            if (ecycles - (int(current.split(" ")[2]) * (current.split(" ")[1] == "invuln"))) >= 0:
                ecycles = ecycles - (int(current.split(" ")[2]) * (current.split(" ")[1] == "invuln"))
                return ammo, torches, gems, score, health, timepassed, tcycles, ecycles, keys
        except IndexError:
            if (ecycles - 75 * (current.split(" ")[1] == "energizer")) >= 0:
                ecycles = ecycles - 75 * (current.split(" ")[1] == "energizer")
                return ammo, torches, gems, score, health, timepassed, tcycles, ecycles, keys
    elif current.split(" ")[1] == "key":
        if keys[KeyDict[current.split(" ")[2]]] == 1:
            keys[KeyDict[current.split(" ")[2]]] = 0
            return ammo, torches, gems, score, health, timepassed, tcycles, ecycles, keys
    #Take failed!
    print "Take failed!"
    return ammo, torches, gems, score, health, timepassed, tcycles, ecycles, keys
  
def TextBox(message, name, screen):
    messagebox = pygame.Surface((392, 266)) #Create the empty surface
    messagebox.fill(Tyger.bgdarkblue)
    
    #Parse the name if needed
    if name[0] != "@":
        name = " Interaction" #The space is because the first char is cut off later
    
    #Top row
    messagebox.blit(Tyger.makeimage(198, Tyger.white, Tyger.bgblack), (0,0))
    messagebox.blit(Tyger.makeimage(209, Tyger.white, Tyger.bgblack), (8,0))
    for offset in xrange(0, 45):
        messagebox.blit(Tyger.makeimage(205, Tyger.white, Tyger.bgblack), ((8*offset)+16,0))
    messagebox.blit(Tyger.makeimage(209, Tyger.white, Tyger.bgblack), (376,0))
    messagebox.blit(Tyger.makeimage(181, Tyger.white, Tyger.bgblack), (384,0))
    
    #Bottom row
    messagebox.blit(Tyger.makeimage(198, Tyger.white, Tyger.bgblack), (0,252))
    messagebox.blit(Tyger.makeimage(207, Tyger.white, Tyger.bgblack), (8,252))
    for offset in xrange(0, 45):
        messagebox.blit(Tyger.makeimage(205, Tyger.white, Tyger.bgblack), ((8*offset)+16,252))
    messagebox.blit(Tyger.makeimage(207, Tyger.white, Tyger.bgblack), (376,252))
    messagebox.blit(Tyger.makeimage(181, Tyger.white, Tyger.bgblack), (384,252))
    
    #Sidebars
    for offset in xrange(0,17):
        messagebox.blit(Tyger.makeimage(32, Tyger.white, Tyger.bgblack), (0,(14*offset)+14))
        messagebox.blit(Tyger.makeimage(179, Tyger.white, Tyger.bgblack), (8,(14*offset)+14))
        messagebox.blit(Tyger.makeimage(179, Tyger.white, Tyger.bgblack), (376,(14*offset)+14))
        messagebox.blit(Tyger.makeimage(32, Tyger.white, Tyger.bgblack), (384,(14*offset)+14))
    
    #Split between name and message
    messagebox.blit(Tyger.makeimage(198, Tyger.white, Tyger.bgblack), (8,28))
    messagebox.blit(Tyger.makeimage(181, Tyger.white, Tyger.bgblack), (376,28))
    for offset in xrange(0, 45):
        messagebox.blit(Tyger.makeimage(205, Tyger.white, Tyger.bgblack), ((8*offset)+16,28))
    
    #The little arrows to indict your line. 175, 174
    messagebox.blit(Tyger.makeimage(175, Tyger.red, Tyger.bgdarkblue), (16,140))
    messagebox.blit(Tyger.makeimage(174, Tyger.red, Tyger.bgdarkblue), (368,140))
    
    #---------------------------------------------------------------------------------------
    #Render the name
    name = name[1:] #Cut off the leading @
    if (len(name) > 1) and (len(name) % 2 != 1): #Even name, can't be centered
        name = " " + name #Just add a leading space to make it odd

    tempimg = pygame.Surface((8*len(name), 14)) #Create a surface for the name
    tempimg.fill(Tyger.bgdarkblue)    
    for x in range(0, len(name)): #Then for every character of text in the name
        tempchar = Tyger.makeimage(ord(name[x]), Tyger.yellow, Tyger.bgdarkblue) #Create the character
        tempimg.blit(tempchar, (x*8,0)) #Stamp it onto the surface for the line
    
    offset = (round(len(name) / 2.) - 1) * 8 #Calculate offset to center text
    messagebox.blit(tempimg, ((192 - offset),14))
    
    #---------------------------------------------------------------------------------------
    lines = []
    
    #Add in the starting blank lines (I am so cheating by doing it this way!)
    blank       = pygame.Surface((344, 14))
    blank.fill(Tyger.bgdarkblue)
    for _ in xrange(0, 6):
        lines.append(blank)
    
    #Render the header/footer bullets
    rawbullets  = "                                  "
    tempimg = pygame.Surface((344, 14)) #Create a surface for the name
    tempimg.fill(Tyger.bgdarkblue)    
    for x in range(0, len(rawbullets)): #Then for every character of text in that header/footer
        tempchar = Tyger.makeimage(ord(rawbullets[x]), Tyger.yellow, Tyger.bgdarkblue) #Create the character
        tempimg.blit(tempchar, (x*8,0)) #Stamp it onto the surface for the line
    lines.append(tempimg)
    #Render the lines of text
    rawlines = message.split("\n")[:-1]
    #print "RAW LINES = ", rawlines
    
    #Render the text itself
    for rawline in rawlines:
        tempimg = pygame.Surface((336, 14)) #Create a surface for the name
        tempimg.fill(Tyger.bgdarkblue)    
        
        try:
            if rawline[0] == "$": #White and centered
                offset = ((42-len(rawline)-1)/2)*8+(8*(len(rawline)%2 == 0))
                print offset
                for x in range(1, len(rawline)): #Then for every character of text in that list...
                    tempchar = Tyger.makeimage(ord(rawline[x]), Tyger.white, Tyger.bgdarkblue) #Create the character
                    tempimg.blit(tempchar, ((x*8-8)+offset,0)) #Stamp it onto the surface for the line

            elif rawline[0] == "!" and rawline[1] != "-": #Regular hypertext
                parsedline = "    " + rawline[rawline.find(";")+1:]
                for x in range(0, len(parsedline)): #Then for every character of text in that list...
                    if x != 2:
                        tempchar = Tyger.makeimage(ord(parsedline[x]), Tyger.white, Tyger.bgdarkblue) #Create the character
                    else:
                        tempchar = Tyger.makeimage(ord(parsedline[x]), Tyger.purple, Tyger.bgdarkblue) #Create the purple arrow
                    tempimg.blit(tempchar, (x*8,0)) #Stamp it onto the surface for the line
            elif rawline[0] == "!" and rawline[1] == "-": #External hypertext
                parsedline = "    " + rawline[rawline.find(";")+1:]
                for x in range(0, len(parsedline)): #Then for every character of text in that list...
                    if x != 2:
                        tempchar = Tyger.makeimage(ord(parsedline[x]), Tyger.white, Tyger.bgdarkblue) #Create the character
                    else:
                        tempchar = Tyger.makeimage(ord(parsedline[x]), Tyger.yellow, Tyger.bgdarkblue) #Create the purple arrow
                    tempimg.blit(tempchar, (x*8,0)) #Stamp it onto the surface for the line
            else: #Standard yellow text
                for x in range(0, len(rawline)): #Then for every character of text in that list...
                    tempchar = Tyger.makeimage(ord(rawline[x]), Tyger.yellow, Tyger.bgdarkblue) #Create the character
                    tempimg.blit(tempchar, (x*8,0)) #Stamp it onto the surface for the line
        except IndexError:
            0 #Ignore me.
        lines.append(tempimg) #Add the actual message
        #lines.pop() #But get rid of the extra newline it probably adds
    
    lines.append(lines[6]) #Add the header bullets as footer bullets
    #Add in the finishing blank lines
    for _ in xrange(0, 6):
        lines.append(blank)

    #---------------------------------------------------------------------------------------
    #Draw the current lines to the Messagebox
    top = 0
    
    for start in range(top, top+15):
        messagebox.blit(lines[start], (32, 42+(start*14)))
    
    #---------------------------------------------------------------------------------------
    #Draw the Messagebox
    screen.blit(messagebox, (40, 42))
    pygame.display.update()
    
    #---------------------------------------------------------------------------------------
    #Player input in window
    input = "null"
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                        
                """if event.key == K_F5: #Take screenshot
                    screenshot = "screenshots/" + world.gamename + "-" + str(scrnum) + ".png"
                    pygame.image.save(screen, screenshot)
                    scrnum = scrnum + 1
                    print("\nSaved screenshot as " + screenshot)"""
                
                #Read keys
                if event.key == K_UP or pygame.key.get_pressed()[273]:
                    input = "up"
                elif event.key == K_DOWN or pygame.key.get_pressed()[274]:
                    input = "down"
                elif event.key == K_PAGEUP:
                    input = "pgup"
                elif event.key == K_PAGEDOWN:
                    input = "pgdown"
                elif event.key == K_RETURN or pygame.key.get_pressed()[13]:
                    input = "select"
                elif event.key == K_ESCAPE or pygame.key.get_pressed()[27]:
                    return None
                else:
                    input = "null"
                    
            if event.type == KEYUP:
                input = "null"
        
        #--------------------------------------
        #Parse input
        if input == "up" or input == "down" or input =="pgup" or input == "pgdown":
            top = top - (input == "up") + (input == "down") - (14*(input=="pgup")) + (14*(input=="pgdown"))
            if top < 0:
                top = 0
            elif top+15 > len(lines):
                top = top + (input == "up") - (input == "down") + (14*(input=="pgup")) - (14*(input=="pgdown")) #Undo your move
                if input == "pgdown":
                    top = len(lines)-15
                #print "What"
            #print "Top:", top, "Top+15", top+15
            messagebox.fill(Tyger.bgdarkblue, (368, 42, 8, 98)) #Fix that last bullet ghosting
            messagebox.fill(Tyger.bgdarkblue, (368, 154, 8, 98)) #Fix that last bullet ghosting
            for start in range(0, 15):
                #print "Start:", start
                messagebox.blit(lines[top+start], (32, 42+(start*14)))
                
            screen.blit(messagebox, (40, 42))
            pygame.time.wait(100)
            pygame.display.update()
            #print "Screen drawn!"
        elif input == "select":
            #TBC. Choosing hyperlinks
            #print rawlines[top], "is the active line?"
            try:
                if rawlines[top][0] == "!" and rawlines[top][1] != "-": #if you have a regular hyperlink
                    label = rawlines[top].split(";")[0][1:] #Extract the label
                    if label == "":
                        return None
                    return ":" + label
                if rawlines[top][0] == "!" and rawlines[top][1] == "-": #if you have an external file to display
                    filename = rawlines[top].split(";")[0][2:] #Extract the filename
                    #print filename ,"will be opened"
                    try:
                        file = open(filename, "r")
                        TextBox(file.read(), filename, screen)
                        file.close()
                    except IOError:
                        print "File" + filename + "could not be opened!"
            except IndexError:
                return None
            return None #Leave
            
    
    #print "By the way, my name is...", name
    #blah = raw_input("PAUSING for textbook junk")
    return None
    
def Walk(current, x, y, board, object):
    dir = Elements.ParseDir(current.split(" ")[1:], x, y, board.statcoords[0][0], board.statcoords[0][1], object.xstep, object.ystep) #Get the raw direction "n", "s", "seek", etc.
    #object.xstep = WalkDict[dir][0]
    #object.ystep = WalkDict[dir][1]
    return WalkDict[dir][0], WalkDict[dir][1]
    
def Zap(object, board, current):
    try:
        name = current.split(":")[0]
        label = current.split(":")[1]
        #Search the board for any objects that have that name
        for position in board.statcoords: #Look at every stat on the screen
            if position != "pop": #Check the stat isn't in limbo
                if board.room[position[0]][position[1]].name == "object": #Check that you're looking at an object
                    if board.room[position[0]][position[1]].oop != None: #Check that the object has oop
                        code = board.room[position[0]][position[1]].oop.lower() #Read its name if it has one
                        code = code.split("\n")[0]
                        #print code
                        if code[1:] == name or name == "all": #if the object and #send name match
                            board.room[position[0]][position[1]].oop = board.room[position[0]][position[1]].oop.replace("\n:" + label, "\n'" + label, 1)
    except IndexError:
        name = None
        label = current
        object.oop = object.oop.replace("\n:" + label, "\n'" + label, 1)
    return object, board