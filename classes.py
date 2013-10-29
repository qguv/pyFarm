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

