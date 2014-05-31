#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
====================================================================
Endless Evil
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
Game written by Ericson Willians, a brazilian composer and programmer.

CONTACT: ericsonwrp@gmail.com
AS A COMPOSER: https://soundcloud.com/r-p-ericson-willians
YOUTUBE CHANNEL: http://www.youtube.com/user/poisonewein

====================================================================
"""

__author__ = 'EricsonWillians'

import os   
from random import randint
from pygame import *
from engine import *

gD()
cursor = SelectionCursor("GFX","selectionCursor.png",0,0)
player = Player("townfolk1_f.png")
while not DONE:

    delta = clock.tick() / 1000.0

    if key.get_pressed()[K_LALT] and key.get_pressed()[K_F4]:
        DONE = True

    if gameScreen == "GAME":

        screen.blit(ground,(0,0))
        dCD()
        player.draw()
        player.info["Walk Cooldown"] -= delta
        if player.info["Walk Cooldown"] <=  0:
            player.move()
            player.info["Walk Cooldown"] = player.info["Walk Delay"]
        cursor.draw("INGAME")
        cursor.move()
        player.watchForDropCommand(cursor)

        gT([str(currentMaze),1,1],[str(currentMaze),1,1],(255,255,255),64,[50,40]) # Current Maze.
        if key.get_pressed()[K_F11]:
            gT(["FPS: " + str(clock.get_fps()),1,15],["FPS: " + str(clock.get_fps()),1,15],(200,255,200),32,[50,0]) # FPS.
            gT(["Walk Cooldown: " + str(player.info["Walk Cooldown"]),5,15],["Walk Cooldown: " + str(player.info["Walk Cooldown"]),5,15],(255,255,255),32,[60,0]) # Player Walk Cooldown.
         
        if key.get_pressed()[K_i] or mouse.get_pressed()[1]:
            gameScreen = "INVENTORY"

    if gameScreen == "INVENTORY":

        player.inventory.draw()
        player.inventory.watchForHotkeys()
        player.inventory.watchForHotkeyAssignments()
        player.inventory.watchForPositionalMouseRequests()

        if key.get_pressed()[K_ESCAPE]:
            gameScreen = "GAME"

    for e in event.get():
        
        if e.type == QUIT:
            
            DONE = True

    display.update()

quit()
