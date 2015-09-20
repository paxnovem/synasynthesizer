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
    ['A#', 'B', 'B'],
    ['G#', 'A', 'A#'],
    ['F#', 'G', 'G#'],
    ['F', 'F', 'F#'],
    ['D#', 'E', 'E'],
    ['C#', 'D', 'D#'],
    ['C', 'C', 'C#'],
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
            note = notes[x_index][y_index]

            print("x = " + str(x) + " y = " + str(y))
            print("[" + str(x_index) + "][" + str(y_index) + "]")
            print(note)
            
            if len(note):
                fluidsynth.play_Note(Note(note, octave), channel, 100)
            y = y + 3
            
            if y >= 9:
                x = x + 8
                y = 0
            
    tick += 0.001
pygame.quit()