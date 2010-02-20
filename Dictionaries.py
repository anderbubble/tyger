#The ID and name of every element. This will be used for acceptable #put/#change/#become statements. Yes, #put n element46 will be valid tyger zzt-oop.
IdDict = {0:"empty", 1:"edge", 2:"messenger", 3:"monitor", 4:"player", 5:"ammo", 6:"torch", 7:"gem", 8:"key", 9:"door", 10:"scroll", 11:"passage", 12:"duplicator", 13:"bomb", 14:"energizer", 15:"star", 16:"clockwise", 17:"counter", 18:"bullet", 19:"water", 20:"forest", 21:"solid", 22:"normal", 23:"breakable", 24:"boulder", 25:"sliderns", 26:"sliderew", 27:"fake", 28:"invisible", 29:"blinkwall", 30:"transporter", 31:"line", 32:"ricochet", 33:"horizray", 34:"bear", 35:"ruffian", 36:"object", 37:"slime", 38:"shark", 39:"spinninggun", 40:"pusher", 41:"lion", 42:"tiger", 43:"vertray", 44:"head", 45:"segment", 46:"element46", 47:"bluetext", 48:"greentext", 49:"cyantext", 50:"redtext", 51:"purpletext", 52:"yellowtext", 53:"whitetext"}

#The default character of every element
CharDict = {0:32, 1:32, 2:63, 3:32, 4:2, 5:132, 6:157, 7:4, 8:12, 9:10, 10:232, 11:240, 12:250, 13:11, 14:127, 15:83, 16:47, 17:47, 18:248, 19:176, 20:176, 21:219, 22:178, 23:177, 24:254, 25:18, 26:29, 27:178, 28:32, 29:206, 30:62, 31:249, 32:42, 33:205, 34:153, 35:5, 36:2, 37:42, 38:94, 39:24, 40:16, 41:234, 42:227, 43:186, 44:233, 45:79, 46:63, 47:63, 48:63, 49:63, 50:63, 51:63, 52:63, 53:63}

#Proper background colors taken by text
AltTextDict = {47:"bgdarkblue", 48:"bgdarkgreen", 49:"bgdarkcyan", 50:"bgdarkred", 51:"bgdarkpurple", 52:"bgdarkyellow", 53:"bgblack"}
TextDict = {"bluetext":"bgdarkblue", "greentext":"bgdarkgreen", "cyantext":"bgdarkcyan", "redtext":"bgdarkred", "purpletext":"bgdarkpurple", "yellowtext":"bgdarkyellow", "whitetext":"bgblack"}

#Color names to array numbers for graphics
ColorDict = {"blue":0, "green":1, "cyan":2, "red":3, "purple":4, "yellow":5, "white":6, "black":7, "darkblue":8, "darkgreen":9, "darkcyan":10, "darkred":11, "darkpurple":12, "darkyellow":13, "gray":14, "darkgray":15}
BGColorDict = {"bgblue":0, "bggreen":1, "bgcyan":2, "bgred":3, "bgpurple":4, "bgyellow":5, "bgwhite":6, "bgblack":7, "bgdarkblue":8, "bgdarkgreen":9, "bgdarkcyan":10, "bgdarkred":11, "bgdarkpurple":12, "bgdarkyellow":13, "bggray":14, "bgdarkgray":15}

#Tuples for line walls to determine which char the line wall should take
LineDict = {(0,0,0,0):249, (0,0,0,1):181, (0,0,1,0):198, (0,0,1,1):205, (0,1,0,0):210, (0,1,0,1):187, (0,1,1,0):201, (0,1,1,1):203, (1,0,0,0):208, (1,0,0,1):188, (1,0,1,0):200, (1,0,1,1):202, (1,1,0,0):186, (1,1,0,1):185, (1,1,1,0):204, (1,1,1,1):206}

