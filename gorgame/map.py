import pygame
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
                this_data.append(0)
        return this_data
