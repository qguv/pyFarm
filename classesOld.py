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
        self.dimensions = self.pygameObject.get_size()

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


class Cardinal():

    directions = ['north', 'east', 'south', 'west']
    directionAbbreviations = ['n', 'e', 's', 'w']

    def __init__(self, direction, north=0):
        if direction in (0, 1, 2, 3):
            self.dir = (direction - north) % 4
        else:
            try:
                direction = direction.lower()
            except AttributeError:
                raise TypeError('directional input must be an int or a str')
            if direction in directions:
                self.dir = directions.index(direction)
            elif direction in directionAbbreviations:
                self.dir = directions.index(direction)
            else:
                raise NameError('not a direction')

    def __str__(self):
        return self.directions[self.dir].capitalize()

    def __repr__(self):
        return "<Cardinal object holding direction {} at 0x{:0x}>".format(
                self.directions[self.dir].capitalize(),
                id(self))

    def __add__(self, other):
        assert type(self) is type(other), 'can only add Cardinal directions'
        return Cardinal((self.dir + other.dir) % 4)

    def __sub__(self, other):
        assert type(self) is type(other), 'can only add Cardinal directions'
        return self.dir - other.dir
    
    def __neg__(self):
        return Cardinal((self.dir + 2) % 4)

class Coords():

    def __init__(self, *args):
        if len(args) > 1:
            self.data = args
        else:
            self.data = tuple(args[0])
    def __add__(self, other):
        assert len(self) == len(other)
        return Coords([ x + y for x, y in zip(self, other) ])

    def __sub__(self, other):
        assert len(self) == len(other)
        return Coords([ x - y for x, y in zip(self, other) ])

    def __mul__(self, n):
        return Coords([ n * x for x in self ])

    def get(self):
        return self.data

