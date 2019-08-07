import pygame
import random
from gorgame import basics

class Map:
    def __init__(self, size):
        self.tiles = self.make_empty_tiles(size)

    def make_empty_tiles(self, size):
        this_data = []
        for i in range(size[0]):
            if len(size) > 1:
                this_data.append(self.make_empty_tiles(size[1:]))
            else:
                this_data.append({})
        return this_data

    def fill_random_tiles(self, name, min, max, array = None):
        if not array:
            array = self.tiles
        for i in range(len(array)):
            if isinstance(array[i], list):
                self.fill_random_tiles(name, min, max, array = array[i])
            else:
                array[i][name] = random.uniform(min, max)

    def fill_chessboard_pattern(self, array = None, current = 0):
        if not array:
            array = self.tiles
        for i in range(len(array)):
            if isinstance(array[i], list):
                self.fill_chessboard_pattern(array = array[i], current = current + i)
            else:
                if (current + i) % 2 == 0:
                    array[i]["rgb"] = [0, 0, 0]
                else:
                    array[i]["rgb"] = [255, 255, 255]
