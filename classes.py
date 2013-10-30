#/usr/bin/env python3
import pygame, sys, os
import formulae
from pygame.locals import *

pygame.init()

class Sprite():
    '''
    A video-game sprite which interacts with pygame and produces instances of
    pygame.image.load stored in self.pygameObject.
    Takes a tuple of file paths and optionally a path to load first.
    The sprite will load the first path in pygameObject (or the optionally
    chosen first path) and store the pygame image.load instance in pygameObject.
    This can be accessed by calling self.pygameObject from the mainline code.
    '''

    def __init__(self, paths, first=0):
        assert first in range(len(self.paths)), "piece number out of range!"
        self.paths = paths
        self.selected = first
        self.update()

    def update(self):
        self.path = self.paths[self.selected]
        self.pygameObject = pygame.image.load(self.path)
        self.dimensions = Point(self.pygameObject.get_size())

    def next(self):
        if self.selected + 1 < len(self.paths):
            self.selected += 1
        else:
            self.selected = 0
        self.update()

    def set(self, piece):
        assert piece in range(len(self.paths)), "piece number out of range!"
        self.selected = piece
        self.update()

    def getCenterpoint(self, position):
        x = self.dimensions[0] / 2 + position[0]
        y = self.dimensions[1] / 2 + position[1]
        return (x, y)

    def getEndpoint(self, position):
        x = self.dimensions[0] + position[0]
        y = self.dimensions[1] + position[1]
        return (x, y)

    def isOnScreen(self, position, dimensions):
        maxX, maxY = dimensions
        x, y = self.getEndpoint(position)
        return x < maxX and y < maxY


class PackagedSprite(Sprite):
    '''
    Like Sprite() but takes sprite data from "sprites" folder under a named (or
    numbered) folder.
    Takes a folder name (as an int or a string) and an int giving the number of
    sprite pieces contained in the folder.
    '''

    def __init__(self, folderName, numPieces):
        self.paths = tuple()
        for piece in range(numPieces):
            self.paths += (os.path.join( \
                            'sprites', str(folderName), str(piece) + '.png'), )
        self.selected = 0
        self.update()


class Cardinal(int):

    directions = ['north', 'east', 'south', 'west']
    directionAbbreviations = ['n', 'e', 's', 'w']

    def __new__(self, direction, north=0):
        if direction in (0, 1, 2, 3):
            return int.__new__(Cardinal, (direction - north) % 4)
        else:
            try:
                direction = direction.lower()
            except AttributeError:
                raise TypeError('directional input must be an int or a str')
            if direction in directions:
                return int.__new__(Cardinal, directions.index(direction))
            elif direction in directionAbbreviations:
                return int.__new__(Cardinal, directionsAbbreviations.index(direction))
            else:
                raise NameError('not a direction')

    def __str__(self, abbreviate=False):
        if abbreviate:
            return self.directionAbbreviations[self].capitalize()
        else:
            return self.directions[self].capitalize()

    def __repr__(self):
        return "<Cardinal object holding direction {} at 0x{:0x}>".format(
                self.directions[self].capitalize(),
                id(self))

    def __add__(self, other):
        return Cardinal((int(self) + int(other)) % 4)

    def __neg__(self):
        return Cardinal((self + 2) % 4)

class Point(tuple):

    def __new__(self, *args):
        if len(args) == 1:
            return tuple.__new__(Point, *args)
        elif len(args) == 2:
            x, y = args
            return tuple.__new__(Point, (x, y))

    def __add__(self, other):
        x1, y1 = self
        if type(other) == type(int()):
            n = other
            return Point(x1 + n, y1 + n)
        elif len(other) == 2:
            x2, y2 = other
            return Point(x1 + x2, y1 + y2)
        else:
            raise TypeError("what are you even doing? ints, tuples, or Points!")

    def __sub__(self, other):
        x1, y1 = self
        if type(other) == type(int()):
            n = other
            return Point(x1 - n, y1 - n)
        elif len(other) == 2:
            x2, y2 = other
            return Point(x1 - x2, y1 - y2)
        else:
            raise TypeError("what are you even doing? ints, tuples, or Points!")

    def __mul__(self, other):
        x1, y1 = self
        if type(other) == type(int()):
            n = other
            return Point(x1 * n, y1 * n)
        elif len(other) == 2:
            x2, y2 = other
            return Point(x1 * x2, y1 * y2)
        else:
            raise TypeError("what are you even doing? ints, tuples, or Points!")

    def __truediv__(self, other):
        x1, y1 = self
        if type(other) == type(int()):
            n = other
            return Point(x1 / n, y1 / n)
        elif len(other) == 2:
            x2, y2 = other
            return Point(x1 / x2, y1 / y2)
        else:
            raise TypeError("what are you even doing? ints, tuples, or Points!")

    def __floordiv__(self, other):
        x1, y1 = self.__truediv__(other)
        return Point(int(x1), int(y1))

    def __rmul__(self, other):
        return self.__mul__(self, other)

    def angle(self, other):
        from math import atan2, pi, degrees
        x1, y1 = self
        x2, y2 = other
        dx = x2 - x1
        dy = y2 - y1
        rads = atan2(-dy, dx)
        rads %= 2 * pi
        deg = degrees(rads)
        return deg

    def distance(self, other):
        from math import sqrt
        x1, y1 = self
        x2, y2 = other
        return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

