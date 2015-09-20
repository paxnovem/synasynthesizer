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

from sensor_interface import SensorInterface
from utils import *

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

                x, y = point

                y_index = int((y % 9) / 3)
                x_index = int((71 - x) / 8)
                note = notes[x_index][y_index]

                print("x = " + str(x) + " y = " + str(y))
                print("[" + str(x_index) + "][" + str(y_index) + "]")
                print(note)

                if len(note):
                    fluidsynth.play_Note(Note(note, octave), channel, 100)

    tick += 0.001

sensor.close()
pygame.quit()