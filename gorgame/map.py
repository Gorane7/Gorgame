import pygame
import random
from gorgame import basics

class Map:
    def __init__(self, size):
        self.data = self.make_empty(size)

    def make_empty(self, size):
        this_data = []
        for i in range(size[0]):
            if len(size) > 1:
                this_data.append(self.make_empty(size[1:]))
            else:
                this_data.append({})
        return this_data

    def fill_random(self, name, min, max, array = None):
        if not array:
            array = self.data
        for i in range(len(array)):
            if isinstance(array[i], list):
                self.fill_random(name, min, max, array[i])
            else:
                array[i][name] = random.uniform(min, max)
