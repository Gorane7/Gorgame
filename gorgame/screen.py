import pygame
from gorgame import basics

#CONSTANTS
#COLORS
colours = {
    "green": [0, 220, 0],
    "blue": [0, 0, 255],
    "red": [255, 0, 0],
    "grey": [127, 127, 127],
    "black": [0, 0, 0],
    "white": [255, 255, 255],
    "yellow": [255, 255, 0],
    "pink": [255, 0, 255],
    "teal": [0, 255, 255],
    "dark_blue": [0, 0, 127],
    "dark_teal": [0, 127, 127],
    "dark_red": [127, 0, 0],
    "dark_green": [0, 110, 0],
    "purple": [127, 0, 127],
    "brown": [139, 69, 19]
}

class Screen:
    def __init__(self, size):
        self.display = pygame.display.set_mode(size)
        pygame.display.set_caption("Game")
        self.window = Window([0,0], [size[0], size[1]], colours["black"], 0, "main window")
        self.mouse_pos = basics.Coords([0, 0])
        self.current_entity = None
        self.current_window = None

    def draw(self):
        self.window.draw(self.display, basics.Coords([0,0]), self.window.size)
        pygame.display.update()

class Entity:
    def __init__(self, loc, size, colour, height, name):
        self.loc = basics.Coords([loc[0], loc[1]])
        self.size = basics.Coords([size[0], size[1]])
        self.colour = colour
        self.height = height
        self.name = name

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

        return basics.Coords([x_size, y_size]), basics.Coords([x_loc, y_loc])

class Spaceview(Entity):
    def __init__(self, loc, size, colour, height, name):
        Entity.__init__(self, loc, size, colour, height, name)
        self.zoom = 1.0
        self.space = None

    def add_space(self, space, ratio):
        self.space = space
        self.ratio = ratio
        self.centre = basics.Coords([0.0, 0.0])

class Gridview(Entity):
    def __init__(self, loc, size, colour, height, name):
        Entity.__init__(self, loc, size, colour, height, name)
        self.acc = 25
        self.zoom = 1.0
        self.grid = None

    def add_grid(self, grid):
        self.grid = grid
        self.centre = basics.Coords([len(self.grid) / 2, len(self.grid[0]) / 2])
        self.grid_size = basics.Coords([self.size.x / len(self.grid), self.size.y / len(self.grid[0])])
        self.tile_size = min(self.grid_size.x, self.grid_size.y)

    def centre_move(self, mouse_move):
        self.centre = self.centre.add(basics.Coords([ - mouse_move.x / (self.grid_size.x * self.zoom),  - mouse_move.y / (self.grid_size.y * self.zoom)]))

    def zoom_in(self):
        self.zoom *= 1.1

    def zoom_out(self):
        self.zoom /= 1.1

    def draw(self, display, delta, parent):
        size, loc = super().draw(display, delta, parent)

        if self.grid:
            surface = pygame.Surface((len(self.grid)*self.acc, len(self.grid[0])*self.acc))
            for i in range(len(self.grid)):
                for j in range(len(self.grid[i])):
                    colour = self.get_colour(self.grid[i][j])
                    surface.fill(colour, (i*self.acc, j*self.acc, self.acc, self.acc))

            x = len(self.grid)
            y = len(self.grid[0])
            surface = pygame.transform.scale(surface, (int(self.tile_size * x * self.zoom), int(self.tile_size * y * self.zoom)))
            #surface = pygame.transform.scale(surface, (int(self.size.x * self.zoom), int(self.size.y * self.zoom)))

            #determines what part of the map is visible
            x_left = self.centre.x - len(self.grid) / (2 * self.zoom)
            x_right = self.centre.x + len(self.grid) / (2 * self.zoom)
            y_top = self.centre.y - len(self.grid[0]) / (2 * self.zoom)
            y_bottom = self.centre.y + len(self.grid[0]) / (2 * self.zoom)
            if x_left < 0:
                x_left = 0
            if x_left > len(self.grid):
                x_left = len(self.grid)
            if x_right < 0:
                x_right = 0
            if x_right > len(self.grid):
                x_right = len(self.grid)
            if y_top < 0:
                y_top = 0
            if y_top > len(self.grid[0]):
                y_top = len(self.grid[0])
            if y_bottom < 0:
                y_bottom = 0
            if y_bottom > len(self.grid[0]):
                y_bottom = len(self.grid[0])

            tile_size_x = self.size.x * self.zoom / len(self.grid)
            tile_size_y = self.size.y * self.zoom / len(self.grid[0])
            #tile_size *= self.zoom

            x_size = int((x_right - x_left)*tile_size_x)
            y_size = int((y_bottom - y_top)*tile_size_y)
            #x_size = int((x_right - x_left) * tile_size)
            #y_size = int((y_bottom - y_top) * tile_size)

            x_left = x_left * tile_size_x
            y_top = y_top * tile_size_y
            x_right = x_right * tile_size_x
            y_bottom = y_bottom * tile_size_y
            #x_left = x_left * tile_size
            #y_top = y_top * tile_size
            #x_right = x_right * tile_size
            #y_bottom = y_bottom * tile_size

            #calculating delta due to zoom and pan
            if x_left == 0:
                d_x = self.size.x * (1 - self.zoom) / 2 + (len(self.grid) / 2 - self.centre.x) * tile_size_x
                #d_x = self.size.x * (1 - self.zoom) / 2 + (len(self.grid) / 2 - self.centre.x) * tile_size
            else:
                d_x = 0

            if y_top == 0:
                d_y = self.size.y * (1 - self.zoom) / 2 + (len(self.grid[0]) / 2 - self.centre.y) * tile_size_y
                #d_y = self.size.y * (1 - self.zoom) / 2 + (len(self.grid[0]) / 2 - self.centre.y) * tile_size
            else:
                d_y = 0
            new_delta = basics.Coords([d_x, d_y])

            new_surf = pygame.Surface((x_size, y_size))
            new_surf.fill(self.colour)
            new_surf.blit(surface, (0, 0), (x_left, y_top, x_size, y_size))

            display.blit(new_surf, (delta.x + loc.x + new_delta.x, delta.y + loc.y + new_delta.y))

    def get_colour(self, t_dict):
        if "red" in t_dict or "green" in t_dict or "blue" in t_dict:
            colour = [0, 0, 0]
            if "red" in t_dict:
                colour[0] = int(t_dict["red"]*256)
            if "green" in t_dict:
                colour[1] = int(t_dict["green"]*256)
            if "blue" in t_dict:
                colour[2] = int(t_dict["blue"]*256)
            return colour