#If the player tries to walk into element something happens.
#solid - Movement is stopped
#walkable - Movement is allowed
#interaction - Something is going to happen but I doubt it's implemented yet!
#DieItem - The element destroys itself and forces the player on top of it. Used for ammo/torch/gem
#InvisWall - You hit an invisible wall. What a dope.
#Push - Pushes the object if it can. Sliders and boulders.
CollisionDict = {"empty":"walkable", "edge":"ChangeBoard", "messenger":"solid", "monitor":"solid", "player":"solid", "ammo":"DieItem", "torch":"DieItem", "gem":"DieItem", "key":"DieItem", "door":"DieItem", "scroll":"interaction", "passage":"Passage", "duplicator":"solid", "bomb":"Push", "energizer":"DieItem", "star":"interaction", "clockwise":"solid", "counter":"solid", "bullet":"DieItem", "water":"interaction", "forest":"DieItem", "solid":"solid", "normal":"solid", "breakable":"solid", "boulder":"Push", "sliderns":"Push", "sliderew":"Push", "fake":"walkable", "invisible":"InvisWall", "blinkwall":"solid", "transporter":"interaction", "line":"solid", "ricochet":"solid", "horizray":"solid", "bear":"DieItem", "ruffian":"DieItem", "object":"Touch", "slime":"interaction", "shark":"interaction", "spinninggun":"solid", "pusher":"solid", "lion":"DieItem", "tiger":"DieItem", "vertray":"solid", "head":"DieItem", "segment":"DieItem", "element46":"solid", "bluetext":"solid", "greentext":"solid", "cyantext":"solid", "redtext":"solid", "purpletext":"solid", "yellowtext":"solid", "whitetext":"solid"}
#Same as above but for object behavior
ObjectDict = {"empty":"walkable", "edge":"solid", "messenger":"solid", "monitor":"solid", "player":"Push", "ammo":"Push", "torch":"solid", "gem":"Push", "key":"Push", "door":"solid", "scroll":"Push", "passage":"solid", "duplicator":"solid", "bomb":"Push", "energizer":"solid", "star":"solid", "clockwise":"solid", "counter":"solid", "bullet":"solid", "water":"solid", "forest":"solid", "solid":"solid", "normal":"solid", "breakable":"solid", "boulder":"Push", "sliderns":"Push", "sliderew":"Push", "fake":"walkable", "invisible":"solid", "blinkwall":"solid", "transporter":"solid", "line":"solid", "ricochet":"solid", "horizray":"solid", "bear":"Push", "ruffian":"Push", "object":"Push", "slime":"solid", "shark":"solid", "spinninggun":"solid", "pusher":"solid", "lion":"Push", "tiger":"Push", "vertray":"solid", "head":"solid", "segment":"solid", "element46":"solid", "bluetext":"solid", "greentext":"solid", "cyantext":"solid", "redtext":"solid", "purpletext":"solid", "yellowtext":"solid", "whitetext":"solid"}


#Noclip mode
NoClipDict = {"empty":"walkable", "edge":"solid", "messenger":"walkable", "monitor":"walkable", "player":"solid", "ammo":"DieItem", "torch":"DieItem", "gem":"DieItem", "key":"DieItem", "door":"walkable", "scroll":"interaction", "passage":"Passage", "duplicator":"walkable", "bomb":"walkable", "energizer":"DieItem", "star":"walkable", "clockwise":"walkable", "counter":"walkable", "bullet":"walkable", "water":"interaction", "forest":"DieItem", "solid":"walkable", "normal":"walkable", "breakable":"walkable", "boulder":"walkable", "sliderns":"walkable", "sliderew":"walkable", "fake":"walkable", "invisible":"walkable", "blinkwall":"walkable", "transporter":"interaction", "line":"walkable", "ricochet":"walkable", "horizray":"walkable", "bear":"walkable", "ruffian":"walkable", "object":"walkable", "slime":"interaction", "shark":"interaction", "spinninggun":"walkable", "pusher":"walkable", "lion":"walkable", "tiger":"walkable", "vertray":"walkable", "head":"walkable", "segment":"walkable", "element46":"walkable", "bluetext":"walkable", "greentext":"walkable", "cyantext":"walkable", "redtext":"walkable", "purpletext":"walkable", "yellowtext":"walkable", "whitetext":"walkable"}
ClipDict = CollisionDict

#Key color to array position. Simple enough.
KeyDict = {"blue":0, "green":1, "cyan":2, "red":3, "purple":4, "yellow":5, "white":6, "black":7, "darkblue":0, "darkgreen":1, "darkcyan":2, "darkred":3, "darkpurple":4, "darkyellow":5, "gray":6, "darkgray":7}
KeyIndexDict = {0:"Blue", 1:"Green", 2:"Cyan", 3:"Red", 4:"Purple", 5:"Yellow", 6:"White", 7:"Black"}

#Door color to array position.
DoorDict = {"blue":0, "green":1, "cyan":2, "red":3, "purple":4, "yellow":5, "white":6, "black":7, "darkblue":0, "darkgreen":1, "darkcyan":2, "darkred":3, "darkpurple":4, "darkyellow":5, "gray":6, "darkgray":7}

