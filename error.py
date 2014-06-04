"""
====================================================================

PYTHUN ENGINE 2.1 - Stable Release.
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

class InvalidColorStructure(Exception):
    pass

class InvalidGridStructure(Exception):
    pass

class SpriteSheetBooleanError(Exception):
    pass

class InvalidPositionStructure(Exception):
    pass

class InvalidObject(Exception):
    pass

class EmptyGrectArray(Exception):
    pass

class GrictIsSpriteSheet(Exception):
    pass

class GrictIsNotSpriteSheet(Exception):
    pass

class UnknownAxis(Exception):
    pass

class InvalidDirection(Exception):
    pass
