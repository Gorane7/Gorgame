import pygame
import math
from gorgame import basics

#CONSTANTS
#COLORS
colours = {
    "green": [0, 220, 0],
    "blue": [0, 0, 255],
    "red": [255, 0, 0],
    "black": [0, 0, 0],
    "dark grey": [63, 63, 63],
    "grey": [127, 127, 127],
    "light grey": [191, 191, 191],
    "white": [255, 255, 255],
    "yellow": [255, 255, 0],
    "pink": [255, 0, 255],
    "teal": [0, 255, 255],
    "dark blue": [0, 0, 127],
    "dark teal": [0, 127, 127],
    "dark red": [127, 0, 0],
    "dark green": [0, 110, 0],
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
        if isinstance(loc, basics.Coords):
            self.loc = loc
        else:
            self.loc = basics.Coords([loc[0], loc[1]])
        if isinstance(size, basics.Coords):
            self.size = size
        else:
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
        if self.colour:
            display.fill(self.colour, (x_loc, y_loc, x_size, y_size))

        return basics.Coords([x_size, y_size]), basics.Coords([x_loc, y_loc])

class Scrollview(Entity):
    def __init__(self, loc, size, colour, height, name):
        Entity.__init__(self, loc, size, colour, height, name)
        self.zoom = 1.0
        self.centre = None

    def zoom_in(self):
        self.zoom *= 1.1

    def zoom_out(self):
        self.zoom /= 1.1

class Spaceview(Scrollview):
    def __init__(self, loc, size, colour, height, name, faction):
        Scrollview.__init__(self, loc, size, colour, height, name)
        self.space = None
        self.ratio = None
        self.centre = None
        self.faction = faction
        self.bounding_lines = self.gen_bounding_lines()
        self.angle_delta = 0.0000000000001
        self.a = (0, 0, 1)
        self.c = (0, 1, 0)
        self.d = (1, 0, 0)
        self.e = (0, 0, 0)

    def add_space(self, space, ratio):
        self.space = space
        self.ratio = ratio
        self.centre = basics.Coords([0.0, 0.0])
        self.update_locs()

    def remove_space(self):
        self.space = None
        self.ratio = None
        self.centre = None

    def gen_bounding_lines(self):
        lines = []
        self.corner_points = [basics.Coords([0, 0]), basics.Coords([self.size.x, 0]), basics.Coords([self.size.x, self.size.y]), basics.Coords([0, self.size.y])]
        lines.append([basics.Coords([self.corner_points[0].x - 1.0, self.corner_points[0].y]), basics.Coords([self.corner_points[1].x + 1.0, self.corner_points[1].y]), self.line_from_points(basics.Coords([self.corner_points[0].x - 1.0, self.corner_points[0].y]), basics.Coords([self.corner_points[1].x + 1.0, self.corner_points[1].y]))])
        lines.append([basics.Coords([self.corner_points[1].x, self.corner_points[1].y - 1.0]), basics.Coords([self.corner_points[2].x, self.corner_points[2].y + 1.0]), self.line_from_points(basics.Coords([self.corner_points[1].x, self.corner_points[1].y - 1.0]), basics.Coords([self.corner_points[2].x, self.corner_points[2].y + 1.0]))])
        lines.append([basics.Coords([self.corner_points[2].x + 1.0, self.corner_points[2].y]), basics.Coords([self.corner_points[3].x - 1.0, self.corner_points[3].y]), self.line_from_points(basics.Coords([self.corner_points[2].x + 1.0, self.corner_points[2].y]), basics.Coords([self.corner_points[3].x - 1.0, self.corner_points[3].y]))])
        lines.append([basics.Coords([self.corner_points[3].x, self.corner_points[3].y + 1.0]), basics.Coords([self.corner_points[0].x, self.corner_points[0].y - 1.0]), self.line_from_points(basics.Coords([self.corner_points[3].x, self.corner_points[3].y + 1.0]), basics.Coords([self.corner_points[0].x, self.corner_points[0].y - 1.0]))])
        return lines

    def line_from_points(self, start, end):
        #x(y1 - y2) + y(x2 - x1) = y1x2 - x1y2
        line = []
        line.append(start.y - end.y)
        line.append(end.x - start.x)
        line.append(start.y * end.x - start.x * end.y)
        return line

    def line_from_point_and_angle(self, start, angle):
        #x(tan(a)) - y = x1(tan(a)) - y1
        line = []
        line.append(math.tan(angle))
        line.append(-1)
        line.append(start.x * math.tan(angle) - start.y)
        return line

    def get_line_intersection(self, line1, line2):
        det = line1[0] * line2[1] - line1[1] * line2[0]
        detx = line1[2] * line2[1] - line1[1] * line2[2]
        dety = line1[0] * line2[2] - line1[2] * line2[0]
        if det == 0.0:
            return None
        x = detx / det
        y = dety / det
        return basics.Coords([x, y])

    def is_between(self, point, start, end):
        is_between = True
        if min(point.x, start.x, end.x) == point.x or max(point.x, start.x, end.x) == point.x:
            if point.x == start.x == end.x:
                pass
            else:
                is_between = False
        if min(point.y, start.y, end.y) == point.y or max(point.y, start.y, end.y) == point.y:
            if point.y == start.y == end.y:
                pass
            else:
                is_between = False
        return is_between

    def in_same_sector(self, point, origin, angle):
        point_angle = math.atan2(point.y - origin.y, point.x - origin.x)
        angle_d = abs(point_angle - angle)
        if angle_d < 0.01:
            return True
        return False

    def get_point_away_at_angle(self, start, angle, dist):
        d_x = math.cos(angle) * dist
        d_y = math.sin(angle) * dist
        return basics.Coords([start.x + d_x, start.y + d_y])

    def closest_point(self, point, points):
        points.sort(key = lambda x : basics.dist(point, x))
        return points[0]

    def update_locs(self):
        self.agent_locs = []
        self.wall_locs = []
        for agent in self.space.agents:
            self.agent_locs.append(self.space_to_pixel(agent.loc))

        for wall in self.space.walls:
            start = self.space_to_pixel(wall.start)
            end = self.space_to_pixel(wall.end)
            line = self.line_from_points(start, end)
            self.wall_locs.append([start, end, line])

    def zoom_in(self):
        if self.space:
            super().zoom_in()
            self.update_locs()

    def zoom_out(self):
        if self.space:
            super().zoom_out()
            self.update_locs()

    def space_to_pixel(self, space_loc):
        temp_loc = basics.Coords([space_loc.x * self.zoom / self.ratio, space_loc.y * self.zoom / self.ratio])
        temp_loc = basics.Coords([temp_loc.x + self.size.x / 2 - self.centre.x * self.zoom / self.ratio, temp_loc.y + self.size.y / 2 - self.centre.y * self.zoom / self.ratio])
        return temp_loc

    def centre_move(self, mouse_move):
        if self.space:
            self.centre.add(basics.Coords([ - mouse_move.x * self.ratio / self.zoom,  - mouse_move.y * self.ratio / self.zoom]))
            self.update_locs()

    def draw(self, display, delta, parent):
        size, loc = super().draw(display, delta, parent)

        if self.space:
            surface = pygame.Surface((self.size.x, self.size.y))
            if self.colour:
                surface.fill(self.colour)
            else:
                surface.fill(self.a)
                surface.set_colorkey(self.a)
            for agent, agent_loc in zip(self.space.agents, self.agent_locs):
                pygame.draw.circle(surface, colours[agent.colour], (int(agent_loc.x), int(agent_loc.y)), int(agent.radius * self.zoom / self.ratio))

            for wall, wall_loc in zip(self.space.walls, self.wall_locs):
                pygame.draw.line(surface, colours[wall.colour], (int(wall_loc[0].x), int(wall_loc[0].y)), (int(wall_loc[1].x), int(wall_loc[1].y)), int(wall.thickness * self.zoom))

            display.blit(surface, (loc.x,loc.y))
            temp_surf = pygame.Surface((self.size.x, self.size.y))
            temp_surf.fill(self.e)
            temp_surf.set_colorkey(self.a)
            if self.faction:
                for agent, agent_loc in zip(self.space.agents, self.agent_locs):
                    if agent.faction == self.faction:
                        agent_surf = pygame.Surface((self.size.x, self.size.y))
                        agent_surf.fill(self.a)
                        agent_surf.set_colorkey(self.d)
                        circle_surf = pygame.Surface((self.size.x, self.size.y))
                        circle_surf.fill(self.d)
                        circle_surf.set_colorkey(self.c)
                        pygame.draw.circle(circle_surf, self.c, (int(agent_loc.x), int(agent_loc.y)), int(agent.vision_radius * self.zoom / self.ratio))
                        agent_surf.blit(circle_surf, (0, 0))
                        sight_angles = []
                        for wall_loc in self.wall_locs:
                            angle = math.atan2(wall_loc[0].y - agent_loc.y, wall_loc[0].x - agent_loc.x)
                            sight_angles.append(angle - self.angle_delta)
                            sight_angles.append(angle + self.angle_delta)
                            angle = math.atan2(wall_loc[1].y - agent_loc.y, wall_loc[1].x - agent_loc.x)
                            sight_angles.append(angle - self.angle_delta)
                            sight_angles.append(angle + self.angle_delta)
                        for corner_point in self.corner_points:
                            angle = math.atan2(corner_point.y - agent_loc.y, corner_point.x - agent_loc.x)
                            sight_angles.append(angle - self.angle_delta)
                            sight_angles.append(angle + self.angle_delta)
                        sight_angles.sort()
                        sight_lines = []
                        for angle in sight_angles:
                            sight_lines.append([self.line_from_point_and_angle(agent_loc, angle), angle])
                        polygon_points = []
                        for line in sight_lines:
                            line_points = []
                            for wall_data in self.wall_locs:
                                point = self.get_line_intersection(line[0], wall_data[2])

                                if self.is_between(point, wall_data[0], wall_data[1]):
                                    if self.in_same_sector(point, agent_loc, line[1]):
                                        line_points.append(point)
                            #add point sqrt(2) * self.size away
                            point = self.get_point_away_at_angle(agent_loc, line[1], max(self.size.x, self.size.y) * math.sqrt(2))
                            line_points.append(point)
                            polygon_points.append([self.closest_point(agent_loc, line_points).x, self.closest_point(agent_loc, line_points).y])
                        #pygame.draw.polygon(walls, (1, 1, 1), polygon_points)
                        wall_surf = pygame.Surface((self.size.x, self.size.y))
                        wall_surf.fill(self.d)
                        wall_surf.set_colorkey(self.c)
                        pygame.draw.polygon(wall_surf, self.c, polygon_points)
                        agent_surf.blit(wall_surf, (0, 0))
                        temp_surf.blit(agent_surf, (loc.x, loc.y))
                display.blit(temp_surf, (loc.x, loc.y))
                #display.blit(fog, (loc.x, loc.y))
                #display.blit(walls, (loc.x, loc.y))

class Gridview(Scrollview):
    def __init__(self, loc, size, colour, height, name):
        Scrollview.__init__(self, loc, size, colour, height, name)
        self.acc = 25
        self.grid = None
        self.centre = basics.Coords([0, 0])
        self.grid_size = basics.Coords([1, 1])
        self.tile_size = None

    def remove_grid(self):
        self.grid = None
        self.centre = basics.Coords([0, 0])
        self.grid_size = basics.Coords([1, 1])
        self.tile_size = None

    def add_grid(self, grid):
        self.grid = grid
        self.centre = basics.Coords([len(self.grid) / 2, len(self.grid[0]) / 2])
        self.grid_size = basics.Coords([self.size.x / len(self.grid), self.size.y / len(self.grid[0])])
        self.tile_size = min(self.grid_size.x, self.grid_size.y)

    def centre_move(self, mouse_move):
        self.centre.add(basics.Coords([ - mouse_move.x / (self.grid_size.x * self.zoom),  - mouse_move.y / (self.grid_size.y * self.zoom)]))

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
        if "rgb" in t_dict:
            return t_dict["rgb"]

class Textbox(Entity):
    def __init__(self, loc, size, colour, height, name):
        Entity.__init__(self, loc, size, colour, height, name)
        self.text = name
        self.text_colour = colours["black"]

    def change_attributes(self, text = None, colour = None):
        if text:
            self.text = text
        if colour:
            self.text_colour = colours[colour]

    def draw(self, display, delta, parent):
        size, loc = super().draw(display, delta, parent)

        if self.text:
            font = pygame.font.SysFont("arial", 200)
            text_surf = font.render(self.text, True, self.text_colour)
            x_per_letter = int(size.x / (len(self.text) * 0.75))
            text_size = min(size.y, x_per_letter)
            if text_size > 0:
                text_surf = pygame.transform.scale(text_surf, (int(len(self.text) * text_size * 0.75), int(text_size)))
                x_text = loc.x + (size.x - text_surf.get_width()) // 2
                y_text = loc.y + (size.y - text_surf.get_height()) // 2
                display.blit(text_surf, (x_text, y_text))

class Input(Textbox):
    def __init__(self, loc, size, colour, height, name):
        Textbox.__init__(self, loc, size, colour, height, name)
        self.default_text = name
        self.is_written = False
        self.active = False
        self.passive_colour = self.colour
        self.active_colour = (255 - self.passive_colour[0], 255 - self.passive_colour[1], 255 - self.passive_colour[2])

    def reset(self):
        self.is_written = False
        self.deactivate()
        self.text = self.default_text

    def change_colours(self, passive = None, active = None):
        if passive:
            self.passive_colour = colours[passive]
        if active:
            self.active_colour = colours[active]

    def change_default_text(self, text):
        self.text = text
        self.default_text = text

    def activate(self):
        self.active = True
        self.colour = self.active_colour

    def deactivate(self):
        self.active = False
        self.colour = self.passive_colour

    def add_letter(self, letter):
        if not self.is_written:
            self.is_written = True
            self.text = letter
        else:
            self.text = self.text + letter

    def remove_last(self):
        if len(self.text) > 0:
            self.text = self.text[:-1]

class Button(Textbox):
    def __init__(self, loc, size, colour, height, name):
        Textbox.__init__(self, loc, size, colour, height, name)
        self.pressed = False

class Window(Entity):
    def __init__(self, loc, size, colour, height, name):
        Entity.__init__(self, loc, size, colour, height, name)
        self.components = []

    def add_component(self, loc, size, height, name, background = None, window = False, textbox = False, button = False, input = False, gridview = False, spaceview = False, faction = False):
        if background:
            colour = colours[background]
        else:
            colour = background
        for component in self.components:
            if component.name == name:
                self.components.remove(component)
        if window:
            self.components.append(Window(loc, size, colour, height, name))
        elif textbox:
            self.components.append(Textbox(loc, size, colour, height, name))
        elif button:
            self.components.append(Button(loc, size, colour, height, name))
        elif input:
            self.components.append(Input(loc, size, colour, height, name))
        elif gridview:
            self.components.append(Gridview(loc, size, colour, height, name))
        elif spaceview:
            self.components.append(Spaceview(loc, size, colour, height, name, faction))
        else:
            self.components.append(Entity(loc, size, colour, height, name))
        self.sort_components()

    def sort_components(self):
        self.components = sorted(self.components, key = lambda x: x.height)

    def get(self, name):
        for component in self.components:
            if component.name == name:
                return component

    def get_current_entity(self, pos):
        to_return = []
        for component in reversed(self.components):
            if component.contains(pos):
                if isinstance(component, Window):
                    return component.get_current_entity(basics.Coords([pos.x - component.loc.x, pos.y - component.loc.y]))
                if component.colour:
                    to_return.append(component)
                    return to_return
                to_return.append(component)
        if self.name == "main window":
            return [None]
        return [self]

    def get_current_window(self, pos):
        for component in reversed(self.components):
            if isinstance(component, Window):
                if component.contains(pos):
                    return component.get_current_window(pos)
        if self.name == "main window":
            return None
        return self

    def remove(self, target):
        for component in self.components:
            if component.name == target:
                self.components.remove(component)

    def reset(self):
        for component in self.components:
            if isinstance(component, Window):
                component.reset()
            elif isinstance(component, Button):
                component.pressed = False

    def deactivate_inputs(self):
        for component in self.components:
            if isinstance(component, Window):
                component.deactivate_inputs()
            elif isinstance(component, Input):
                component.deactivate()

    def add_letter_to_active(self, letter):
        for component in self.components:
            if isinstance(component, Window):
                component.add_letter_to_active(letter)
            elif isinstance(component, Input):
                if component.active:
                    component.add_letter(letter)

    def remove_last_from_active(self):
        for component in self.components:
            if isinstance(component, Window):
                component.remove_last_from_active()
            elif isinstance(component, Input):
                if component.active:
                    component.remove_last()

    def get_inputs(self):
        return_dict = {}
        for component in self.components:
            if isinstance(component, Window):
                this_dict = component.get_inputs()
                for key, item in this_dict.items():
                    return_dict[key] = item
            elif isinstance(component, Input):
                if component.is_written:
                    return_dict[component.name] = component.text
                component.reset()
        return return_dict

    def draw(self, display, delta, parent):
        size, loc = super().draw(display, delta, parent)

        for component in self.components:
            component.draw(display, basics.Coords([self.loc.x + delta.x, self.loc.y + delta.y]), self.size)