class Textbox(Entity):
    def __init__(self, loc, size, colour, height, name):
        Entity.__init__(self, loc, size, colour, height, name)
        self.text = None
        self.text_colour = None

    def add_text(self, text, colour):
        self.text = text
        self.text_colour = colours[colour]

    def draw(self, display, delta, parent):
        size, loc = super().draw(display, delta, parent)

        if self.text:
            font = pygame.font.SysFont("arial", 200)
            text_surf = font.render(self.text, True, self.text_colour)
            x_per_letter = int(size.x / (len(self.text) * 0.75))
            text_size = min(size.y, x_per_letter)
            if text_size > 0:
                text_surf = pygame.transform.scale(text_surf, (int(len(self.text) * text_size * 0.75), text_size))
                x_text = loc.x + (size.x - text_surf.get_width()) // 2
                y_text = loc.y + (size.y - text_surf.get_height()) // 2
                display.blit(text_surf, (x_text, y_text))

class Window(Entity):
    def __init__(self, loc, size, colour, height, name):
        Entity.__init__(self, loc, size, colour, height, name)
        self.components = []

    def add_component(self, loc, size, colour, height, name, window = False, textbox = False, gridview = False, spaceview = False):
        if window:
            self.components.append(Window(loc, size, colours[colour], height, name))
        elif textbox:
            self.components.append(Textbox(loc, size, colours[colour], height, name))
        elif gridview:
            self.components.append(Gridview(loc, size, colours[colour], height, name))
        elif spaceview:
            self.components.append(Spaceview(loc, size, colours[colour], height, name))
        else:
            self.components.append(Entity(loc, size, colours[colour], height, name))
        self.sort_components()

    def sort_components(self):
        self.components = sorted(self.components, key = lambda x: x.height)

    def get(self, name):
        for component in self.components:
            if component.name == name:
                return component

    def get_current_entity(self, pos):
        for component in reversed(self.components):
            if component.contains(pos):
                if isinstance(component, Window):
                    return component.get_current_entity(basics.Coords([pos.x - component.loc.x, pos.y - component.loc.y]))
                return component
        if self.name == "main window":
            return None
        return self

    def get_current_window(self, pos):
        for component in reversed(self.components):
            if isinstance(component, Window):
                if component.contains(pos):
                    return component.get_current_window(pos)
        if self.name == "main window":
            return None
        return self

    def draw(self, display, delta, parent):
        size, loc = super().draw(display, delta, parent)

        for component in self.components:
            component.draw(display, basics.Coords([self.loc.x + delta.x, self.loc.y + delta.y]), self.size)
