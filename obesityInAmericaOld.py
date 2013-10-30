#/usr/bin/env python3
import pygame, sys
from pygame.locals import *
from classesOld import *
from random import randint
import math
from formulaeOld import *

pygame.init()
fpsClock = pygame.time.Clock()

dimensions = (1024, 768)
screen = pygame.display.set_mode(dimensions)
background = pygame.Surface(dimensions)
black = pygame.Color(0, 0, 0)
mousex, mousey = dimensions
pygame.mouse.set_visible(False)

char = PackagedSprite('rachel', 4)
pie = PackagedSprite('applePie', 2)
floorTile = PackagedSprite('floor', 1)

def randomPlace():
    return ( randint(0, dimensions[0]), randint(0, dimensions[1]) )

def newPos(object):
    pos = randomPlace()
    while not object.isOnScreen(pos, dimensions):
        pos = randomPlace()
    return pos

def buildBackground(tile, background, dimensions):
    maxX, maxY = dimensions
    dx, dy = tile.dimensions
    for y in range(0, maxY, dy):
        for x in range(0, maxX, dx):
            background.blit(tile.pygameObject, (x, y))

piePos = newPos(pie)
pies = 0

charSize = char.dimensions

angleToPie = angle(centerpoint((mousex, mousey), charSize), pie.getCenterpoint(piePos))
turn = Cardinal(char.selected, north=2) - directionOfAngle(degs=angleToPie)
char.set((char.selected + turn) % 4)

buildBackground(floorTile, background, dimensions)

font = pygame.font.Font('fonts/DroidSans.ttf', 36)
countText = font.render("no pies!", 1, (200, 200, 200))
countTextRectobj = countText.get_rect()
countTextRectobj.topleft = (10, 20)
screen.blit(countText, countTextRectobj)

warningText1 = font.render("do not eat more pie!", 1, (200, 200, 0))
warningTextRectobj = warningText1.get_rect()
warningTextRectobj.topleft = (300, 20)

warningText2 = font.render("do not eat more pie!", 1, (200, 0, 200))

warningText3 = font.render("obesity in America!", 1, (255, 50, 50))
warningText4 = font.render("obesity in America!", 1, (255, 255, 255))
warningText5 = font.render("obesity in America!", 1, (100, 100, 255))

while True:
    screen.fill(black)
    if pies < 50:
        screen.blit(background, (0, 0))

        screen.blit(countText, countTextRectobj)

        if pies > 35:
            if pies % 3 == 0:
                screen.blit(warningText5, warningTextRectobj)
            elif pies % 3 == 1:
                screen.blit(warningText3, warningTextRectobj)
            else:
                screen.blit(warningText4, warningTextRectobj)
        elif pies > 25:
            if pies % 2 == 0:
                screen.blit(warningText1, warningTextRectobj)
            else:
                screen.blit(warningText2, warningTextRectobj)

        screen.blit(pie.pygameObject, piePos)
        charMid = centerpoint((mousex, mousey), charSize)
        screen.blit(
                pygame.transform.scale(char.pygameObject, (charSize)),
                (mousex, mousey))
    else:
        deathTextRectobj = warningText1.get_rect()
        deathTextRectobj.topleft = centerpoint((0, 0), dimensions)
        screen.blit(warningText3, deathTextRectobj)

    if distance(centerpoint((mousex, mousey), charSize), pie.getCenterpoint(piePos)) < 75:
        pies += 1
        if pies == 1:
            countText = font.render("1 pie!", 1, (255, 255, 255))
        else:
            countText = font.render(str(pies) + " pies!", 1, (255, 255, 255))
        pie.next()
        piePos = newPos(pie)
        charSize = tuple( int(x * 1.03) for x in charSize )
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            mousex, mousey = event.pos
            angleToPie = angle((mousex, mousey), pie.getCenterpoint(piePos))
            turn = Cardinal(char.selected, north=2) - directionOfAngle(degs=angleToPie)
            char.set((char.selected + turn) % 4)
        elif event.type == MOUSEBUTTONUP:
            if event.button in ( 2, 3 ):
                pie.next()
                piePos = newPos(pie)
                pies = 0
                text = font.render("no pies!", 1, (200, 200, 200))
                charSize = char.dimensions
                
    pygame.display.update()
    fpsClock.tick(30)

