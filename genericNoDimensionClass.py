#/usr/bin/env python3

# Environment variables
isVisibleMouse = False
dimensions = (1024, 768)

# Imports
import pygame, sys, math
from random import randint
from pygame.locals import *
from classes import *
from formulae import *

# Setting environment
pygame.init()
fpsClock = pygame.time.Clock()
pygame.mouse.set_visible(isVisibleMouse)
screen = pygame.display.set_mode(dimensions)
background = pygame.Surface(dimensions)

# Colors
black = pygame.Color(0, 0, 0)

# Position functions
def randomPlace():
    maxX, maxY = dimensions
    return ( randint(0, maxX), randint(0, maxY) )

def newPos(object):
    pos = randomPlace()
    while not object.isOnScreen(pos, dimensions):
        pos = randomPlace()
    return pos

# Handy functions
def buildBackground(tile, background, dimensions):
    maxX, maxY = dimensions
    dx, dy = tile.dimensions
    for y in range(0, maxY, dy):
        for x in range(0, maxX, dx):
            background.blit(tile.pygameObject, (x, y))

# Sprites
char = PackagedSprite('rachel', 4)
floorTile = PackagedSprite('floor', 1)

# Positions and Counters
mousePos = ( 1, 1 )

buildBackground(floorTile, background, dimensions)

while True:
    screen.fill(black)
    screen.blit(background, (0, 0))

    screen.blit(char.pygameObject, (mousePos))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            mousePos = event.pos
        elif event.type == MOUSEBUTTONUP:
            if event.button in ( 2, 3 ):
                pass
                
    pygame.display.update()
    fpsClock.tick(30)

