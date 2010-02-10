from Dictionaries import *
import Tyger
import Elements

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
    
def Cycle(cycle, current):
    try:
        cycle = int(cycle)
        if (cycle >= 0) and (cycle <= 255): #Make sure the cycle's range is good
            print "Setting cycle to", cycle
            return cycle
        else:
            return current
    except ValueError: #Invalid cycle, return the old cycle
        return current
    
def Die(board, x, y):
    element = Tyger.Spawn("empty", 32, Tyger.black, Tyger.bgblack, (x, y), 0, 0, 0, 0, 0, 0)
    Elements.DestroyStat(board, x, y)
    return element
    
def Give(ammo, torches, gems, score, health, timepassed, tcycles, ecycles, keys, current):
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
        except ValueError:
            return ammo, torches, gems, score, health, timepassed, tcycles, ecycles, keys
    elif current.split(" ")[1] == "key":
        keys[KeyDict[current.split(" ")[2]]] = 1
    return ammo, torches, gems, score, health, timepassed, tcycles, ecycles, keys

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
        print "OK I MOVED!"
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
        print "Current is..." + str(current) + " ... " + str(command)
        
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
                print "Flaggot"
                break
        print "Fla"
    
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
        print "Line is:", object.line
    return NoAdvance, Moved, object

def Restore(oop, current):
    while oop.find("'" + current.split(" ")[1]) != -1:
        oop = oop.replace("'" + current.split(" ")[1], ":" + current.split(" ")[1])
    return oop

def Send(current, board, object):
    #print "SEND COMMAND", current
        
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
                        if code[1:] == name: #if the object and #send name match
                            SendJump(board.room[position[0]][position[1]], label, True)
    return False #This lets the object that did #send continue updating its code.
    
def SendJump(object, label, extsend=False):
    if (object.oop == None) or (object.param2 == 1) or (object.oop.lower().find(label) == -1 and extsend == True): #No oop or a lock
        return                                                                                                     #or external object lacks the label
    #print "Jumping to label", label
    object.line = object.oop.lower().find(label) #Find the label
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
    
def Walk(current, x, y, board, object):
    dir = Elements.ParseDir(current.split(" ")[1:], x, y, board.statcoords[0][0], board.statcoords[0][1], object.xstep, object.ystep) #Get the raw direction "n", "s", "seek", etc.
    #object.xstep = WalkDict[dir][0]
    #object.ystep = WalkDict[dir][1]
    return WalkDict[dir][0], WalkDict[dir][1]