#/usr/bin/env python3

# Library Imports
import pygame, sys, math
import random

# The following are explicitly import-star safe
from pygame.locals import *
from classes import *
from formulae import *

# Environment variables
dimensions = Point(1024, 768)

# Setting environment
pygame.init()
fpsClock = pygame.time.Clock()
pygame.mouse.set_visible(True)
screen = pygame.display.set_mode(dimensions)
background = pygame.Surface(dimensions)

# Color sugar
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
lightGrey = pygame.Color(200, 200, 200)

# Display sugar
topLeft = Point(0, 0)
bottomRight = dimensions
midScreen = dimensions // 2

# Position functions
def randomPlace():
    maxX, maxY = dimensions
    return Point(random.randint(0, maxX), random.randint(0, maxY))

def newPos(object):
    pos = randomPlace()
    while not object.isOnScreen(pos, dimensions):
        pos = randomPlace()
    return pos

def buildBackground(tile, background, dimensions : Point):
    maxX, maxY = dimensions
    dx, dy = tile.dimensions
    for y in range(0, maxY, dy):
        for x in range(0, maxX, dx):
            background.blit(tile.pygameObject, Point(x, y))

# Sprites
char = PackagedSprite('rachel', 4)
pie = PackagedSprite('applePie', 2)
flora0 = PackagedSprite("flora", 99)
flora1 = PackagedSprite("flora", 99)
flora2 = PackagedSprite("flora", 99)
floorTile = PackagedSprite('floor', 1)

# Set flora sprites to random plants
plants = random.sample(range(len(flora0.paths)), 3)
flora0.set(plants[0])
flora1.set(plants[1])
flora2.set(plants[2])

# Positions and Counters
pies = 0
keylength = 0
keydown = False
keydirection = None
choice = None
repick = True
repick_timeout = pygame.time.Clock()
repick_timeout.tick()
mousePos = Point(1, 1)
char_pos = mousePos - char.dimensions / 2
floraX = midScreen[0] - flora0.dimensions[0] / 2
floraY = midScreen[1] - flora0.dimensions[1] / 2
floraXStep = dimensions[0] / 5
flora0_pos = Point(floraX - floraXStep, floraY)
flora1_pos = Point(floraX, floraY)
flora2_pos = Point(floraX + floraXStep, floraY)

# Messages
font = pygame.font.Font('fonts/DroidSans.ttf', 36)

def buildCount(count):
    if count == 0:
        msg = 'no pies'
    elif count == 1:
        msg = 'one pie'
    else:
        msg = str(count) + ' pies'
    return font.render(msg + '!', 1, (200, 200, 200))

# Pie Count
countText = buildCount(pies)
countTextRectobj = countText.get_rect()
countTextRectobj.topleft = (10, 20)

buildBackground(floorTile, background, dimensions)

flora0_center = flora0.getCenterpoint(flora0_pos)
flora1_center = flora0.getCenterpoint(flora1_pos)
flora2_center = flora0.getCenterpoint(flora2_pos)

screen.fill(black)

while True:
    # Calculate position data
    char_center = char.getCenterpoint(char_pos)

    if char_center.distance(flora0_center) < 50:
        choice = 0
        repick = True
    elif char_center.distance(flora1_center) < 50:
        choice = 1
        repick = True
    elif char_center.distance(flora2_center) < 50:
        choice = 2
        repick = True

    # Draw objects to screen
    screen.blit(background, topLeft)
    #screen.blit(countText, countTextRectobj)
    screen.blit(flora0.pygameObject, flora0_pos)
    screen.blit(flora1.pygameObject, flora1_pos)
    screen.blit(flora2.pygameObject, flora2_pos)
    screen.blit(char.pygameObject, char_pos)

    # Handle UI events
    for event in pygame.event.get():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_q:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            keydown = True
            keydirection = event.key
        elif event.type == KEYUP and keydirection == event.key:
            keydown = False
        elif event.type == MOUSEBUTTONUP:
            repick = True

    # Handle status events
    if keydown:
        if keydirection == K_UP:
            char_pos += (0, -20)
        elif keydirection == K_DOWN:
            char_pos += (0, 20)
        elif keydirection == K_LEFT:
            char_pos += (-20, 0)
        elif keydirection == K_RIGHT:
            char_pos += (20, 0)
        angleToCenter = Angle(char_center.angle(flora1_center))
        if angleToCenter.cardinal() != char.selected:
            char.set(angleToCenter.cardinal())
                
    if repick: 
        repick_timeout.tick()
        repick = False
        if repick_timeout.get_time() > 100:
            plants = random.sample(range(len(flora0.paths)), 3)
            flora0.set(plants[0])
            flora1.set(plants[1])
            flora2.set(plants[2])

    pygame.display.update()
    fpsClock.tick(30)
