#/usr/bin/env python3
import pygame, sys
from pygame.locals import *
from classes import PackagedSprite
from random import randint
import math
import formulae

pygame.init()
fpsClock = pygame.time.Clock()

dimensions = (1024, 768)
screen = pygame.display.set_mode(dimensions)
background = pygame.Surface(dimensions)
black = pygame.Color(0, 0, 0)
mousex, mousey = 0, 0
pygame.mouse.set_visible(False)

char = PackagedSprite('rachel', 4)
pie = PackagedSprite('applePie', 2)

def randomPlace():
    return ( randint(0, dimensions[0]), randint(0, dimensions[1]) )

def newPos(object):
    pos = randomPlace()
    while not object.isOnScreen(pos, dimensions):
        pos = randomPlace()
    return pos

piePos = newPos(pie)

# TODO figure out how rachel can constantly look at the pie

while True:
    screen.fill(black)
    screen.blit(background, (0, 0))
    screen.blit(pie.pygameObject, piePos)
    screen.blit(char.pygameObject, (mousex, mousey))
    if formulae.distance((mousex, mousey), pie.getCenterpoint(piePos)) < 75:
        pie.next()
        piePos = newPos(pie)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            mousex, mousey = event.pos
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                char.next()
            elif event.button in ( 2, 3 ):
                pie.next()
                piePos = newPos(pie)
                
    pygame.display.update()
    fpsClock.tick(30)

