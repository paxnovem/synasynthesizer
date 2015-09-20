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

x = 0
y = 0

from sensor_interface import SensorInterface
from utils import *

from vispy import app
import vis
import random

app.set_interactive()

canvas = vis.Canvas()
canvas.show()

RED = (0.9, 0.1, 0.1, )
ORANGE = (0.9, 0.5, 0.1, )
YELLOW = (0.9, 0.9, 0.1, )
GREEN = (0.1, 0.9, 0.1, )
TEAL = (0.1, 0.9, 0.5, )
BLUE = (0.1, 0.1, 0.9, )
INDIGO = (0.5, 0.1, 0.9, )
PURPLE = (0.9, 0.1, 0.9, )

sensor = SensorInterface()
sensor.connect()

import time
time.sleep(1)

while True:
    baseline_image = sensor.getAllImages()

    if baseline_image:
        baseline_image = baseline_image[-1]
        break

baseline_data = baseline_image["image"]

while not quit:
    for event in pygame.event.get():
        if event.type == QUIT:
            quit = True

    '''
    time.sleep(0.5)

    y_index = int((y % 9) / 3)
    x_index = int((71 - x) / 8)
    note = notes[x_index][y_index]

    print("x = " + str(x) + " y = " + str(y))
    print("[" + str(x_index) + "][" + str(y_index) + "]")
    print(note)

    if len(note):
        fluidsynth.play_Note(Note(note, octave), channel, 100)

        color = [RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, PURPLE][x_index]
        location = (
            x_index / 7.0,
            y_index / 5.0,
            0.0
        )

        canvas._new_explosion(color, location)

    y = y + 3

    if y >= 9:
        x = x + 8
        y = 0
    '''

    images = sensor.getAllImages()

    if images:
        image = images[-1]
        image_data = image["image"]

        delta_data = delta_from_baseline(image_data, baseline_data)

        all_visited_list = set()

        for row_number in range(len(delta_data)):
            row = delta_data[row_number]
            for column_number in range(len(row)):
                visited_list = []
                point = (row_number, column_number)

                if point in all_visited_list:
                    continue

                find_touch_area(delta_data, point, 50, visited_list)
                touch_area = touch_area_from_visited(visited_list)

                if touch_area is None:
                    continue

                all_visited_list.update(visited_list)

                touch_point = touch_area_midpoint(*touch_area)

                print(point, touch_point)

                y, x = point

                y_index = int((y % 9) / 3)
                x_index = int((71 - x) / 8)
                note = notes[x_index][y_index]

                print("x = " + str(x) + " y = " + str(y))
                print("[" + str(x_index) + "][" + str(y_index) + "]")
                print(note)

                if len(note):
                    fluidsynth.play_Note(Note(note, octave), channel, 100)

                canvas._new_explosion(random.choice([ORANGE, RED, GREEN, BLUE]))

sensor.close()
pygame.quit()