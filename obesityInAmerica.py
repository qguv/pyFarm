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
pie = PackagedSprite('applePie', 2)
floorTile = PackagedSprite('floor', 1)

# Positions and Counters
pies = 0
fakePie = False
charSize = char.dimensions
mousePos = Point(1, 1)
piePos = newPos(pie)
charPos = mousePos - char.dimensions / 2

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

## Pie Count
countText = buildCount(pies)
countTextRectobj = countText.get_rect()
countTextRectobj.topleft = (10, 20)
screen.blit(countText, countTextRectobj)

## Warning text
warningTextYellow = font.render("do not eat more pie!", 1, (200, 200, 0))
warningTextMagenta = font.render("do not eat more pie!", 1, (200, 0, 200))
warningTextRectobj = warningTextYellow.get_rect()
warningTextRectobj.topleft = (300, 20)

## Obesity Text
obesityRed = font.render("obesity in America!", 1, (255, 50, 50))
obesityWhite = font.render("obesity in America!", 1, (255, 255, 255))
obesityBlue = font.render("obesity in America!", 1, (100, 100, 255))
obesityRectobj = obesityRed.get_rect()
obesityRectobj.topleft = (300, 20)

obesityDeath = font.render("obesity in America!", 1, (255, 50, 50))
obesityDeathRectobj = obesityDeath.get_rect()
obesityDeathRectobj.topleft = midScreen

buildBackground(floorTile, background, dimensions)

while True:
    screen.fill(black)
    screen.blit(background, topLeft)
    screen.blit(countText, countTextRectobj)

    if pies > 25:
        if pies > 35:
            if pies % 3 == 2:
                screen.blit(obesityRed, obesityRectobj)
            elif pies % 3 == 0:
                screen.blit(obesityWhite, obesityRectobj)
            else:
                screen.blit(obesityBlue, obesityRectobj)
        else:
            if pies % 2 == 1:
                screen.blit(warningTextYellow, warningTextRectobj)
            else:
                screen.blit(warningTextMagenta, warningTextRectobj)

    screen.blit(pie.pygameObject, piePos)
    screen.blit(pygame.transform.scale(char.pygameObject, charSize), charPos)

    if charPos.distance(piePos) < 70 or fakePie:
        piePos = newPos(pie)
        pies += 1
        countText = buildCount(pies)
        if pies > 35:
            charSizeMod = 1.05
        else:
            charSizeMod = 1.03
        charSize = math.trunc(charSize * charSizeMod)
        fakePie = False

    if pies > 49:
        screen.fill(black)
        screen.blit(obesityDeath, obesityDeathRectobj)
        pygame.mouse.set_visible(True)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            mousePos = Point(event.pos)
            charPos = mousePos - char.dimensions / 2
            angleToPie = Angle(charPos.angle(piePos))
            char.set(angleToPie.cardinal())
        elif event.type == MOUSEBUTTONUP:
            if event.button in ( 2, 3 ):
                fakePie = True
                
    pygame.display.update()
    fpsClock.tick(30)

