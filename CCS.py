#Custom Control System - Tyger Edition

#USAGE-
#from CCS import *
#controls, scancodes = CCSInit() #Set up control dictionary
#input = GetInput(controls, scancodes) #Looks for input that's contained in said dictionary
#input = GetMultiInput(controls, scancodes) #Returns all pressed input keys
import os

import pygame
#from pygame.locals import *
#from sys import exit

def CCSInit(file="keys.cfg"):
    controllist = open(file, "r")
    key = []
    function = []
    
    #Read in controls
    for line in controllist:
        if line != "\n":
            key.append(line.split("\t")[1])
            function.append(line.split("\t")[2][:-1])
        else:
            break
    
    print key
    print function
    
    #Assemble dictionary
    dictionary = {}
    for x in xrange(0, len(function)):
        dictionary[key[x]] = function[x]
    return dictionary, key

def GetInput(controls, activebuttons):
    input = "null"
    
    for key in activebuttons:
        if pygame.key.get_pressed()[int(key)]:
            return controls[key]
    return "null"
    
def GetMultiInput(controls, activebuttons):
    input = []
    
    for key in activebuttons:
        if pygame.key.get_pressed()[int(key)]:
            input.append(controls[key])
            
    if len(input) == 0:
        return None
    else:
        return input