#!/usr/bin/env python

import sys
import itertools
import pygame
from pygame.locals import *

# window shit
pygame.init()
DS = pygame.display.set_mode((400, 400), 0, 32)
pygame.display.set_caption('I CAN HAZ INTELLIGENCE?')
SCREEN = pygame.display.get_surface()
WIDTH = DS.get_width()
HEIGHT = DS.get_height()


# some important numbers
ALTER = 5
BOXSIZE = 10
FPS = 15
fpsClock = pygame.time.Clock()


# some colors
COLORS = {
    'BLACK': (0, 0, 0),
    'WHITE': (255, 255, 255),
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 0, 255)
    }
DS.fill(COLORS['WHITE'])
ALIVE = {0: COLORS['WHITE'], 1: COLORS['BLUE']}

# coordinates and such
mousex, mousey = 0, 0
leftclicked, rightclicked = False, False

# this is our grid - (LEFT, TOP) : STATE
grid = {}


class Box():
    def __init__(self):
        pass

def m(*args):
    for a in args:
        print a,
    print

def buildrects():
    # rect is declared left,top,width,height
    rects = [(j, k, BOXSIZE, BOXSIZE)
            for j in range(0, WIDTH, BOXSIZE)
            for k in range(0, HEIGHT, BOXSIZE)]
    return rects

def surrounds(box):
    x, y = box
    alivetotal = 0
    mapping = list(
            (j+WIDTH if j == -BOXSIZE else (j-WIDTH if j == WIDTH else j),
                k+HEIGHT if k == -BOXSIZE else (k-HEIGHT if k == HEIGHT else k))
                for j in range(x-BOXSIZE, x+2*BOXSIZE, BOXSIZE)
                for k in range(y-BOXSIZE, y+2*BOXSIZE, BOXSIZE)
                )
    mapping.remove((x, y))
    for i in mapping:
        if isactive(i):
            alivetotal += 1
    return alivetotal

def amialive(box):
    n = surrounds(box)
    if 2 <= n <=3:
        return True
    else:
        return False

def rounder(n, base=BOXSIZE):
    # always down
    return int((n/base)*base)

def isactive(box):
    if grid[box][0] == 1:
        return True
    else:
        return False

def translate(x, y):
    box = Box()
    box.x, box.y = rounder(x), rounder(y)
    return box

def togglebox(x, y):
    box = translate(x, y)
    if grid[(box.x, box.y)][0]:
        grid[(box.x, box.y)] = (0, 0)
        event = "died"
    else:
        grid[(box.x, box.y)] = (1, 0)
        event = "is born"
    changecolor(box, n=0)
    m(box.x, box.y, event, amialive((box.x, box.y)))

def hoverstatus(x, y):
    # this is slightly redundant but mainly for testing only
    box = translate(x, y)
    m(box.x, box.y, 'next turn ->', amialive((box.x, box.y)))

def setupgrid():
    for r in buildrects():
        grid[(r[0], r[1])] = (0, 0)
        pygame.draw.rect(SCREEN, COLORS['BLACK'], r, 1)
    m("* Grid built")

def changecolor(box, n=0):
    # dimensions are 1 px smaller all around so we don't lose our border
    SCREEN.fill(ALIVE[grid[(box.x, box.y)][n]],
            (box.x+1, box.y+1, BOXSIZE-2, BOXSIZE-2))

def simulate():
    for square in grid:
        if amialive(square):
            grid[square] = (grid[square][0], 1)
        else:
            grid[square] = (grid[square][0], 0)
        box = Box()
        box.x, box.y = square
        changecolor(box, n=1)
    for square in grid:
        grid[square] = (grid[square][1], 0)

# setup some things
setupgrid()

# game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            mousex, mousey = event.pos

        elif event.type == MOUSEBUTTONDOWN:
            mousex, mousey = event.pos
            if pygame.mouse.get_pressed()[0] == 1:
                leftclicked = True
            else:
                rightclicked = True

        if leftclicked:
            leftclicked = False
            togglebox(mousex, mousey)
        elif rightclicked:
            #hoverstatus(mousex, mousey)
            rightclicked = False
            simulate()

    pygame.display.update()
    fpsClock.tick(FPS)