#Bullet reactions
BulletDict = {"empty":"walkable", "edge":"solid", "messenger":"walkable", "monitor":"solid", "player":"hurt", "ammo":"solid", "torch":"solid", "gem":"solid", "key":"solid", "door":"solid", "scroll":"solid", "passage":"solid", "duplicator":"solid", "bomb":"solid", "energizer":"solid", "star":"solid", "clockwise":"solid", "counter":"solid", "bullet":"destroy", "water":"walkable", "forest":"solid", "solid":"solid", "normal":"solid", "breakable":"destroy", "boulder":"solid", "sliderns":"solid", "sliderew":"solid", "fake":"walkable", "invisible":"solid", "blinkwall":"solid", "transporter":"solid", "line":"solid", "ricochet":"ricochet", "horizray":"solid", "bear":"destroy", "ruffian":"destroy", "object":"Shot", "slime":"solid", "shark":"solid", "spinninggun":"solid", "pusher":"solid", "lion":"destroy", "tiger":"destroy", "vertray":"solid", "head":"destroy", "segment":"destroy", "element46":"solid", "bluetext":"solid", "greentext":"solid", "cyantext":"solid", "redtext":"solid", "purpletext":"solid", "yellowtext":"solid", "whitetext":"solid"}

"""ColorDict = {"9":blue, "a":green, "b":cyan, "c":red, "d":purple, "e":yellow, "f":white, "0":black, "1":darkblue, "2":darkgreen, "3":darkcyan, "4":darkred, "5":darkpurple, "6":darkyellow, "7":gray, "8":darkgray}
BGColorDict = {"9":bgblue, "a":bggreen, "b":bgcyan, "c":bgred, "d":bgpurple, "e":bgyellow, "f":bgwhite, "0":bgblack, "1":bgdarkblue, "2":bgdarkgreen, "3":bgdarkcyan, "4":bgdarkred, "5":bgdarkpurple, "6":bgdarkyellow, "7":bggray, "8":bgdarkgray}"""
#ThingsDict = {"empty":0, "edge":0, "messenger":0, "monitor":0, "player":player(input), "lion":0}

#Pushing
PushDict = {"empty":"go", "edge":"stop", "messenger":"stop", "monitor":"stop", "player":"push", "ammo":"push", "torch":"stop", "gem":"crush", "key":"push", "door":"stop", "scroll":"push", "passage":"stop", "duplicator":"stop", "bomb":"push", "energizer":"stop", "star":"stop", "clockwise":"stop", "counter":"stop", "bullet":"stop", "water":"stop", "forest":"stop", "solid":"stop", "normal":"stop", "breakable":"stop", "boulder":"push", "sliderns":"push", "sliderew":"push", "fake":"go", "invisible":"stop", "blinkwall":"stop", "transporter":"stop", "line":"stop", "ricochet":"stop", "horizray":"stop", "bear":"crush", "ruffian":"crush", "object":"stop", "slime":"stop", "shark":"stop", "spinninggun":"stop", "pusher":"stop", "lion":"crush", "tiger":"crush", "vertray":"stop", "head":"crush", "segment":"crush", "element46":"stop", "bluetext":"stop", "greentext":"stop", "cyantext":"stop", "redtext":"stop", "purpletext":"stop", "yellowtext":"stop", "whitetext":"stop"}

