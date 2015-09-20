#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from mingus.core import notes, chords
from mingus.containers import *
from mingus.midi import fluidsynth
from os import sys

SF2 = 'soundfont.sf2'
octave = 4
channel = 8
quit = False
tick = 0
notes = [
    ['B', 'B', 'A#'],
    ['A#', 'A', 'G#'],
    ['G#', 'G', 'F#'],
    ['F#', 'F', 'F'],
    ['E', 'E', 'D#'],
    ['D#', 'D', 'C#'],
    ['C#', 'C', 'C'],
    ['', '', ''],
    ['', '', '']
]

if not fluidsynth.init(SF2):
    print "Couldn't load soundfont", SF2
    sys.exit(1)
    
pygame.init()
pygame.font.init()

font = pygame.font.SysFont('monospace', 12)
screen = pygame.display.set_mode((640, 480))
x = 0
y = 0

while not quit:
    for event in pygame.event.get():
        if event.type == QUIT:
            quit = True
        if event.type == KEYUP:
            y_index = int((y % 9) / 3)
            x_index = int((71 - x) / 8)

            print("x = " + str(x) + " y = " + str(y))
            print("[" + str(x_index) + "][" + str(y_index) + "]")
            print(notes[x_index][y_index])
            # fluidsynth.play_Note(Note('A#', octave), channel, 100)
            x = x + 1
            y = y + 1
            
    tick += 0.001
pygame.quit()