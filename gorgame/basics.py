import math

class Coords:
    def __init__(self, loc):
        self.x = loc[0]
        self.y = loc[1]

    def __str__(self):
        return str([self.x, self.y])

    def subtract(self, second_coords):
        self.x -= second_coords.x
        self.y -= second_coords.y

    def add(self, second_coords):
        self.x += second_coords.x
        self.y += second_coords.y

def dist(a, b):
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)
