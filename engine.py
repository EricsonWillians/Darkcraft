#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================
Darkcraft - v1.0 Alpha.
Copyright (C) <2014>  <Ericson Willians.>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

====================================================================
Engine written by Ericson Willians, a brazilian composer and programmer.

CONTACT: ericsonwrp@gmail.com
AS A COMPOSER: https://soundcloud.com/r-p-ericson-willians
YOUTUBE CHANNEL: http://www.youtube.com/user/poisonewein

====================================================================
"""

__author__ = 'EricsonWillians'

import sys
import os
from collections import Sequence
from itertools import product
import collections
import copy
import pythun # My grid-based engine.
import functions
from random import randint
import pygame

# = CFG Area = <<<

pygame.display.set_caption("Darkcraft 1.0.")
pygame.init()

DONE = False
clock = pygame.time.Clock()

res = pythun.Global.RESOLUTIONS.get("XGA")
screen = pygame.display.set_mode(res)
screen.set_alpha(None)

def loadImage(path,name,colorkey=None):

    fullname = os.path.join(path, name)
    try:
        i = pygame.image.load(fullname)
    except error, message:
        print "Cannot load image:", name
        raise SystemExit, message
    if ".png" not in name:
        i = i.convert()
    else:
        i = pygame.Surface.convert_alpha(i)
    if colorkey is not None:
        if colorkey is -1:
            colorkey = i.get_at((0,0))
        i.set_colorkey(colorkey,RLEACCEL)
    return i

def loadSound(path,name):

    """
    Same as the above function.
    """

    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join(path,name)
    try:
        sound = mixer.Sound(fullname)
    except error, message:
        print "Cannot load sound:", name
        raise SystemExit, message
    return sound

def loadDefaultFont(size):

    """
    A function to load the default system font (Good for cross-platform games).
    """

    try:
        f = pygame.font.Font(None,size)
    except error, message:
        print "Cannot load the default font"
        raise SystemExit, message
    return f

def loadCustomFont(path,name,size):

    """
    A function to load a custom font from a file.
    """

    fullname = os.path.join(path,name)
    f = pygame.font.Font(fullname,size)
    return f

def loadSystemFont(name, size):

    """
    A function to load a specific system font (Not good for cross-platform games).
    """

    try:
        f = pygame.font.SysFont(name,size)
    except error, message:
        print "Cannot load font: ", name
        raise SystemExit, message
    return f

def getSystemFonts():

    return font.get_fonts()

# = Game Area = <<<

gameScreen = "GAME"
gameGrid = pythun.Grid((16,16,64,48))
interfaceGrid = pythun.Grid((8,8,128,96))
brickWidth = gameGrid.tileWidth
brickHeight = gameGrid.tileHeight
interfaceWidth = res[0]/8
interfaceHeight = res[1]/8
language = "EN"
screenPositions = [(i*brickWidth,j*brickHeight) for i,j in product(range(16), repeat=2)] # In-game.

def cFS(textSize): # Custom Font Size

    return loadCustomFont("GFX","Kingthings_Petrock.ttf",textSize)

def gT(en,pt,c,textSize,adjust=[0,0]): # Generate Text Procedure.

    if language == "EN":
        t = cFS(textSize).render(en[0],1,c)
        screen.blit(pygame.transform.scale(t,(t.get_width(),t.get_height())),
                    (gameGrid.getX(en[1])-adjust[0],gameGrid.getY(en[2])-adjust[1]))
    elif language == "PT":
        t = cFS(textSize).render(pt[0],1,c)
        screen.blit(pygame.transform.scale(t,(t.get_width(),t.get_height())),
                    (gameGrid.getX(pt[1])-adjust[0],gameGrid.getY(pt[2])-adjust[1]))

def gPT(en,pt,c,textSize,adjust=[0,0]): # Generate Pure-Pos Text Procedure.

    if language == "EN":
        t = loadDefaultFont(textSize).render(en[0],1,c)
        screen.blit(pygame.transform.scale(t,(t.get_width(),t.get_height())),
                    (en[1]-adjust[0],en[2]-adjust[1]))
    elif language == "PT":
        t = loadDefaultFont(textSize).render(pt[0],1,c)
        screen.blit(pygame.transform.scale(t,(t.get_width(),t.get_height())),
                    (pt[1]-adjust[0],pt[2]-adjust[1]))

def gIS(path,name,x,y): # Generate Image Surface Procedure.

    s = loadImage(path,name)
    screen.blit(transform.scale(s,(brickWidth,brickHeight)),(x,y))

def cGIS(sur,path,name,x,y,w,h): # Custom 'Generate Image Surface' Procedure.

    s = loadImage(path,name)
    sur.blit(pygame.transform.scale(s,(w,h)),(x,y))

def cW(r1,r2): # Collide With

    if not ((((r1.x + brickWidth) >= r2.x) and r1.x <= ((r2.x + brickWidth))) and (((r1.y + brickHeight) >= r2.y) and (r1.y <= (r2.y + brickHeight)))):
        return True
    else:
        return False

dungeonSize = 8
dungeon = {(i, j): pythun.GridMap(gameGrid) for i, j in product(range(dungeonSize), repeat=2)}
currentMaze = (randint(0,dungeonSize-1),randint(0,dungeonSize-1))
lOR = 10 # Level of Randomness.

class Info(collections.MutableMapping):

    def __init__(self,*args,**kwargs):

        self.store = dict()
        self.update(dict(*args, **kwargs))

    def __getitem__(self,key):

        return self.store[self.__keytransform__(key)]

    def __setitem__(self,key,value):

        self.store[self.__keytransform__(key)] = value

    def __delitem__(self,key):

        del self.store[self.__keytransform__(key)]

    def __iter__(self):

        return iter(self.store)

    def __len__(self):

        return len(self.store)

    def __keytransform__(self,key):

        return key

class Entity():

    def __init__(self,info):

        self.keyPositions = [[x for x in range(16)], [x for x in range(16)]]
        self.xGamePositions = dict(zip([x for x in self.keyPositions[0]], [x for x in range(0,1024,brickWidth)]))
        self.yGamePositions = dict(zip([x for x in self.keyPositions[1]], [x for x in range(0,768,brickHeight)]))
        self.xInterfacePositions = dict(zip([x for x in self.keyPositions[0]], [x for x in range(0,1024,interfaceWidth)]))
        self.yInterfacePositions = dict(zip([x for x in self.keyPositions[1]], [x for x in range(0,768, interfaceHeight)]))

        self.info = info

    def getGameX(self,pos):

        if self.xGamePositions.get(pos) != None: # Avoiding bugs.
            return self.xGamePositions.get(pos)
        else:
            return 0

    def getGameY(self,pos):

        if self.yGamePositions.get(pos) != None: # Avoiding bugs.
            return self.yGamePositions.get(pos)
        else:
            return 0

    def getInterfaceX(self,pos):

        if self.xInterfacePositions.get(pos) != None: # Avoiding bugs.
            return self.xInterfacePositions.get(pos)
        else:
            return 0

    def getInterfaceY(self,pos):

        if self.yInterfacePositions.get(pos) != None: # Avoiding bugs.
            return self.yInterfacePositions.get(pos)
        else:
            return 0

class ImageEntity(Entity):

    def __init__(self,path,filename,x,y,sizeType="INGAME",info=Info()):
        Entity.__init__(self,info)

        self.path = path
        self.filename = filename
        if sizeType == "INGAME":
            self.x = self.getGameX(x)
            self.y = self.getGameY(y)
        if sizeType == "INTERFACE":
            self.x = self.getInterfaceX(x)
            self.y = self.getInterfaceY(y)
        self.s = loadImage(self.path,self.filename)

    def draw(self,sizeType):

        if sizeType == "INGAME":
            screen.blit(pygame.transform.scale(self.s,(brickWidth,brickHeight)),(self.x,self.y))
        elif sizeType == "INTERFACE":
            screen.blit(pygame.transform.scale(self.s,(interfaceWidth,interfaceHeight)),(self.x,self.y))

class Wall(ImageEntity):

    def __init__(self,path,filename,x,y):

        self.path = path
        self.filename = filename
        self.x = x
        self.y = y

        ImageEntity.__init__(self,path,filename,self.x,self.y)

def gD(): # Generate Dungeon

    length = 5

    for d in dungeon:
        for k in range(brickWidth/4):
            for l in range(brickWidth/4):
                if randint(0,lOR*2) == 0:
                    for m in range(length):
                        try:
                            dungeon[d][(l+m,k)]["wallEntity"] = Wall("GFX","brick.jpg",l+m,k)
                        except:
                            pass
                elif randint(0,lOR*2) == 1:
                    for m in range(length):
                        try:
                            dungeon[d][(l,k+m)]["wallEntity"] = Wall("GFX","brick.jpg",l,k+m)
                        except:
                            pass

def dCD(): # Draw Current Dungeon

    map((lambda x: dungeon[currentMaze][x]["wallEntity"].draw("INGAME")),[x for x in dungeon[currentMaze] if "wallEntity" in dungeon[currentMaze][x]])

    if "wallEntity" in [x for x in dungeon[currentMaze][(0,0)]]:
        dungeon[currentMaze][(0,0)]["wallEntity"].draw("INGAME")
    if pygame.key.get_pressed()[pygame.K_F12]:
        for wall in dungeon[currentMaze]:
            gPT([str((wall[0]*brickWidth,wall[1]*brickHeight)),wall[0]*brickWidth,wall[1]*brickHeight],
                [str((wall[0]*brickWidth,wall[1]*brickHeight)),wall[0]*brickWidth,wall[1]*brickHeight],(0,255,0),16)

def gG(source): # Generate Ground Image

    groundSurface = pygame.Surface((res[0],res[1]))
    map((lambda x: cGIS(groundSurface,"GFX",source,x[0],x[1],brickWidth,brickHeight)),[x for x in screenPositions])

    return groundSurface

def gIBGI(source): # Generate Interface Background Image

    iSurface = pygame.Surface((res[0],res[1]))
    map((lambda x: cGIS(iSurface,"GFX",source,x[0],x[1],interfaceWidth,interfaceHeight)),[x for x in [(i*interfaceWidth,j*interfaceHeight) for i,j in product(range(8), repeat=2)]])

    return iSurface

ground = gG("ground.jpg") # The ground can't be generated at each frame. It really screws with the FPS.

class FontEntity():

    def __init__(self,displayCharacter,x,y,c):

        self.displayCharacter = displayCharacter
        self.x = x
        self.y = y
        self.c = c

        if language == "EN":
            self.s = cFS(64).render(self.displayCharacter[0],1,c)
        elif language == "PT":
            self.s = cFS(64).render(self.displayCharacter[1],1,c)

    def draw(self):

        screen.blit(transform.scale(self.s,(brickWidth,brickHeight)),(self.x,self.y))

class Item(ImageEntity):

    def __init__(self,filename,x,y):
        ImageEntity.__init__(self,"GFX/Items",filename,x,y)

ew0 = Item("ew0.png",0,0)



class SelectionCursor(ImageEntity):

    def __init__(self,path,filename,x,y):
        ImageEntity.__init__(self,path,filename,x,y)

    def move(self):

        for i in range(0,16*brickHeight,brickHeight):
            for j in range(0,16*brickWidth,brickWidth):
                if (((pygame.mouse.get_pos()[0] > j) and (pygame.mouse.get_pos()[0] < (j + brickWidth)) and
                     (pygame.mouse.get_pos()[1] > i) and (pygame.mouse.get_pos()[1] < (i + brickHeight)))):
                    self.x = j
                    self.y = i

class InterfaceSelectionCursor(ImageEntity):

    def __init__(self,path,filename,x,y):
        ImageEntity.__init__(self,path,filename,x,y)

    def move(self):

        for i in range(0,8*interfaceHeight,interfaceHeight):
            for j in range(0,8*interfaceWidth,interfaceWidth):
                if (((pygame.mouse.get_pos()[0] > j) and (pygame.mouse.get_pos()[0] < (j + interfaceWidth)) and
                     (pygame.mouse.get_pos()[1] > i) and (pygame.mouse.get_pos()[1] < (i + interfaceHeight)))):
                    self.x = j
                    self.y = i

class Inventory(ImageEntity):

    def __init__(self,filename):
        ImageEntity.__init__(self,"GFX",filename,0,0)

        self.interface = gIBGI(filename)
        self.cursor = InterfaceSelectionCursor("GFX","selectionCursor.png",0,0)
        self.storage = pythun.GridMap(interfaceGrid)
        for slot in self.storage:
            self.storage[slot] = [0,"No hotkey",False]
        ew0InitialPos = (randint(0,7),randint(0,7))
        ew0.x = self.getInterfaceX(ew0InitialPos[0])
        ew0.y = self.getInterfaceY(ew0InitialPos[1])
        self.storage[(ew0InitialPos[0],ew0InitialPos[1])][0] = ew0

        self.isItemSelected = False
        self.slotHolder = None
        self.slotToBeErased = None

    def watchForPositionalMouseRequests(self):

        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == True:
                if self.isItemSelected == False:
                    for slot in self.storage:
                        if (self.getInterfaceX(slot[0]),self.getInterfaceY(slot[1])) == (self.cursor.x,self.cursor.y):
                            if isinstance(self.storage[slot][0],Item):
                                self.isItemSelected = True
                                if self.slotHolder is None:
                                    self.storage[slot][0].x = self.cursor.x
                                    self.storage[slot][0].y = self.cursor.y
                                    self.slotHolder = self.storage[slot][0]
                                    self.slotToBeErased = slot

            if e.type == pygame.MOUSEBUTTONUP and pygame.mouse.get_pressed()[0] == False:
                if self.isItemSelected == True:
                    for slot in list(self.storage):
                        if (self.getInterfaceX(slot[0]),self.getInterfaceY(slot[1])) == (self.cursor.x,self.cursor.y):
                            if self.slotHolder is not None:
                                self.isItemSelected = False
                                self.storage[slot][0] = self.slotHolder
                                self.slotHolder = None
                                if self.slotToBeErased is not None:
                                    if slot != self.slotToBeErased:
                                        self.storage[self.slotToBeErased][0] = 0
                                        self.slotToBeErased = None

    def draw(self):

        screen.blit(self.interface,(0,0))
        self.cursor.draw("INTERFACE")
        self.cursor.move()
        for slot in self.storage:
            try:
                if isinstance(self.storage[slot][0],Item):
                    if self.isItemSelected == True:
                        self.storage[slot][0].x = self.cursor.x
                        self.storage[slot][0].y = self.cursor.y
                    if self.storage[slot][2] == True:
                        ImageEntity("GFX","selectedItem.jpg",slot[0],slot[1],"INTERFACE").draw("INTERFACE")
                    self.storage[slot][0].draw("INTERFACE")
                for n in range(1,10,1):
                    if str(n) in self.storage[slot][1]:
                        gPT([str(n),self.storage[slot][0].x,self.storage[slot][0].y],
                            [str(n),self.storage[slot][0].x,self.storage[slot][0].y],(255,255,255),32)
            except:
                pass
        if self.slotHolder is not None:
            self.slotHolder.draw("INTERFACE")

    def watchForHotkeyAssignments(self):

        for slot in self.storage:
            if (self.getInterfaceX(slot[0]),self.getInterfaceY(slot[1])) == (self.cursor.x,self.cursor.y):
                if isinstance(self.storage[slot][0],Item):
                    if (pygame.key.get_pressed()[pygame.K_LCTRL] and (pygame.key.get_pressed()[pygame.K_0] or pygame.key.get_pressed()[pygame.K_KP0])):
                            self.storage[slot][1] = "No hotkey"
                    if (pygame.key.get_pressed()[pygame.K_LCTRL] and (pygame.key.get_pressed()[pygame.K_1] or pygame.key.get_pressed()[pygame.K_KP1])):
                            self.storage[slot][1] = "Hotkey 1"
                    if (pygame.key.get_pressed()[pygame.K_LCTRL] and (pygame.key.get_pressed()[pygame.K_2] or pygame.key.get_pressed()[pygame.K_KP2])):
                            self.storage[slot][1] = "Hotkey 2"
                    if (pygame.key.get_pressed()[pygame.K_LCTRL] and (pygame.key.get_pressed()[pygame.K_3] or pygame.key.get_pressed()[pygame.K_KP3])):
                            self.storage[slot][1] = "Hotkey 3"
                    if (pygame.key.get_pressed()[pygame.K_LCTRL] and (pygame.key.get_pressed()[pygame.K_4] or pygame.key.get_pressed()[pygame.K_KP4])):
                            self.storage[slot][1] = "Hotkey 4"
                    if (pygame.key.get_pressed()[pygame.K_LCTRL] and (pygame.key.get_pressed()[pygame.K_5] or pygame.key.get_pressed()[pygame.K_KP5])):
                            self.storage[slot][1] = "Hotkey 5"
                    if (pygame.key.get_pressed()[pygame.K_LCTRL] and (pygame.key.get_pressed()[pygame.K_6] or pygame.key.get_pressed()[pygame.K_KP6])):
                            self.storage[slot][1] = "Hotkey 6"
                    if (pygame.key.get_pressed()[pygame.K_LCTRL] and (pygame.key.get_pressed()[pygame.K_7] or pygame.key.get_pressed()[pygame.K_KP7])):
                            self.storage[slot][1] = "Hotkey 7"
                    if (pygame.key.get_pressed()[pygame.K_LCTRL] and (pygame.key.get_pressed()[pygame.K_8] or pygame.key.get_pressed()[pygame.K_KP8])):
                            self.storage[slot][1] = "Hotkey 8"
                    if (pygame.key.get_pressed()[pygame.K_LCTRL] and (pygame.key.get_pressed()[pygame.K_9] or pygame.key.get_pressed()[pygame.K_KP9])):
                            self.storage[slot][1] = "Hotkey 9"

    def watchForHotkeys(self):

        for slot in self.storage:
            if (self.getInterfaceX(slot[0]),self.getInterfaceY(slot[1])) == (self.cursor.x,self.cursor.y):
                if isinstance(self.storage[slot][0],Item):
                    if self.storage[slot][1] == "Hotkey 1":
                        if (pygame.key.get_pressed()[pygame.K_1] or pygame.key.get_pressed()[pygame.K_KP1]):
                            self.storage[slot][2] = True
                            for sl in self.storage:
                                if isinstance(self.storage[slot][0],Item):
                                    if sl != slot:
                                        if self.storage[sl][2] == True:
                                            self.storage[sl][2] = False
                                            break
                        elif (pygame.key.get_pressed()[pygame.K_2] or pygame.key.get_pressed()[pygame.K_KP2] or
                              pygame.key.get_pressed()[pygame.K_3] or pygame.key.get_pressed()[pygame.K_KP3] or
                              pygame.key.get_pressed()[pygame.K_4] or pygame.key.get_pressed()[pygame.K_KP4] or
                              pygame.key.get_pressed()[pygame.K_5] or pygame.key.get_pressed()[pygame.K_KP5] or
                              pygame.key.get_pressed()[pygame.K_6] or pygame.key.get_pressed()[pygame.K_KP6] or
                              pygame.key.get_pressed()[pygame.K_7] or pygame.key.get_pressed()[pygame.K_KP7] or
                              pygame.key.get_pressed()[pygame.K_8] or pygame.key.get_pressed()[pygame.K_KP8] or
                              pygame.key.get_pressed()[pygame.K_9] or pygame.key.get_pressed()[pygame.K_KP9]):
                            self.storage[slot][2] = False
                    if self.storage[slot][1] == "Hotkey 2":
                        if (pygame.key.get_pressed()[pygame.K_2] or pygame.key.get_pressed()[pygame.K_KP2]):
                            self.storage[slot][2] = True
                            for sl in self.storage:
                                if isinstance(self.storage[slot][0],Item):
                                    if sl != slot:
                                        if self.storage[sl][2] == True:
                                            self.storage[sl][2] = False
                                            break
                        elif (pygame.key.get_pressed()[pygame.K_1] or pygame.key.get_pressed()[pygame.K_KP1] or
                              pygame.key.get_pressed()[pygame.K_3] or pygame.key.get_pressed()[pygame.K_KP3] or
                              pygame.key.get_pressed()[pygame.K_4] or pygame.key.get_pressed()[pygame.K_KP4] or
                              pygame.key.get_pressed()[pygame.K_5] or pygame.key.get_pressed()[pygame.K_KP5] or
                              pygame.key.get_pressed()[pygame.K_6] or pygame.key.get_pressed()[pygame.K_KP6] or
                              pygame.key.get_pressed()[pygame.K_7] or pygame.key.get_pressed()[pygame.K_KP7] or
                              pygame.key.get_pressed()[pygame.K_8] or pygame.key.get_pressed()[pygame.K_KP8] or
                              pygame.key.get_pressed()[pygame.K_9] or pygame.key.get_pressed()[pygame.K_KP9]):
                            self.storage[slot][2] = False
                    if self.storage[slot][1] == "Hotkey 3":
                        if (pygame.key.get_pressed()[pygame.K_3] or pygame.key.get_pressed()[pygame.K_KP3]):
                            self.storage[slot][2] = True
                            for sl in self.storage:
                                if isinstance(self.storage[slot][0],Item):
                                    if sl != slot:
                                        if self.storage[sl][2] == True:
                                            self.storage[sl][2] = False
                                            break
                        elif (pygame.key.get_pressed()[pygame.K_2] or pygame.key.get_pressed()[pygame.K_KP2] or
                              pygame.key.get_pressed()[pygame.K_1] or pygame.key.get_pressed()[pygame.K_KP1] or
                              pygame.key.get_pressed()[pygame.K_4] or pygame.key.get_pressed()[pygame.K_KP4] or
                              pygame.key.get_pressed()[pygame.K_5] or pygame.key.get_pressed()[pygame.K_KP5] or
                              pygame.key.get_pressed()[pygame.K_6] or pygame.key.get_pressed()[pygame.K_KP6] or
                              pygame.key.get_pressed()[pygame.K_7] or pygame.key.get_pressed()[pygame.K_KP7] or
                              pygame.key.get_pressed()[pygame.K_8] or pygame.key.get_pressed()[pygame.K_KP8] or
                              pygame.key.get_pressed()[pygame.K_9] or pygame.key.get_pressed()[pygame.K_KP9]):
                            self.storage[slot][2] = False
                    if self.storage[slot][1] == "Hotkey 4":
                        if (pygame.key.get_pressed()[pygame.K_4] or pygame.key.get_pressed()[pygame.K_KP4]):
                            self.storage[slot][2] = True
                            for sl in self.storage:
                                if isinstance(self.storage[slot][0],Item):
                                    if sl != slot:
                                        if self.storage[sl][2] == True:
                                            self.storage[sl][2] = False
                                            break
                        elif (pygame.key.get_pressed()[pygame.K_2] or pygame.key.get_pressed()[pygame.K_KP2] or
                              pygame.key.get_pressed()[pygame.K_3] or pygame.key.get_pressed()[pygame.K_KP3] or
                              pygame.key.get_pressed()[pygame.K_1] or pygame.key.get_pressed()[pygame.K_KP1] or
                              pygame.key.get_pressed()[pygame.K_5] or pygame.key.get_pressed()[pygame.K_KP5] or
                              pygame.key.get_pressed()[pygame.K_6] or pygame.key.get_pressed()[pygame.K_KP6] or
                              pygame.key.get_pressed()[pygame.K_7] or pygame.key.get_pressed()[pygame.K_KP7] or
                              pygame.key.get_pressed()[pygame.K_8] or pygame.key.get_pressed()[pygame.K_KP8] or
                              pygame.key.get_pressed()[pygame.K_9] or pygame.key.get_pressed()[pygame.K_KP9]):
                            self.storage[slot][2] = False
                    if self.storage[slot][1] == "Hotkey 5":
                        if (pygame.key.get_pressed()[pygame.K_5] or pygame.key.get_pressed()[pygame.K_KP5]):
                            self.storage[slot][2] = True
                            for sl in self.storage:
                                if isinstance(self.storage[slot][0],Item):
                                    if sl != slot:
                                        if self.storage[sl][2] == True:
                                            self.storage[sl][2] = False
                                            break
                        elif (pygame.key.get_pressed()[pygame.K_2] or pygame.key.get_pressed()[pygame.K_KP2] or
                              pygame.key.get_pressed()[pygame.K_3] or pygame.key.get_pressed()[pygame.K_KP3] or
                              pygame.key.get_pressed()[pygame.K_4] or pygame.key.get_pressed()[pygame.K_KP4] or
                              pygame.key.get_pressed()[pygame.K_1] or pygame.key.get_pressed()[pygame.K_KP1] or
                              pygame.key.get_pressed()[pygame.K_6] or pygame.key.get_pressed()[pygame.K_KP6] or
                              pygame.key.get_pressed()[pygame.K_7] or pygame.key.get_pressed()[pygame.K_KP7] or
                              pygame.key.get_pressed()[pygame.K_8] or pygame.key.get_pressed()[pygame.K_KP8] or
                              pygame.key.get_pressed()[pygame.K_9] or pygame.key.get_pressed()[pygame.K_KP9]):
                            self.storage[slot][2] = False
                    if self.storage[slot][1] == "Hotkey 6":
                        if (pygame.key.get_pressed()[pygame.K_6] or pygame.key.get_pressed()[pygame.K_KP6]):
                            self.storage[slot][2] = True
                            for sl in self.storage:
                                if isinstance(self.storage[slot][0],Item):
                                    if sl != slot:
                                        if self.storage[sl][2] == True:
                                            self.storage[sl][2] = False
                                            break
                        elif (pygame.key.get_pressed()[pygame.K_2] or pygame.key.get_pressed()[pygame.K_KP2] or
                              pygame.key.get_pressed()[pygame.K_3] or pygame.key.get_pressed()[pygame.K_KP3] or
                              pygame.key.get_pressed()[pygame.K_4] or pygame.key.get_pressed()[pygame.K_KP4] or
                              pygame.key.get_pressed()[pygame.K_5] or pygame.key.get_pressed()[pygame.K_KP5] or
                              pygame.key.get_pressed()[pygame.K_1] or pygame.key.get_pressed()[pygame.K_KP1] or
                              pygame.key.get_pressed()[pygame.K_7] or pygame.key.get_pressed()[pygame.K_KP7] or
                              pygame.key.get_pressed()[pygame.K_8] or pygame.key.get_pressed()[pygame.K_KP8] or
                              pygame.key.get_pressed()[pygame.K_9] or pygame.key.get_pressed()[pygame.K_KP9]):
                            self.storage[slot][2] = False
                    if self.storage[slot][1] == "Hotkey 7":
                        if (pygame.key.get_pressed()[pygame.K_7] or pygame.key.get_pressed()[pygame.K_KP7]):
                            self.storage[slot][2] = True
                            for sl in self.storage:
                                if isinstance(self.storage[slot][0],Item):
                                    if sl != slot:
                                        if self.storage[sl][2] == True:
                                            self.storage[sl][2] = False
                                            break
                        elif (pygame.key.get_pressed()[pygame.K_2] or pygame.key.get_pressed()[pygame.K_KP2] or
                              pygame.key.get_pressed()[pygame.K_3] or pygame.key.get_pressed()[pygame.K_KP3] or
                              pygame.key.get_pressed()[pygame.K_4] or pygame.key.get_pressed()[pygame.K_KP4] or
                              pygame.key.get_pressed()[pygame.K_5] or pygame.key.get_pressed()[pygame.K_KP5] or
                              pygame.key.get_pressed()[pygame.K_6] or pygame.key.get_pressed()[pygame.K_KP6] or
                              pygame.key.get_pressed()[pygame.K_1] or pygame.key.get_pressed()[pygame.K_KP1] or
                              pygame.key.get_pressed()[pygame.K_8] or pygame.key.get_pressed()[pygame.K_KP8] or
                              pygame.key.get_pressed()[pygame.K_9] or pygame.key.get_pressed()[pygame.K_KP9]):
                            self.storage[slot][2] = False
                    if self.storage[slot][1] == "Hotkey 8":
                        if (pygame.key.get_pressed()[pygame.K_8] or pygame.key.get_pressed()[pygame.K_KP8]):
                            self.storage[slot][2] = True
                            for sl in self.storage:
                                if isinstance(self.storage[slot][0],Item):
                                    if sl != slot:
                                        if self.storage[sl][2] == True:
                                            self.storage[sl][2] = False
                                            break
                        elif (pygame.key.get_pressed()[pygame.K_2] or pygame.key.get_pressed()[pygame.K_KP2] or
                              pygame.key.get_pressed()[pygame.K_3] or pygame.key.get_pressed()[pygame.K_KP3] or
                              pygame.key.get_pressed()[pygame.K_4] or pygame.key.get_pressed()[pygame.K_KP4] or
                              pygame.key.get_pressed()[pygame.K_5] or pygame.key.get_pressed()[pygame.K_KP5] or
                              pygame.key.get_pressed()[pygame.K_6] or pygame.key.get_pressed()[pygame.K_KP6] or
                              pygame.key.get_pressed()[pygame.K_7] or pygame.key.get_pressed()[pygame.K_KP7] or
                              pygame.key.get_pressed()[pygame.K_1] or pygame.key.get_pressed()[pygame.K_KP1] or
                              pygame.key.get_pressed()[pygame.K_9] or pygame.key.get_pressed()[pygame.K_KP9]):
                            self.storage[slot][2] = False
                    if self.storage[slot][1] == "Hotkey 9":
                        if (pygame.key.get_pressed()[pygame.K_9] or pygame.key.get_pressed()[pygame.K_KP9]):
                            self.storage[slot][2] = True
                            for sl in self.storage:
                                if isinstance(self.storage[slot][0],Item):
                                    if sl != slot:
                                        if self.storage[sl][2] == True:
                                            self.storage[sl][2] = False
                                            break
                        elif (pygame.key.get_pressed()[pygame.K_2] or pygame.key.get_pressed()[pygame.K_KP2] or
                              pygame.key.get_pressed()[pygame.K_3] or pygame.key.get_pressed()[pygame.K_KP3] or
                              pygame.key.get_pressed()[pygame.K_4] or pygame.key.get_pressed()[pygame.K_KP4] or
                              pygame.key.get_pressed()[pygame.K_5] or pygame.key.get_pressed()[pygame.K_KP5] or
                              pygame.key.get_pressed()[pygame.K_6] or pygame.key.get_pressed()[pygame.K_KP6] or
                              pygame.key.get_pressed()[pygame.K_7] or pygame.key.get_pressed()[pygame.K_KP7] or
                              pygame.key.get_pressed()[pygame.K_8] or pygame.key.get_pressed()[pygame.K_KP8] or
                              pygame.key.get_pressed()[pygame.K_1] or pygame.key.get_pressed()[pygame.K_KP1]):
                            self.storage[slot][2] = False
                    if (pygame.key.get_pressed()[pygame.K_0] or pygame.key.get_pressed()[pygame.K_KP0]):
                        self.storage[slot][2] = False

class Player(ImageEntity):

    def __init__(self,filename):

        self.inventory = Inventory("interface.jpg")

        # Free Positions (Tuple for tuple in screenPositions if tuple not in list with tuple-positions of walls in the current maze.)
        self.fP = [x for x in screenPositions if x not in [(y[0]*brickWidth,y[1]*brickHeight) for y in dungeon[currentMaze] if "wallEntity" in dungeon[currentMaze][y]]]
        self.fP.sort()
        playerPos = self.fP[randint(0,len(self.fP)-1)]
        ImageEntity.__init__(self,"GFX\Players",filename,playerPos[0]/brickWidth,playerPos[1]/brickHeight)

        self.info["Name"] = ""
        self.info["Walk Cooldown"] = 0
        self.info["Walk Delay"] = 0.3
        self.info["Health"] = 100
        self.info["XP"] = 0

        self.walkUp = [self.s.subsurface((x*31,0,31,30)) for x in range(3)]
        temp = []
        for i in self.walkUp:
            for j in range(8):
                temp.append(i)
        self.walkUp = temp
        self.walkDown = [self.s.subsurface((x*31,36*2,31,38)) for x in range(3)]
        temp = []
        for i in self.walkDown:
            for j in range(8):
                temp.append(i)
        self.walkDown = temp
        self.walkLeft = [self.s.subsurface((x*31,144-36,31,36)) for x in range(3)]
        temp = []
        for i in self.walkLeft:
            for j in range(8):
                temp.append(i)
        self.walkLeft = temp
        self.walkRight = [self.s.subsurface((x*31,36,31,38)) for x in range(3)]
        temp = []
        for i in self.walkRight:
            for j in range(8):
                temp.append(i)
        self.walkRight = temp

        self.dir = 1
        self.frame = 0
        self.walking = False

        self.previousItemPos = None

    def move(self):

        if pygame.key.get_pressed()[pygame.K_F12]:
            gPT([str((self.x,self.y)),self.x,self.y],[str((self.x,self.y)),self.x,self.y],(255,0,0),16)
        if pygame.key.get_pressed()[pygame.K_w] == True or pygame.key.get_pressed()[pygame.K_UP] == True:
            if (self.x,self.y-brickHeight) in self.fP:
                self.walking = True
                self.dir = 0
                self.y -= brickHeight
        if pygame.key.get_pressed()[pygame.K_s] == True or pygame.key.get_pressed()[pygame.K_DOWN] == True:
            if (self.x,self.y+brickHeight) in self.fP:
                self.walking = True
                self.dir = 1
                self.y += brickHeight
        if pygame.key.get_pressed()[pygame.K_a] == True or pygame.key.get_pressed()[pygame.K_LEFT] == True:
            if (self.x-brickWidth,self.y) in self.fP:
                self.walking = True
                self.dir = 2
                self.x -= brickWidth
        if pygame.key.get_pressed()[pygame.K_d] == True or pygame.key.get_pressed()[pygame.K_RIGHT] == True:
            if (self.x+brickWidth,self.y) in self.fP:
                self.walking = True
                self.dir = 3
                self.x += brickWidth
        if not (pygame.key.get_pressed()[pygame.K_w] or pygame.key.get_pressed()[pygame.K_UP] or
                pygame.key.get_pressed()[pygame.K_s] or pygame.key.get_pressed()[pygame.K_DOWN] or
                pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_LEFT] or
                pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT]):
            self.walking = False

    def draw(self):

        if self.dir == 0:
            screen.blit(pygame.transform.scale(self.walkUp[self.frame],(brickWidth,brickHeight)),(self.x,self.y))
            if self.walking == True:
                self.frame += 1
            if self.frame > len(self.walkUp)-1:
                self.frame = 0

        if self.dir == 1:
            screen.blit(pygame.transform.scale(self.walkDown[self.frame],(brickWidth,brickHeight)),(self.x,self.y))
            if self.walking == True:
                self.frame += 1
            if self.frame > len(self.walkDown)-1:
                self.frame = 0
        if self.dir == 2:
            screen.blit(pygame.transform.scale(self.walkLeft[self.frame],(brickWidth,brickHeight)),(self.x,self.y))
            if self.walking == True:
                self.frame += 1
            if self.frame > len(self.walkLeft)-1:
                self.frame = 0

        if self.dir == 3:
            screen.blit(pygame.transform.scale(self.walkRight[self.frame],(brickWidth,brickHeight)),(self.x,self.y))
            if self.walking == True:
                self.frame += 1
            if self.frame > len(self.walkRight)-1:
                self.frame = 0

    def watchForDropCommand(self,cursor):

        if pygame.key.get_pressed()[pygame.K_x]:
            for slot in self.inventory.storage:
                if self.inventory.storage[slot][2] == True:
                    self.previousItemPos = (self.inventory.cursor.x,self.inventory.cursor.y)
                    self.inventory.storage[slot][0].x = cursor.x
                    self.inventory.storage[slot][0].y = cursor.y
                    self.inventory.storage[slot][0].draw("INGAME")
        if not pygame.key.get_pressed()[pygame.K_x]:
            for slot in self.inventory.storage:
                if self.inventory.storage[slot][2] == True:
                    if self.previousItemPos is not None:
                        self.inventory.storage[slot][0].x = self.previousItemPos[0]
                        self.inventory.storage[slot][0].y = self.previousItemPos[1]

class popUp(ImageEntity):

    def __init__(self,title,x,y,alpha=255):
        ImageEntity.__init__(self,"GFX","interface.jpg",x,y)

        self.title = title
        self.alpha = alpha
        self.hasFocus = False
        self.content = []

        self.surface = gIBGI(filename)
        self.surface.set_alpha(self.alpha)

    def addContent(self,content):

        self.content.append(content)

    def popUp(self):

        gIBGI(filename)


