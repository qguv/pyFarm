#/usr/bin/env python3

# Imports
import pygame, sys, math
from random import randint
from pygame.locals import *
from classes import *
from formulae import *

# Environment variables
isVisibleMouse = False
dimensions = Point(1024, 768)
cameraSlack = 90

# Setting environment
pygame.init()
fpsClock = pygame.time.Clock()
pygame.mouse.set_visible(isVisibleMouse)
screen = pygame.display.set_mode(dimensions)
background = pygame.Surface(dimensions)

# Handy shortcuts
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
lightGrey = pygame.Color(200, 200, 200)
topLeft = Point(0, 0)
bottomRight = dimensions #Total sugar
midScreen = dimensions // 2

# Position functions
def randomPlace():
    maxX, maxY = dimensions
    return Point(randint(0, maxX), randint(0, maxY))

def newPos(object):
    pos = randomPlace()
    while not object.isOnScreen(pos, dimensions):
        pos = randomPlace()
    return pos

# Handy functions
def buildBackground(tile, background, dimensions : Point):
    maxX, maxY = dimensions
    dx, dy = tile.dimensions
    for y in range(0, maxY, dy):
        for x in range(0, maxX, dx):
            background.blit(tile.pygameObject, Point(x, y))

# Sprites
char = PackagedSprite('rachel', 4)
floorTile = PackagedSprite('floor', 1)

# Positions and Counters
mousePos = Point(1, 1)
cameraPos = Point(1, 1)

buildBackground(floorTile, background, dimensions)
pygame.draw.circle(background, lightGrey, midScreen, 8, 1)

while True:
    screen.fill(black)
    screen.blit(background, topLeft)

    screen.blit(char.pygameObject, mousePos - char.dimensions / 2)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            mousePos = Point(event.pos)
            angleToCenter = mousePos.angle(dimensions / 2)
            turn = Cardinal(char.selected, north=2) - directionOfAngle(degs=angleToCenter)
            char.set((char.selected + turn) % 4)
        elif event.type == MOUSEBUTTONUP:
            if event.button in ( 2, 3 ):
                pass
                
    pygame.display.update()
    fpsClock.tick(30)

