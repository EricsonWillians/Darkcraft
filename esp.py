"""
====================================================================

Shadow Killer
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

import os, sys
import xml.etree.ElementTree as ET

DEFAULT_MAPS_FOLDER = "Maps/"
ERICSON_PARSER = "esp"

def replaceExtension(path):

    for f in os.listdir(path):
        try:
            if 'txt' in f:
                os.rename(path+f,path+f.replace("txt",ERICSON_PARSER))
            if 'tmx' in f:
                os.rename(path+f,path+f.replace("tmx",ERICSON_PARSER))
            if 'xml' in f:
                os.rename(path+f,path+f.replace("xml",ERICSON_PARSER))
        except OSError as e:
            print(e)
            sys.exit()

class ESP():

    """
    THE ERICSON PARSER
    It parses a .esp file exported from TILED Map Editor.
    """

    def __init__(self, xmlFile, path=DEFAULT_MAPS_FOLDER):

        replaceExtension(path)

        if ".esp" not in xmlFile:
            self.fullPath = os.path.join(path, xmlFile+".esp")
        elif "esp" not in xmlFile:
            self.fullPath = os.path.join(path, xmlFile+"esp")
        else:
            self.fullPath = os.path.join(path, xmlFile)

        self.data = []
        self.tree = ET.parse(self.fullPath)
        self.root = self.tree.getroot()
        for i in self.root.iter():
            self.data.append(dict([list(x) for x in i.items()]))

    def getTags(self):
        l = []
        for i in self.root.iter():
            l.append(i.tag)
        return l

    def getElementByTag(self, tag):
        l = []
        filtered = []
        for i in self.root.iter():
            if i.tag == tag:
                for j in i.items():
                    l.append(j)
        return l

    def getValueInElementByTag(self, tag, name):
        l = []
        value = ''
        for i in self.root.iter():
            if i.tag == tag:
                for j in i.items():
                    if name in j:
                        value = j[1]
        return value
