import pygame
from enum import Enum

#CONSTANTS
#COLORS
colours = {
    "green": (0, 220, 0),
    "blue": (0, 0, 255),
    "red": (255, 0, 0),
    "grey": (127, 127, 127),
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "yellow": (255, 255, 0),
    "pink": (255, 0, 255),
    "teal": (0, 255, 255),
    "dark_blue": (0, 0, 127),
    "dark_teal": (0, 127, 127),
    "dark_red": (127, 0, 0),
    "dark_green": (0, 110, 0),
    "purple": (127, 0, 127),
}

class Screen:
    def __init__(self, size):
        self.clock = pygame.time.Clock()
        pygame.init()
        self.display = pygame.display.set_mode(size)
        pygame.display.set_caption("Game")
        self.window = Window([0,0], [size[0], size[1]], colours["black"], 0, "main window")

    def loop(self):
        self.event_handle()
        self.draw()
        self.clock.tick(30)

    def event_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

    def draw(self):
        self.window.draw(self.display, Coords([0,0]), self.window.size)

        pygame.display.update()

    def quit(self):
        pygame.quit()
        quit()

class Window:
    def __init__(self, loc, size, colour, height, name):
        self.loc = Coords([loc[0], loc[1]])
        self.size = Coords([size[0], size[1]])
        self.colour = colour
        self.height = height
        self.windows = []
        self.name = name

    def add_window(self, loc, size, colour, height, name):
        self.windows.append(Window(loc, size, colours[colour], height, name))
        self.sort_windows()

    def sort_windows(self):
        self.windows = sorted(self.windows, key = lambda x: x.height)

    def get(self, name):
        for window in self.windows:
            if window.name == name:
                return window

    def draw(self, display, delta, parent):
        if self.loc.x + self.size.x > parent.x:
            x_size = parent.x - self.loc.x
        else:
            x_size = self.size.x

        if self.loc.y + self.size.y > parent.y:
            y_size = parent.y - self.loc.y
        else:
            y_size = self.size.y

        if self.loc.x < 0:
            x_loc = delta.x
            x_size += self.loc.x
        else:
            x_loc = self.loc.x + delta.x

        if self.loc.y < 0:
            y_loc = delta.y
            y_size += self.loc.y
        else:
            y_loc = self.loc.y + delta.y
        display.fill(self.colour, (x_loc, y_loc, x_size, y_size))
        
        for window in self.windows:
            window.draw(display, Coords([self.loc.x + delta.x, self.loc.y + delta.y]), self.size)

class Coords:
    def __init__(self, loc):
        self.x = loc[0]
        self.y = loc[1]
