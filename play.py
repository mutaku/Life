#!/usr/bin/env python

import sys
import pygame
from pygame.locals import *

# user set items
DEAD_COLOR = "WHITE"
ALIVE_COLOR = "BLUE"
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# window shit
pygame.init()
DS = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
pygame.display.set_caption('I CAN HAZ INTELLIGENCE?')
SCREEN = pygame.display.get_surface()
WIDTH = DS.get_width()
HEIGHT = DS.get_height()
pygame.key.set_repeat(500, 10)

# some important numbers
BOXSIZE = 10

# some colors
COLORS = {
    'BLACK': (0, 0, 0),
    'WHITE': (255, 255, 255),
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 0, 255)
    }
DS.fill(COLORS['WHITE'])
ALIVE = {0: COLORS[DEAD_COLOR], 1: COLORS[ALIVE_COLOR]}

# coordinates and such
mousex, mousey = 0, 0
leftclicked, rightclicked = False, False

# this is our grid - (LEFT, TOP) : STATE
grid = {}
# this is our state change array
changestate = []

class Box():
    def __init__(self, square=False):
        if square:
            self.x, self.y = self.translate(square)
        else:
            pass
    def translate(self, s):
        return (rounder(s[0]), rounder(s[1]))

def m(*args):
    sys.stdout.write("\r\x1b[K"+" ".join([str(x) for x in args]))
    sys.stdout.flush()

def buildrects():
    # rect is declared left,top,width,height
    rects = [(j, k, BOXSIZE, BOXSIZE)
            for j in range(0, WIDTH, BOXSIZE)
            for k in range(0, HEIGHT, BOXSIZE)]
    return rects

def mapping(box):
    x, y = box
    zone = list(
            (j+WIDTH if j == -BOXSIZE else (j-WIDTH if j == WIDTH else j),
                k+HEIGHT if k == -BOXSIZE else (k-HEIGHT if k == HEIGHT else k))
                for j in range(x-BOXSIZE, x+2*BOXSIZE, BOXSIZE)
                for k in range(y-BOXSIZE, y+2*BOXSIZE, BOXSIZE)
                )
    zone.remove((x, y))
    return zone

def surrounds(box):
    alivetotal = 0
    for i in mapping(box):
        if isactive(i):
            alivetotal += 1
    return alivetotal

def amialive(box):
    n = surrounds(box)
    if 2 <= n <= 3 and isactive(box) or n == 3 and not isactive(box):
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

def togglebox(x, y):
    box = Box((x, y))
    if isactive((box.x, box.y)):
        grid[(box.x, box.y)] = (0, 0)
        event = "Died!"
    else:
        grid[(box.x, box.y)] = (1, 0)
        event = "is Born!"
    changecolor(box, n=0)
    m(box.x, box.y, event)

def setupgrid():
    for r in buildrects():
        grid[(r[0], r[1])] = (0, 0)
        pygame.draw.rect(SCREEN, COLORS['BLACK'], r, 1)
    m("* Grid built")

def changecolor(box, n=0):
    # dimensions are 1 px smaller all around so we don't lose our border
    SCREEN.fill(ALIVE[grid[(box.x, box.y)][n]],
            (box.x+1, box.y+1, BOXSIZE-2, BOXSIZE-2))

def runsimulation(f):
    def checkrun():
        if len(changestate) >= 3 and changestate[-3] == changestate[-1]:
            m(len(changestate), " state changes - stuck oscillating.")
        elif not len(changestate) or changestate[-1]:
            f()
        else:
            m(len(changestate), " state changes - finished.")
    return checkrun

@runsimulation
def simulate():
    if not len(changestate):
        array = grid
    else:
        array = []
        array.extend(changestate[-1])
        for box in changestate[-1]:
            array.extend(mapping(box))
        array = list(set(array))

    for square in array:
        nextturn(square)
    changestate.append([])
    for square in array:
        makechanges(square)

def nextturn(square):
    if amialive(square):
        grid[square] = (grid[square][0], 1)
    else:
        grid[square] = (grid[square][0], 0)
    box = Box(square)
    changecolor(box, n=1)

def makechanges(square):
    if grid[square][0] != grid[square][1]:
        changestate[-1].append(square)
    grid[square] = (grid[square][1], 0)

def printstate():
    # this is just for debugging
    m(len(changestate), ' state changes, last two changes : ', changestate[-2:])

def clear(keep=False):
    if not keep:
        for square in grid:
            grid[square] = (0, 0)
            box = Box(square)
            changecolor(box)
    del changestate[:]
    m("* Grid reset")

def exit():
    pygame.quit()
    m()
    sys.exit()

# setup some things
setupgrid()

# game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type == MOUSEMOTION:
            mousex, mousey = event.pos
        elif event.type == KEYDOWN and pygame.key.name(event.key) == "q":
            exit()
        elif event.type == MOUSEBUTTONDOWN:
            mousex, mousey = event.pos
            if pygame.mouse.get_pressed()[0] == 1:
                leftclicked = True
            else:
                rightclicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            leftclicked, rightclicked = False, False
        elif event.type == KEYDOWN and pygame.key.name(event.key) == "c":
            clear()
        elif event.type == KEYDOWN and pygame.key.name(event.key) == "k":
            clear(keep=True)
        elif event.type == KEYDOWN and pygame.key.name(event.key) == "p":
            printstate()
        elif event.type == KEYDOWN and pygame.key.name(event.key) == "r":
            simulate()

        if leftclicked:
            togglebox(mousex, mousey)
        if rightclicked:
            rightclicked = False
            simulate()

    pygame.display.update()
