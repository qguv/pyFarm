#/usr/bin/env python3
import pygame, sys
from pygame.locals import *
from classes import *
from random import randint
import math
from formulae import *

pygame.init()
fpsClock = pygame.time.Clock()

dimensions = (1024, 768)
screen = pygame.display.set_mode(dimensions)
background = pygame.Surface(dimensions)
black = pygame.Color(0, 0, 0)
mousex, mousey = 1, 1
pygame.mouse.set_visible(False)

char = PackagedSprite('rachelSmall', 4)
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

angleToPie = angle(char.getCenterpoint((mousex, mousey)), pie.getCenterpoint(piePos))
turn = Cardinal(char.selected, north=2) - directionOfAngle(degs=angleToPie)
char.set((char.selected + turn) % 4)

buildBackground(floorTile, background, dimensions)

font = pygame.font.Font('fonts/DroidSans.ttf', 36)
text = font.render("no pies!", 1, (200, 200, 200))
textRectobj = text.get_rect()
textRectobj.topleft = (10, 20)
screen.blit(text, textRectobj)

while True:
    screen.fill(black)
    screen.blit(background, (0, 0))

    screen.blit(text, textRectobj)

    screen.blit(char.pygameObject, (mousex, mousey))
    screen.blit(pie.pygameObject, piePos)

    if distance((mousex, mousey), pie.getCenterpoint(piePos)) < 75:
        pies += 1
        if pies == 1:
            text = font.render("1 pie!", 1, (255, 255, 255))
        else:
            text = font.render(str(pies) + " pies!", 1, (255, 255, 255))
        pie.next()
        piePos = newPos(pie)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            mousex, mousey = event.pos
            angleToPie = angle((mousex, mousey), pie.getCenterpoint(piePos))
            print(angleToPie) #DEBUG
            turn = Cardinal(char.selected, north=2) - directionOfAngle(degs=angleToPie)
            char.set((char.selected + turn) % 4)
        elif event.type == MOUSEBUTTONUP:
            if event.button in ( 2, 3 ):
                pie.next()
                piePos = newPos(pie)
                pies = 0
                text = font.render("no pies!", 1, (200, 200, 200))
                
    pygame.display.update()
    fpsClock.tick(30)

