"""
====================================================================

PYTHUN ENGINE 2.1 - Stable Release
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

import os
import operator
from collections import Sequence
import itertools
import collections
import pygame
import esp
import error

class Global():

    """
    The Pythun Global class provides useful and common attributes and static methods.
    """

    DONE = False
    CLOCK = pygame.time.Clock()
    RESOLUTIONS = {"CGA":(320,200),"CIF":(352,288),"HVGA":(480,320),
                    "QVGA":(320,240),"SIF**":(384,288),"WVGA":(800,480),
                    "WVGA(NTSC_CROSS)":(854,480),"PAL_CROSS":(1024,576),
                    "WSVGA":(1024,600),"VGA(NTSC*)":(640,480),"PAL*":(768,576),
                    "SVGA":(800,600),"XGA":(1024,768),"XGA_PLUS":(1152,864),
                    "HD720":(1280,720),"WXGA1":(1280,768),"WXGA2":(1280,800),
                    "WSXGA_PLUS":(1680,1050),"HD1080":(1920,1080),"2K":(2048,1080),
                    "WUXGA":(1920,1200),"SXGA":(1280,1024),"SXGA_PLUS":(1400,1050),
                    "UXGA":(1600,1200),"QXGA":(2048,1536),"WQHD":(2560,1440),"WQXGA":(2560,1600),"QSXGA":(2560,2048)}
    INIT = pygame.display.set_mode((1,1))

    res = RESOLUTIONS.get("WXGA1")
    globalSpeed = 16*3
    movementTiles = 100
    movementSize = 4

    g = 10 # 9.81

    @staticmethod
    def loadImage(path, name, colorkey=None):

        """
        Function taken from the chimp pygame tutorial and altered a bit (To deal with PNG alpha transparency, for example).
        The function is just too good for me not to use it :).
        https://www.pygame.org/docs/tut/chimp/ChimpLineByLine.html
        """

        fullname = os.path.join(path, name)
        try:
            image = pygame.image.load(fullname)
        except pygame.error, message:
            print "Cannot load image:", name
            raise SystemExit, message
        if ".png" not in name:
            image = image.convert()
        else:
            image = pygame.Surface.convert_alpha(image)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    @staticmethod
    def loadSound(path, name):

        """
        Same as the above function.
        """

        class NoneSound:
            def play(self): pass
        if not pygame.mixer:
            return NoneSound()
        fullname = os.path.join(path, name)
        try:
            sound = pygame.mixer.Sound(fullname)
        except pygame.error, message:
            print "Cannot load sound:", name
            raise SystemExit, message
        return sound

    @staticmethod
    def loadDefaultFont(size):

        """
        A function to load the default system font (Good for cross-platform games).
        """

        try:
            font = pygame.font.Font(None, size)
        except pygame.error, message:
            print "Cannot load the default font"
            raise SystemExit, message
        return font

    @staticmethod
    def loadSystemFont(name, size):

        """
        A function to load a specific system font (Not good for cross-platform games).
        """

        try:
            font = pygame.font.SysFont(name, size)
        except pygame.error, message:
            print "Cannot load font: ", name
            raise SystemExit, message
        return font

    @staticmethod
    def getSystemFonts():

        """
        A function to return all system fonts in a list of strings (In case you really want a system font and is not sure about their names).
        """

        return pygame.font.get_fonts()

    @staticmethod
    def useBasicMovement(keys, collisionModel, step):

        """
        Function for engine-debugging purposes. It provides an easy and efficient way to "make things moving" fast.
        """

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            collisionModel.translate(0,step)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            collisionModel.translate(1,step)
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            collisionModel.translate(2,step)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            collisionModel.translate(3,step)

    @staticmethod
    def useBasicLeftAndRightMovement(keys, controller, step):

        """
        Function for engine-debugging purposes. It provides an easy and efficient way to "make things moving" fast.
        """

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            controller.control(controller.masterOf, controller.LEFT, step)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            controller.control(controller.masterOf, controller.RIGHT, step)

class Grid():

    """
    A Pythun Grid is a tessellation of n-dimensional Euclidean space by congruent bricks.
    """

    # === STATIC ===

    SMALL_GRID = 5, 100
    MEDIUM_GRID = SMALL_GRID[0]*2, SMALL_GRID[1]/2
    BIG_GRID = MEDIUM_GRID[0]*2, MEDIUM_GRID[1]/2
    HUGE_GRID = BIG_GRID[0]*2, BIG_GRID[1]/2

    # === OVERLOADED ===

    def __init__(self, sizes):

        """
        The Grid constructor defines its size in width and height by tiles.
        Every tile is a grid rectangle, with a x and y position and fixed size.

        The keys list has two indexes.
        keys[0] is the width of the grid in tiles.
        keys[1] is the height of the grid in tiles.

        The x dictionary has keys[0] number of keys.
        Each key[0] key in x dictionary has an equivalent int value in pixels.
        The same applies to the y dictionary.
        """

        if len(sizes) == 2:
            self.tileWidth = sizes[1][0]
            self.tileHeight = sizes[1][1]
            self.widthInTiles = sizes[0][0]
            self.heightInTiles = sizes[0][0]
            self.widthInPixels = sizes[1][0]*sizes[0][0]
            self.heightInPixels = sizes[1][1]*sizes[0][0]
        elif len(sizes) == 4:
            self.tileWidth = sizes[2]
            self.tileHeight = sizes[3]
            self.widthInTiles = sizes[0]
            self.heightInTiles = sizes[1]
            self.widthInPixels = sizes[2]*sizes[0]
            self.heightInPixels = sizes[3]*sizes[1]
        else:
            raise error.InvalidGridStructure("Invalid grid structure, considering that '(x,x,x,x)' and '((x,x),(x,x))' are valid grid structures.")
        self.keyPositions = [[x for x in range(self.widthInTiles)], [x for x in range(self.heightInTiles)]]
        self.x = dict(zip([x for x in self.keyPositions[0]], [x for x in range(0, self.widthInPixels, self.tileWidth)]))
        self.y = dict(zip([x for x in self.keyPositions[1]], [x for x in range(0, self.heightInPixels, self.tileHeight)]))

    # === GETTERS ===

    def getTileWidth(self):

        """
        getTileWidth() -> int
        It returns the width in pixels of each tile of the grid.
        """

        return self.tileWidth

    def getTileHeight(self):

        """
        getTileHeight() -> int
        It returns the height in pixels of each tile of the grid.
        """

        return self.tileHeight

    def getWidthInTiles(self):

        """
        getWidthInTiles() -> int
        It returns the width of the grid in tiles.
        """

        return self.widthInTiles

    def getHeightInTiles(self):

        """
        getHeightInTiles() -> int
        It returns the height of the grid in tiles.
        """

        return self.heightInTiles

    def getWidthInPixels(self):

        """
        getWidthInPixels() -> int
        It returns the width of the grid in pixels (Total amount of tiles in width).
        """

        return self.widthInPixels

    def getHeightInPixels(self):

        """
        getHeightInPixels() -> int
        It returns the height of the grid in pixels (Total amount of tiles in height).
        """

        return self.heightInPixels

    def getX(self, pos):

        """
        getX() -> int
        It returns the pixels corresponding to the given x-key.
        """

        if self.x.get(pos) != None: # Avoiding bugs.
            return self.x.get(pos)
        else:
            return 0

    def getY(self, pos):

        """
        getY() -> int
        It returns the pixels corresponding to the given y-key.
        """

        if self.y.get(pos) != None: # Avoiding bugs.
            return self.y.get(pos)
        else:
            return 0

    def getCenterX(self):

        """
        getCenterX() -> int
        It returns the "center" X position key of the grid.
        """

        return (self.widthInTiles / 2)-1 # Not perfectly accurate.

    def getCenterY(self):

        """
        getCenterY() -> int
        It returns the "center" Y position key of the grid.
        """

        return (self.heightInTiles / 2)-1 # Not perfectly accurate.

    # === SETTERS ===

    def setTileWidth(self, newValue):

        """
        It sets the width in pixels of each tile of the grid.
        """

        self.tileWidth = newValue

    def setTileHeight(self, newValue):

        """
        It sets the height in pixels of each tile of the grid.
        """

        self.tileHeight = newValue

    def setWidthInTiles(self, newValue):

        """
        It sets the width of the grid in tiles.
        """

        self.widthInTiles = newValue

    def setHeightInTiles(self, newValue):

        """
        It sets the height of the grid in tiles.
        """

        self.heightInTiles = newValue

class GridMap(collections.MutableMapping):

    """
    A Pythun GridMap is a dictionary with all grid positions.
    All grid positions in a GridMap are keys. There are keys for every possible position in tuples (x,y).
    Each value of a key-position in a GridMap is a GridKey, a container with Grid Images, etc.
    """

    # === OVERLOADED ===

    def __init__(self, grid, *args, **kwargs):

        self.store = dict()
        self.update(dict(*args, **kwargs))  # use the free update to set keys
        for k in list(itertools.product(grid.y.keys(),grid.x.keys())): # This is complex, I'm not going to talk about it right now.
            self.store[k] = {}

    def __getitem__(self, key):

        return self.store[self.__keytransform__(key)]

    def __setitem__(self, key, value):

        self.store[self.__keytransform__(key)] = value

    def __delitem__(self, key):

        del self.store[self.__keytransform__(key)]

    def __iter__(self):

        return iter(self.store)

    def __len__(self):

        return len(self.store)

    def __keytransform__(self, key):

        return key

class CollisionModel():

    """
    A Pythun collision model is a list with tuples containing the XML map gids and their respective grid elements,
    that includes a "player" or game object in a collision model (It handles it in the list).
    """

    def __init__(self, collider, x, y, map, collisionGids, surface):

        self.x = x
        self.y = y
        self.map = map
        self.gridKeys = [list(t) for t in self.map.gridKeys] # Converting each tuple to a mutable sequence.
        self.gids = self.map.gids
        i = 0
        for i in self.gridKeys:
            if ((i[0][0] == self.x) and (i[0][1] == self.y)):
                if i[1] == '0':
                    i[1] = collider

        self.collisionGids = collisionGids
        self.surface = surface

    def __getitem__(self, index):

        return self.gids[index]

    def __add__(self, collisionGids):

        self.collisionGids = self + collisionGids

    def __len__(self):

        return len(self.collisionGids)

    # === FUNCTIONALITY ===

    def getKey(self, x, y):

        innerXMeasure = x
        innerYMeasure = y*self.map.widthInTiles

        return self.gridKeys[innerYMeasure+x]

    def setValue(self, x, y, newValue):

        innerXMeasure = x
        innerYMeasure = y*self.map.widthInTiles

        self.gridKeys[innerYMeasure+x][1] = newValue

    def translate(self, direction, step):

        if direction == 0:
            if self.getKey(self.x,self.y-step)[1] not in self.collisionGids:
                self.y -= step
                self.setValue(self.x,self.y,self.getKey(self.x,self.y+step)[1])
                self.getKey(self.x,self.y)[1].setY(self.y)
                self.setValue(self.x,self.y+step,'0')
        if direction == 1:
            if self.getKey(self.x,self.y+step)[1] not in self.collisionGids:
                self.y += step
                self.setValue(self.x,self.y,self.getKey(self.x,self.y-step)[1])
                self.getKey(self.x,self.y)[1].setY(self.y)
                self.setValue(self.x,self.y-step,'0')
        if direction == 2:
            if self.getKey(self.x-step,self.y)[1] not in self.collisionGids:
                self.x -= step
                self.setValue(self.x,self.y,self.getKey(self.x+step,self.y)[1])
                self.getKey(self.x,self.y)[1].setX(self.x)
                self.setValue(self.x+step,self.y,'0')
        if direction == 3:
            if self.getKey(self.x+step,self.y)[1] not in self.collisionGids:
                self.x += step
                self.setValue(self.x,self.y,self.getKey(self.x-step,self.y)[1])
                self.getKey(self.x,self.y)[1].setX(self.x)
                self.setValue(self.x-step,self.y,'0')

    def drawCollider(self):

        if self.getKey(self.x,self.y)[1] not in self.collisionGids:
            self.getKey(self.x,self.y)[1].draw(self.surface)

class Grect():

    """
    A Pythun Grect is a grid rectangle.
    """

    # === OVERLOADED ===

    def __init__(self, grid, x=0, y=0, color=(255,255,255)):

        """
        The grect constructor defines its position on the specified grid and its color.

        The grect x position in pixels is the specified x-key.
        The grect y position in pixels is the specified y-key.
        The grect width and height are grid-fixed (But they can be altered).
        The grect color is the specified color.
        """

        self.grid = grid
        self.x = grid.getX(x)
        self.y = grid.getY(y)
        self.w = grid.tileWidth
        self.h = grid.tileHeight
        self.color = color

    # === GETTERS ===

    def getGrid(self):

        """
        getGrid() -> Grid
        It returns the grid associated with the instance.
        """

        return self.grid

    def getColor(self):

        """
        getColor() -> (R,G,B)
        It returns the grect RGB color (Tuple).
        """

        return self.color

    # === SETTERS ===

    def setColor(self, *color):

        """
        It sets a new color.
        """

        if len(color) < 3 or len(color) > 3:
            raise error.InvalidColorStructure("Invalid color structure, considering that '(R,G,B)' is a valid color structure.")
        elif len(color) == 3:
            self.color = color

    # === FUNCTIONALITY ===

    def draw(self, surface):

        """
        The draw() method draws the grect in its current x and y positions.
        If the grect position is offset within the grid limits, it raises a TypeError.
        """

        pygame.draw.rect(surface, self.color, (self.x, self.y, self.w, self.h))

class Animation(Sequence):

    """
    A Pythun animation object is a sequence of pygame surfaces, where each surface represents a frame.
    """

    # === STATIC ===

    LOOP_FORWARDS = True
    LOOP_BACKWARDS = False

    # === OVERLOADED ===

    def __init__(self, grid, *frames):

        self.grid = grid
        self.frame = 0
        self.step = 1
        self.direction = Animation.LOOP_FORWARDS
        self.frames = list(frames)

    def __getitem__(self, frame):

        return self.frames[frame]

    def __add__(self, frames):

        self.frames = self.frames + frames

    def __len__(self):

        return len(self.frames)

    # === GETTERS ===

    def getGrid(self):

        """
        getGrid() -> Grid
        It returns the actual grid of the animation.
        """

        return self.grid

    def getFrame(self):

        """
        getFrame() -> int
        It returns the actual frame position of the animation. (It does not return the frame, but the position).
        """

        return self.frame

    def getStep(self):

        """
        getStep() -> int
        It returns the present animation-loop step.
        """

        return self.step

    def getDirection(self):

        """
        getDirection() -> boolean
        It returns the actual looping direction.
        """

        return self.direction

    # === SETTERS ===

    def setGrid(self, newGrid):

        """
        It sets a new grid for the animation.
        """

        self.grid = newGrid

    def setFramePosition(self, newFramePosition):

        """
        It sets a new frame position.
        """

        self.frame = newFramePosition

    def setStep(self, newSequenceStep):

        """
        It sets a new sequence step.
        """

        self.step = newSequenceStep

    def setDirection(self, newLoopingDirection):

        """
        It sets a new looping direction.
        """

        self.direction = newLoopingDirection

    # === FUNCTIONALITY ===

    def appendFrame(self, frame, animationSpeed):

        """
        Appends a new frame to the animation's inner frame-collection.
        """

        for repetitionRate in range(animationSpeed):
            self.frames.append(frame)

    def animate(self, grict, isTransformed=True, flipX=False, flipY=False):

        """
        It animates the sprite-sequence on a game main loop.
        If isTransformed is equal to true, than the new surfaces are adjusted to the grid.
        flipX and flipY mirror the animation.
        """


        grict.setSurface(self.__getitem__(self.frame))

        if isTransformed == True:
            grict.transformSurface(self.grid.tileWidth, self.grid.tileHeight)
        if flipX == True:
            grict.setSurface(pygame.transform.flip(grict.getSurface(), True, False))
        if flipY == True:
            grict.setSurface(pygame.transform.flip(grict.getSurface(), False, True))

        if self.direction == Animation.LOOP_FORWARDS:
            self.frame += self.step
            if self.frame > self.__len__()-1:
                self.frame = 0
        elif self.direction == Animation.LOOP_BACKWARDS:
            self.frame -= self.step
            if self.frame < 0:
                self.frame = self.__len__()-1

    def pause(self):

        """
        It pauses the animation.
        """

        self.step = 999

    def resume(self):

        """
        It resumes the animation.
        """

        self.step = 1

class Grict(Grect):

    """
    The Pythun Grict is an image grect.
    A Grict can be treated as an "actor".
    You can add animations, functions and a controller to it.
    """

    # === STATIC ===

    STRETCHED = True
    NOT_STRETCHED = False
    WITH_UNDER_COLOR = True
    WITHOUT_UNDER_COLOR = False
    SPRITE_DETECTED = True
    BACKGROUND_DETECTED = False

    # === OVERLOADED ===

    def __init__(self, grid, x=0, y=0, path="", name="", isSpriteSheet=False, colorkey=-1, hasAnimation=False):

        self.grid = grid
        self.x = self.grid.getX(x)
        self.y = self.grid.getY(y)
        self.w = self.grid.tileWidth
        self.h = self.grid.tileHeight
        self.path = path
        self.name = name
        self.isSpriteSheet = isSpriteSheet
        self.colorkey = colorkey
        self.hasAnimation = hasAnimation
        if ((((path != "") or (name != "")) and (self.hasAnimation == False)) or ((((path != "") or (name != "")) and (self.hasAnimation == True)) and (isSpriteSheet == True))):
            self.surface = Global.loadImage(self.path, self.name, self.colorkey)
        self.animations = {}
        self.functions = {}
        self.col = None

    # === GETTERS ===

    def getPath(self):

        """
        getPath() -> String
        It returns the grict string path.
        """

        return self.path

    def getName(self):

        """
        getName() -> String
        It returns the grict string file name.
        """

        return self.fileName

    def getColorkey(self):

        """
        getColorKey() -> (R,G,B) or int
        It returns the grict color key (RGB tuple or -1).
        """

        return self.colorkey

    def getSurface(self):

        """
        getSurface() -> pygame.Surface
        It returns the grict surface.
        """

        return self.surface

    def getSubsurface(self, rect):

        """
        getSubsurface() -> pygame.Surface
        It returns the subsurface of a specified rect area in the grict surface.
        """

        return self.surface.subsurface(rect)

    def getInnerSprites(self, innerRect, times, step):

        """
        getInnerSprites() -> list with N pygame surfaces.
        If the grict is a sprite sheet, it returns a list of sprites based on the first offsets and the width and the height of the sprite rect inside the sprite sheet.
        # [0] = x, [1] = y, [2] = w, [3] = h.
        """

        innerSprites = []
        if self.isSpriteSheet == True:
            for i in range(innerRect[0], times, step):
                innerSprites.append(self.getSubsurface((i,innerRect[1],innerRect[2],innerRect[3])))
            return innerSprites
        else:
            raise error.SpriteSheetBooleanError("The Grict must be a sprite sheet in order to be subsurfaced.")

    def isSpriteSheet(self):

        """
        isSpriteSheet() -> boolean
        It returns wether the Grict is a sprite sheet or not (Animation).
        """

        return self.isSpriteSheet

    # === SETTERS ===

    def setX(self, newPos):

        """
        Sets a new x position.
        """

        self.x = self.grid.getX(newPos)

    def setY(self, newPos):

        """
        Sets a new y position.
        """

        self.y = self.grid.getY(newPos)

    def setPos(self, newPos):

        """
        Sets a new position (tuple).
        """

        if ((len(newPos) < 2) or (len(newPos) > 2)):
            raise error.InvalidPositionStructure("Invalid position structure, considering that '(x,y)' is a valid structure.")
        elif len(newPos) == 2:
            self.x = self.grid.getX(newPos[0])
            self.y = self.grid.getY(newPos[1])

    def setPosUsingAnotherGridAsReferenceForPositioning(self, newPos, referenceGrid):

        if ((len(newPos) < 2) or (len(newPos) > 2)):
            raise error.InvalidPositionStructure("Invalid position structure, considering that '(x,y)' is a valid structure.")
        elif len(newPos) == 2:
            self.x = referenceGrid.getX(newPos[0])
            self.y = referenceGrid.getY(newPos[1])

    def setPath(self, path):

        """
        The setPath() method expects a string object for the new image path of the grict instance.
        """

        self.path = path

    def setFileName(self, fileName):

        """
        The setFileName() method expects a string object for the new image file name of the grict instance.
        """

        self.fileName = fileName

    def setColorkey(self, colorkey):

        """
        The setColorkey() method expects a rgb tuple object for the new image colorkey of the grict instance.
        """

        self.colorkey = colorkey

    def setSurface(self, surface):

        """
        The setSurface() expects a pygame surface object for the new surface of the grict instance.
        """

        self.surface = surface

    # === FUNCTIONALITY ===

    def transformSurface(self, w, h):

        """
        It transforms the grict instance surface size.
        """

        transformedSurface = pygame.transform.scale(self.surface, (w, h))
        self.surface = transformedSurface

    def addAnimationPerFile(self, animationName, imageFileExtension, numberOfSprites, referenceRectForSubsurfacing, repetitionRate):

        """
        This method is too complex to be explained right now :).
        """

        if self.hasAnimation == True:
            self.animationName = animationName
            self.animations[self.animationName] = Animation(self.grid)
            if self.isSpriteSheet == False:
                for i in range(numberOfSprites):
                    self.surface = Global.loadImage(self.path+self.animationName,str(i)+imageFileExtension,self.colorkey)
                    subsurfacedImage = self.getSubsurface(referenceRectForSubsurfacing)
                    self.animations[self.animationName].appendFrame(subsurfacedImage,repetitionRate)
            else:
                raise error.GrictIsSpriteSheet("If the Grict object is a sprite sheet, then use 'addAnimationPerSprite' instead.")
        if len(self.animations[self.animationName]) > 0:
            self.surface = self.animations[self.animationName][0]

    def makeListOfSprites(self, axis, index, spriteWidth, spriteHeight, startPos, step):

        """
        makeListOfSprites() -> list of pygame surfaces.
        It subsurfaces the grict surface based on its width or height.
        The index argument specifies the starting column or the row for the iteration.
        The axis takes only two possible strings: "x" or "y".
        """

        # For the step, you'll usually want to use the size of the surface.
        # If the axis is "x", then, its width. If "y", then, it's height.

        l = []

        if axis == "x":
            for i in range(startPos,self.surface.get_width(),step):
                l.append(self.getSubsurface((i,index,spriteWidth,spriteHeight)))
        elif axis == "y":
            for i in range(startPos,self.surface.get_height(),step):
                l.append(self.getSubsurface((index,i,spriteWidth,spriteHeight)))
        else:
            raise error.UnknownAxis("Use 'x' or 'y' for the axis argument.")

        return l

    def addAnimationPerSprite(self, animationName, listOfSprites, repetitionRate):

        """
        This method adds an animation to the grict animation dictionary manually (per sprite).
        It takes a list of pygame surfaces (Fortunately, you can use "makeListOfSprites" to automatically cut a sprite sheet).
        You can also subsurface the sprite sheet manually using the 'getSubsurface()" method.
        """

        if self.hasAnimation == True:
            self.animationName = animationName
            self.listOfSprites = listOfSprites
            self.animations[self.animationName] = Animation(self.grid)
            if self.isSpriteSheet == True:
                self.surface = Global.loadImage(self.path,self.name,self.colorkey)
                if len(self.listOfSprites) > 0:
                    for sprite in self.listOfSprites:
                        self.animations[self.animationName].appendFrame(sprite,repetitionRate)
            else:
                raise error.GrictIsNotSpriteSheet("If the Grict object is not a sprite sheet, then use 'addAnimationPerFile' instead.")
        if len(self.animations[self.animationName]) > 0:
            self.surface = self.animations[self.animationName][0]

    def addCollisionModel(self, collisionModel):

        self.col = collisionModel

    def draw(self, surface, isStretched=NOT_STRETCHED, hasColor=WITHOUT_UNDER_COLOR, color=(255,255,255), isTransformed=True):

        """
        The draw() method draws the grict in its current x and y positions.
        If the grict position is offset within the grid limits, it raises a TypeError.
        """

        if isTransformed == True:
            self.transformSurface(self.grid.tileWidth, self.grid.tileHeight)
        if hasColor == Grict.WITH_UNDER_COLOR:
            pygame.draw.rect(surface, color, (self.x, self.y, self.w, self.h))
        if isStretched == Grict.STRETCHED:
            scaledToGrid = pygame.transform.scale(self.surface, (self.grid.tileWidth, self.grid.tileHeight))
            try:
                surface.blit(scaledToGrid, (self.x, self.y, scaledToGrid.get_width(), scaledToGrid.get_height()))
            except:
                pass
        elif isStretched == Grict.NOT_STRETCHED:
            try:
                surface.blit(self.surface, (self.x, self.y, self.surface.get_width(), self.surface.get_height()))
            except:
                pass

class Brect(pygame.Rect):

    """
    The Pythun Brect is a background rect.
    """

    # === OVERLOADED ===

    def __init__(self, grid, color):

        self.grid = grid
        self.color = color

    # === FUNCTIONALITY ===

    def draw(self, surface):

        try:
            pygame.draw.rect(surface, self.color, (0, 0, self.grid.widthInPixels, self.grid.heightInPixels))
        except:
            pass

class Brict(Grict):

    """
    The Pythun Brict is a background image rect.
    It inherits image-methods from Grict.
    """

    # === STATIC ===

    IT_SCROLLS = True
    IT_DOES_NOT_SCROLL = False
    SCROLL_NORTH = 0
    SCROLL_SOUTH = 1
    SCROLL_WEST = 2
    SCROLL_EAST = 3
    BACKGROUND_SCROLLING_DEFAULT_SPEED = 16

    # === OVERLOADED ===

    def __init__(self, grid, path="", name="", isScrolling=IT_DOES_NOT_SCROLL, direction=SCROLL_NORTH, scrollingSpeed=BACKGROUND_SCROLLING_DEFAULT_SPEED, colorkey=(1,1,1)):

        self.grid = grid
        self.path = path
        self.fileName = name
        self.colorkey = colorkey
        self.isScrolling = isScrolling
        self.direction = direction
        self.scrollingSpeed = scrollingSpeed
        self.x = 0
        self.y = 0
        if path != "" or name != "":
            self.surface = Global.loadImage(self.path, self.fileName, self.colorkey)

    # === GETTERS ===

    def isScrolling(self):

        """
        isScrolling() -> boolean
        It returns wether the background is scrolling or not.
        """

        return self.isScrolling

    def getDirection(self):

        """
        getDirection() -> int
        It returns the present scrolling direction.
        """

        return self.direction

    def getScrollingSpeed(self):

        """
        getScrollingSpeed() -> int
        It returns the present scrolling speed of the brict.
        """

        return self.scrollingSpeed

    # === SETTERS ===

    def setScrolling(self, boolean):

        """
        It defines wether the brict scrolls or not.
        """

        self.isScrolling = boolean

    def setScrollingDirection(self, direction):

        """
        It sets a new scrolling direction.
        """

        self.direction = direction

    def setScrollingSpeed(self, newScrollingSpeed):

        """
        It sets a new scrolling speed to the brict.
        """

        self.scrollingSpeed = newScrollingSpeed

    # === FUNCTIONALITY ===

    def draw(self, surface, isStretched=Grict.NOT_STRETCHED):

        """
        The draw() method draws the brict in the 0,0 position.
        It also scrolls the background in the brict's direction if "isScrolling" is True.
        """

        if isStretched == Grict.STRETCHED:
            scaledToGrid = pygame.transform.scale(self.surface, (self.grid.widthInPixels, self.grid.heightInPixels))
            try:
                if self.isScrolling == self.IT_SCROLLS:
                    if self.direction == Brict.SCROLL_NORTH:
                        self.y -= self.scrollingSpeed
                        if self.y<-scaledToGrid.get_height():
                            self.y = 0
                        surface.blit(scaledToGrid, (self.x, self.y+scaledToGrid.get_height(), scaledToGrid.get_width(), scaledToGrid.get_height()))
                    elif self.direction == Brict.SCROLL_SOUTH:
                        self.y += self.scrollingSpeed
                        if self.y>+scaledToGrid.get_height():
                            self.y = 0
                        surface.blit(scaledToGrid, (self.x, self.y-scaledToGrid.get_height(), scaledToGrid.get_width(), scaledToGrid.get_height()))
                    elif self.direction == Brict.SCROLL_WEST:
                        self.x -= self.scrollingSpeed
                        if self.x<-scaledToGrid.get_width():
                            self.x = 0
                        surface.blit(scaledToGrid, (self.x+scaledToGrid.get_width(), self.y, scaledToGrid.get_width(), scaledToGrid.get_height()))
                    elif self.direction == Brict.SCROLL_EAST:
                        self.x += self.scrollingSpeed
                        if self.x>+scaledToGrid.get_width():
                            self.x = 0
                        surface.blit(scaledToGrid, (self.x-scaledToGrid.get_width(), self.y, scaledToGrid.get_width(), scaledToGrid.get_height()))
                    surface.blit(scaledToGrid, (self.x, self.y, scaledToGrid.get_width(), scaledToGrid.get_height()))
                elif self.isScrolling == self.IT_DOES_NOT_SCROLL:
                    surface.blit(scaledToGrid, (0, 0, scaledToGrid.get_width(), scaledToGrid.get_height()))
            except:
                pass
        elif isStretched == Grict.NOT_STRETCHED:
            try:
                if self.isScrolling == self.IT_SCROLLS:
                    if self.direction == Brict.SCROLL_NORTH:
                        self.y -= self.scrollingSpeed
                        if self.y<-self.surface.get_height():
                            self.y = 0
                        surface.blit(self.surface, (self.x, self.y+self.surface.get_height(), self.surface.get_width(), self.surface.get_height()))
                    elif self.direction == Brict.SCROLL_SOUTH:
                        self.y += self.scrollingSpeed
                        if self.y>+self.surface.get_height():
                            self.y = 0
                        surface.blit(self.surface, (self.x, self.y-self.surface.get_height(), self.surface.get_width(), self.surface.get_height()))
                    elif self.direction == Brict.SCROLL_WEST:
                        self.x -= self.scrollingSpeed
                        if self.x<-self.surface.get_width():
                            self.x = 0
                        surface.blit(self.surface, (self.x+self.surface.get_width(), self.y, self.surface.get_width(), self.surface.get_height()))
                    elif self.direction == Brict.SCROLL_EAST:
                        self.x += self.scrollingSpeed
                        if self.x>+self.surface.get_width():
                            self.x = 0
                        surface.blit(self.surface, (self.x-self.surface.get_width(), self.y, self.surface.get_width(), self.surface.get_height()))
                    surface.blit(self.surface, (self.x, self.y, self.surface.get_width(), self.surface.get_height()))
                elif self.isScrolling == self.IT_DOES_NOT_SCROLL:
                    surface.blit(self.surface, (0, 0, self.surface.get_width(), self.surface.get_height()))
            except:
                pass

class GrectArray():

    """
    A Pythun GrectArray is a sequence of grid rectangles.
    """

    # === OVERLOADED ===

    def __init__(self, grid):

        """
        The constructor defines to the GrectArray instance its own list and a boolean indicating if it is used as a background.
        """

        self.grid = grid
        self.array = []

    # === GETTERS ===

    def getGrid(self):

        """
        getGrid() -> Grid
        It returns the associated grid instance.
        """

        return self.grid

    # === FUNCTIONALITY ===

    def add(self, grect):

        """
        It adds a grect to the grect array.
        """

        self.array.append(grect)

    def remove(self, grect):

        """
        It removes a grect from the grect array if it exists.
        """

        if len(self.array) > 0:
            for i in self.array:
                if i == grect:
                    self.array.remove(grect)
        else:
            raise error.EmptyGrectArray("You can't remove something from a set of things if the 'set of things' is empty!")

    def draw(self, surface):

        """
        The draw() method draws the sequence of grects.
        It loops through the sequence and draws each grect in their own x and y positions.
        If the position of a grect is offset within the grid limits, it raises a TypeError.
        """

        try:
            if len(self.array) > 0:
                for i in self.array:
                    pygame.draw.rect(surface, i.color, (i.x, i.y, self.grid.tileWidth, self.grid.tileHeight))
        except:
            pass

def loadMaps():

    """
    A function to load maps in the default maps folder with the Ericson Parser.
    """

    maps = []
    for f in os.listdir(esp.DEFAULT_MAPS_FOLDER):
        if f.endswith("esp"):
            maps.append(f)
    return maps

class Map():

    """
    A Pythun Tileset makes things easier to work with tilesets.
    """

    # === OVERLOADED ===

    def __init__(self, xmlMapFile, path, name, isSpriteSheet=False, colorkey=None):

        self.xml = esp.ESP(xmlMapFile) # It creates a XML Tree for the Tileset instance.
        # Collected information from the TILED .tmx/XML file.
        self.widthInPixels = int(self.xml.getValueInElementByTag('image','width'))
        self.heightInPixels = int(self.xml.getValueInElementByTag('image','height'))
        self.widthInTiles = int(self.xml.getValueInElementByTag('map','width'))
        self.heightInTiles = int(self.xml.getValueInElementByTag('map','height'))
        self.tileWidth = int(self.xml.getValueInElementByTag('tileset','tilewidth'))
        self.tileHeight = int(self.xml.getValueInElementByTag('tileset','tileheight'))
        # Two Grids. One for the map, and one for the tileset.
        self.mapGrid = Grid(((self.widthInTiles,self.heightInTiles),
                             ((self.tileWidth+((Global.res[0]/self.widthInTiles)-self.tileWidth)),
                              (self.tileHeight+(Global.res[1]/self.heightInTiles)-self.tileHeight))))
        self.tilesetGrid = Grid(((self.widthInPixels/self.widthInTiles,self.heightInPixels/self.heightInTiles),
                                 ((self.tileWidth+(Global.res[0]/self.widthInTiles)-self.tileWidth),
                                  ((self.tileHeight+Global.res[1]/self.heightInTiles)-self.tileHeight))))
        # Trivial information.
        self.x = 0
        self.y = 0
        self.path = path
        self.name = name
        self.isSpriteSheet = isSpriteSheet
        self.colorkey = colorkey
        self.tileset = Grict(self.tilesetGrid,self.x,self.y,self.path,self.name,self.isSpriteSheet,self.colorkey)
        # Gids from the XML.
        self.gids = []
        for i in self.xml.getElementByTag('tile'):
            self.gids.append(i[1])
        # It creates a GridMap for the instance (A little tuple-trick of mine (See GridMap class)).
        self.gridMap = GridMap(self.mapGrid) # Instantiating, using the grid for the map as a grid reference. (mapGrid and GridMap are different things).
        self.gridKeys = self.gridMap.keys() # The keys of the instance of the GridMap (It returns the product of every possible combination of positions in the specified grid, in tuples.)
        self.gridKeys.sort(key=lambda x:tuple(reversed(x))) # They're dicts, so they need to be properly ordered for further XML-analysis.
        self.gridKeys = zip(self.gridKeys,self.gids) # Associates each tuplePosition-key with the XML-gids.
        subs = [Grict(self.tilesetGrid)] # Creates a default 0 Grict (It shall correspond to the 0-gid of the XML (It's necessary to have it, otherwise the 0 gid would be considered and the order would be wrong.)).
        subs[0].setSurface(pygame.Surface((1,1),pygame.SRCALPHA,32).convert_alpha()) # It sets a transparent pygame Surface to it.
        filtered = [] # A list for the Gricts corresponding to the tiles of the XML-map.
        w = self.tileWidth
        h = self.tileHeight
        # It iterates over the size of the tileset in pixels by step of the size of each tile (For each collumn it iterates over each row).
        for i in range(0,self.heightInPixels,self.tileHeight):
            for j in range(0,self.widthInPixels,self.tileWidth):
                g = Grict(self.tilesetGrid) # Creates a local Grict.
                # It sets a surface for the local grid, by the process of subsurfacing the original tileset.
                g.setSurface(self.tileset.getSubsurface((j,i,w,h)))
                # It appends each tile from the tileset as Grict in the subs list (After the default 0 Grict).
                subs.append(g)
        # That was ALL the tiles.
        # Now we filter only the gricts used in the map.
        for j in self.gids: # For each string-gid.
            for i in range(len(subs)): # It iterates over the size of the whole amount of tiles/gricts.
                if str(i) == j: # If the index-position equals to the gid (In the case, only the gids used in the map)
                    filtered.append(subs[i]) # Append the filtered grict to the filtered list.
        self.gids = zip(self.gids,filtered) # It combines the xml-map-gids with the filtered/right gricts/tiles.

    # === GETTERS ===

    def getXML(self):

        """
        getXML() -> ESP
        It returns the parsed form of the XML map document used by the Tileset instance.
        """

        return self.xml

    def getWidthInPixels(self):

        """
        getWidthInPixels() -> int
        It returns the width of the image used by the tileset in pixels.
        """

        return self.widthInPixels

    def getHeightInPixels(self):

        """
        getHeightInPixels() -> int
        It returns the height of the image used by the tileset in pixels.
        """

        return self.heightInPixels

    def getWidthInTiles(self):

        """
        getWidthInTiles() -> int
        It returns the width of the image used by the tileset in tiles.
        """

        return self.widthInTiles

    def getHeightInTiles(self):

        """
        getHeightInTiles() -> int
        It returns the height of the image used by the tileset in tiles.
        """

        return self.heightInTiles

    def getTileWidth(self):

        """
        getTileWidth() -> int
        It returns the fixed width of each tile of the tileset.
        """

        return self.tileWidth

    def getTileHeight(self):

        """
        getTileHeight() -> int
        It returns the fixed height of each tile of the tileset.
        """

        return self.tileHeight

    def getMapGrid(self):

        """
        getMapGrid() -> Grid
        It returns the grid used for the whole map. (Used for the MapGrid class).
        """

        return self.mapGrid

    def getTilesetGrid(self):

        """
        getTilesetGrid() -> Grid
        It returns the grid used for the whole tileset.
        """

        return self.tilesetGrid

    def getX(self):

        """
        getX() -> int
        It returns the initial X position of the tileset (Not used by default).
        """

        return self.x

    def getY(self):

        """
        getY() -> int
        It returns the initial Y position of the tileset (Not used by default).
        """

        return self.y

    def getPath(self):

        """
        getPath() -> String
        It returns the path used for the tileset image file.
        """

        return self.path

    def getName(self):

        """
        getName() -> String
        It returns the name used for the tileset image file.
        """

        return self.name

    def isSpriteSheet(self):

        """
        isSpriteSheet() -> Boolean
        It returns wether the tileset image is used as a spritesheet or not (For colorkey purposes).
        This method is only here because the tileset image is loaded through a Grict.
        """

        return self.isSpriteSheet

    def getColorkey(self):

        """
        getColorkey() -> int
        This method is only here because the tileset image is loaded through a Grict.
        """

        return self.colorkey

    def getTileset(self):

        """
        getTileset() -> Grict
        It returns the grict (with the image) used for the tileset.
        """

        return self.tileset

    # === SETTERS ===

    def setXML(self, newXML):

        """
        It sets a new ESP for the tileset instance.
        """

        self.xml = newXML

    def setWidthInPixels(self, newValue):

        """
        It sets a new width in pixels (int) for the tileset instance.
        """

        self.widthInPixels = newValue

    def setHeightInPixels(self, newValue):

        """
        It sets a new height in pixels (int) for the tileset instance.
        """

        self.heightInPixels = newValue

    def setWidthInTiles(self, newValue):

        """
        It sets a new width in tiles (int) for the tileset instance.
        """

        self.widthInTiles = newValue

    def setHeightInTiles(self, newValue):

        """
        It sets a new height in tiles (int) for the tileset instance.
        """

        self.heightInTiles = newValue

    def setTileWidth(self, newValue):

        """
        It sets a new fixed width for each tile of the tileset instance (int).
        """

        self.tileWidth = newValue

    def setTileHeight(self, newValue):

        """
        It sets a new fixed height for each tile of the tileset instance (int).
        """

        self.tileHeight = newValue

    def setMapGrid(self, newGrid):

        """
        It sets a new grid for the map grid of the tileset instance.
        """

        self.mapGrid = newGrid

    def setTilesetGrid(self, newGrid):

        """
        It sets a new grid for the tileset grid of the tileset instance.
        """

        self.tilesetGrid = newGrid

    def setX(self, newValue):

        """
        It sets a new x position for the tileset instance (int).
        """

        self.x = newValue

    def setY(self, newValue):

        """
        It sets a new y position for the tileset instance (int).
        """

        self.y = newValue

    def setPath(self, newPath):

        """
        It sets a new path for the image file of the tileset instance (String).
        """

        self.path = newPath

    def setName(self, newName):

        """
        It sets a new name for the image file of the tileset instance (String).
        """

        self.name = newName

    def setColorkey(self, newValue):

        """
        It sets a new colorkey for the image of the tileset instance (int).
        """

        self.colorkey = newValue

    def setTileset(self, newTileset):

        """
        It sets a whole new Grict for the tileset instance.
        """

        if isinstance(newTileset, Grict):
            self.tileset = newTileset
        else:
            raise error.InvalidObject("The given tileset is not a Grict.")

    # === FUNCTIONALITY ===

    def draw(self, surface):

        i = 0
        for key in self.gridKeys:
            if key[1] == self.gids[i][0]:
                self.gids[i][1].setX(key[0][0])
                self.gids[i][1].setY(key[0][1])
                self.gids[i][1].draw(surface)
            i += 1

class Levels():

    """
    A class to handle all levels in a game.
    Every level has its own grid.
    """

    def __init__(self):

        self.gameMaps = loadMaps()
        self.loadedMaps = []
        self.levelGridMaps = []
        self.levelData = []
        if len(self.gameMaps) > 0:
            i = 0
            for m in self.gameMaps:
                self.loadedMaps.append(esp.ESP(m))
                i += 1

    def __getitem__(self, map):

        return self.loadedMaps[map]

    def __len__(self):

        return len(self.loadedMaps)

    def drawLevel(self, surface, level, tiles):

        for tileKey in tiles.keys():
            for key in self.levelGridMaps[level].keys():
                if self.levelGridMaps[level][key] == tileKey:
                    g = Grict(self.levelGrids[level])
                    g.setSurface(tiles.get(tileKey))
                    g.setY(key[0])
                    g.setX(key[1])
                    g.draw(surface)
