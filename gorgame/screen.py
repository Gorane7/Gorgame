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
        self.mouse_pos = Coords([0, 0])
        self.current_window = None
        self.current_scrollable = None

    def loop(self):
        self.event_handle()
        self.draw()
        self.clock.tick(30)

    def event_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = Coords([event.pos[0], event.pos[1]])
                self.current_window = self.window.get_current_window(self.mouse_pos)
                self.current_scrollable = self.window.get_current_window(self.mouse_pos, scrollable = True)

    def draw(self):
        self.window.draw(self.display, Coords([0,0]), self.window.size)

        pygame.display.update()

    def quit(self):
        pygame.quit()
        quit()

class Window:
    def __init__(self, loc, size, colour, height, name, scrollable = False):
        self.loc = Coords([loc[0], loc[1]])
        self.size = Coords([size[0], size[1]])
        self.colour = colour
        self.height = height
        self.windows = []
        self.name = name
        self.text = None
        self.text_colour = None
        self.scrollable = scrollable

    def add_window(self, loc, size, colour, height, name, scrollable = False):
        self.windows.append(Window(loc, size, colours[colour], height, name, scrollable = scrollable))
        self.sort_windows()

    def add_text(self, text, colour):
        self.text = text
        self.text_colour = colours[colour]

    def sort_windows(self):
        self.windows = sorted(self.windows, key = lambda x: x.height)

    def get(self, name):
        for window in self.windows:
            if window.name == name:
                return window

    def get_current_window(self, pos, scrollable = False):
        for window in reversed(self.windows):
            if (scrollable and window.scrollable) or not scrollable:
                if window.contains(pos):
                    return window.get_current_window(Coords([pos.x - window.loc.x, pos.y - window.loc.y]), scrollable = scrollable)
        if self.name == "main window":
            return None
        return self

    def contains(self, pos):
        if pos.x > self.loc.x and pos.x < self.loc.x + self.size.x and pos.y > self.loc.y and pos.y < self.loc.y + self.size.y:
            return True
        return False

    def __str__(self):
        return self.name

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

        if self.text:
            font = pygame.font.SysFont("arial", 200)
            text_surf = font.render(self.text, True, self.text_colour)
            x_per_letter = int(x_size / (len(self.text) * 0.75))
            text_size = min(y_size, x_per_letter)
            text_surf = pygame.transform.scale(text_surf, (int(len(self.text) * text_size * 0.75), text_size))
            x_text = x_loc + (x_size - text_surf.get_width()) // 2
            y_text = y_loc + (y_size - text_surf.get_height()) // 2
            display.blit(text_surf, (x_text, y_text))

        for window in self.windows:
            window.draw(display, Coords([self.loc.x + delta.x, self.loc.y + delta.y]), self.size)

class Coords:
    def __init__(self, loc):
        self.x = loc[0]
        self.y = loc[1]
