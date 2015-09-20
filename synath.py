#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from mingus.core import notes, chords
from mingus.containers import *
from mingus.midi import fluidsynth
from os import sys

SF2 = 'soundfont.sf2'

octave = 6
channel = 8
velocity = 50

quit = False

tick = 0
x = 0
y = 0

notes_played = set()

notes = [
    ['B', 'B', 'B'],
    ['A#', 'A', 'A'],
    ['G#', 'G', 'G'],
    ['F#', 'F', 'F'],
    ['E', 'E', 'E'],
    ['D#', 'D', 'D'],
    ['C#', 'C', 'C'],
    ['', '', ''],
    ['', '', '']
]

if not fluidsynth.init(SF2, "dsound"):
    print "Couldn't load soundfont", SF2
    sys.exit(1)

pygame.init()

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
    notes_playing = set()

    for event in pygame.event.get():
        if event.type == QUIT:
            quit = True

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

                y, x = point

                y_index = int((y % 9) / 3)
                x_index = int((71 - x) / 8)

                note = notes[x_index][y_index]

                print(note)

                if len(note):
                    notes_playing.add( (x_index, y_index, (octave - int(y/9))) )

                color = [
                    RED, ORANGE, YELLOW, GREEN, TEAL, BLUE, INDIGO, PURPLE, RED
                ][x_index]
                location = (
                    x_index / 7.0,
                    y_index / 5.0,
                    0.0
                )

                canvas._new_explosion(color, location)

        for coord in notes_playing:
            if coord not in notes_played:
                fluidsynth.midi.play_event(Note(notes[coord[0]][coord[1]], coord[2]), channel, velocity)
                notes_played.add(coord)

        for coord in set(notes_played):
            if coord not in notes_playing:
                notes_played.remove(coord)

sensor.close()
pygame.quit()