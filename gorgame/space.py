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
        self.default_agent_radius = 0.5
        self.default_faction = None
        self.default_colour = "black"
        self.default_vision_radius = 10
        self.default_wall_thickness = 1.0
        self.default_wall_colour = "brown"
        self.faction_stats = {}

    def add_wall(self, start, end, thickness = None, colour = None):
        if not thickness:
            thickness = self.default_wall_thickness
        if not colour:
            colour = self.default_wall_colour
        self.walls.append(Wall(start, end, thickness, colour))

    def add_agent(self, loc, radius = None, colour = None, faction = None, vision_radius = None):
        if not faction:
            faction = self.default_faction
        if faction in self.faction_stats.keys():
            if "agent_radius" in self.faction_stats[faction]:
                radius = self.faction_stats[faction]["agent_radius"]
            if "colour" in self.faction_stats[faction]:
                colour = self.faction_stats[faction]["colour"]
            if "vision_radius" in self.faction_stats[faction]:
                vision_radius = self.faction_stats[faction]["vision_radius"]
        if not radius:
            radius = self.default_agent_radius
        if not colour:
            colour = self.default_colour
        if not vision_radius:
            vision_radius = self.default_vision_radius
        self.agents.append(Agent(loc, radius, colour, faction, vision_radius))

    def add_faction_stats(self, faction, agent_radius = None, colour = None, vision_radius = None):
        self.faction_stats[faction] = {}
        if agent_radius:
            self.faction_stats[faction]["agent_radius"] = agent_radius
        if colour:
            self.faction_stats[faction]["colour"] = colour
        if vision_radius:
            self.faction_stats[faction]["vision_radius"] = vision_radius

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
    def __init__(self, loc, radius, colour, faction, vision_radius):
        if isinstance(loc, basics.Coords):
            self.loc = loc
        else:
            self.loc = basics.Coords(loc)
        self.radius = radius
        self.colour = colour
        self.faction = faction
        self.vision_radius = vision_radius
