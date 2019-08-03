import pygame
from gorgame import basics

class Space:
    def __init__(self, size):
        if isinstance(size, basics.Coords):
            self.size = size
        else:
            self.size = basics.Coords(size)
        self.walls = []
        self.agents = []

    def add_wall(self, start, end, thickness, colour):
        self.walls.append(Wall(start, end, thickness, colour))

    def add_agent(self, loc, radius, colour):
        self.agents.append(Agent(loc, radius, colour))

class Wall:
    def __init__(self, start, end, thickness, colour):
        if isinstance(start, basics.Coords):
            self.start = start
            self.end = end
        else:
            self.start = basics.Coords(start)
            self.end = basics.Coords(end)
        self.thickness = thickness
        self.colour = colour

class Agent:
    def __init__(self, loc, radius, colour):
        if isinstance(loc, basics.Coords):
            self.loc = loc
        else:
            self.loc = basics.Coords(loc)
        self.radius = radius
        self.colour = colour