#Bombing
BombDict = {"empty":"boom", "edge":"no", "messenger":"no", "monitor":"no", "player":"hurt", "ammo":"no", "torch":"no", "gem":"boom", "key":"no", "door":"no", "scroll":"no", "passage":"no", "duplicator":"no", "bomb":"no", "energizer":"no", "star":"boom", "clockwise":"no", "counter":"no", "bullet":"boom", "water":"no", "forest":"no", "solid":"no", "normal":"no", "breakable":"boom", "boulder":"no", "sliderns":"no", "sliderew":"no", "fake":"no", "invisible":"no", "blinkwall":"no", "transporter":"no", "line":"no", "ricochet":"no", "horizray":"no", "bear":"boom", "ruffian":"boom", "object":"bombed", "slime":"no", "shark":"boom", "spinninggun":"no", "pusher":"no", "lion":"boom", "tiger":"boom", "vertray":"no", "head":"boom", "segment":"boom", "element46":"no", "bluetext":"no", "greentext":"no", "cyantext":"no", "redtext":"no", "purpletext":"no", "yellowtext":"no", "whitetext":"no"}
#Bomb radius
BoomDict = {
(4,7):"Ignore", (4,6):"Ignore", (4,5):"Ignore", (4,4):"Boom", (4,3):"Boom", (4,2):"Boom", (4,1):"Boom", (4,0):"Boom", 
(3,7):"Ignore", (3,6):"Ignore", (3,5):"Boom", (3,4):"Boom", (3,3):"Boom", (3,2):"Boom", (3,1):"Boom", (3,0):"Boom", 
(2,7):"Ignore", (2,6):"Boom", (2,5):"Boom", (2,4):"Boom", (2,3):"Boom", (2,2):"Boom", (2,1):"Boom", (2,0):"Boom", 
(1,7):"Ignore", (1,6):"Boom", (1,5):"Boom", (1,4):"Boom", (1,3):"Boom", (1,2):"Boom", (1,1):"Boom", (1,0):"Boom",
(0,7):"Boom", (0,6):"Boom", (0,5):"Boom", (0,4):"Boom", (0,3):"Boom", (0,2):"Boom", (0,1):"Boom", (0,0):"Boom"}

#Torch Light
LightDict = {
(4,7):"Dark", (4,6):"Dark", (4,5):"Dark", (4,4):"Light", (4,3):"Light", (4,2):"Light", (4,1):"Light", (4,0):"Light", 
(3,7):"Dark", (3,6):"Dark", (3,5):"Light", (3,4):"Light", (3,3):"Light", (3,2):"Light", (3,1):"Light", (3,0):"Light", 
(2,7):"Dark", (2,6):"Light", (2,5):"Light", (2,4):"Light", (2,3):"Light", (2,2):"Light", (2,1):"Light", (2,0):"Light", 
(1,7):"Dark", (1,6):"Light", (1,5):"Light", (1,4):"Light", (1,3):"Light", (1,2):"Light", (1,1):"Light", (1,0):"Light",
(0,7):"Light", (0,6):"Light", (0,5):"Light", (0,4):"Light", (0,3):"Light", (0,2):"Light", (0,1):"Light", (0,0):"Light"}


#Movement ZZT-OOP related dictionaries
#Walking directions to x/y-steps
WalkDict = {"n":(0,-1), "s":(0,1), "e":(1,0), "w":(-1,0), "i":(0,0)}
#It's like WalkDict reversed!
FlowDict = {(0,-1):"n", (0,1):"s", (1,0):"e", (-1,0):"w", (0,0):"i"}
CwDict = {"n":"e", "s":"w", "e":"s", "w":"n", "i":"i"}
CcwDict = {"n":"w", "s":"e", "e":"n", "w":"s", "i":"i"}
OppDict = {"n":"s", "s":"n", "e":"w", "w":"e", "i":"i"}
RndpDict = {"n":["e", "w"], "s":["e", "w"], "e":["n", "s"], "w":["n", "s"], "i":["i"], "rndns":["e", "w"], "rndne":["n", "s", "e", "w"]}
IsDirDict = {"n":True, "s":True, "e":True, "w":True, "i":True, "seek":True, "flow":True}

#Bears have restrictions.
BearDict = {"empty":"walkable", "edge":"solid", "messenger":"solid", "monitor":"solid", "player":"hurt", "ammo":"solid", "torch":"solid", "gem":"solid", "key":"solid", "door":"solid", "scroll":"solid", "passage":"solid", "duplicator":"solid", "bomb":"solid", "energizer":"solid", "star":"solid", "clockwise":"solid", "counter":"solid", "bullet":"solid", "water":"solid", "forest":"solid", "solid":"solid", "normal":"solid", "breakable":"destroy", "boulder":"solid", "sliderns":"solid", "sliderew":"solid", "fake":"walkable", "invisible":"solid", "blinkwall":"solid", "transporter":"solid", "line":"solid", "ricochet":"solid", "horizray":"solid", "bear":"solid", "ruffian":"solid", "object":"solid", "slime":"solid", "shark":"solid", "spinninggun":"solid", "pusher":"solid", "lion":"solid", "tiger":"solid", "vertray":"solid", "head":"solid", "segment":"solid", "element46":"solid", "bluetext":"solid", "greentext":"solid", "cyantext":"solid", "redtext":"solid", "purpletext":"solid", "yellowtext":"solid", "whitetext":"solid"}
