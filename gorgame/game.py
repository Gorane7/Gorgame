import pygame
from gorgame import screen
from gorgame import basics
from gorgame import map
from gorgame import space


class Game:
    def __init__(self, size):
        self.clock = pygame.time.Clock()
        pygame.init()
        self.screen = screen.Screen(size)
        self.maps = {}
        self.spaces = {}
        self.mouse_down = False
        self.output = None
        self.default_map = None
        self.default_space = None

    def loop(self):
        self.reset()
        self.event_handle()
        self.screen.render()
        self.screen.draw()
        self.clock.tick(30)

    def reset(self):
        self.screen.window.reset()
        self.output = None

    def event_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.MOUSEMOTION:
                new_pos = basics.Coords([event.pos[0], event.pos[1]])
                mouse_move = basics.Coords([new_pos.x, new_pos.y])
                mouse_move.subtract(self.screen.mouse_pos)
                self.screen.mouse_pos = new_pos
                self.screen.current_entity = self.screen.window.get_current_entity(self.screen.mouse_pos)
                self.screen.current_window = self.screen.window.get_current_window(self.screen.mouse_pos)
                if self.mouse_down:
                    for entity in self.screen.current_entity:
                        if isinstance(entity, screen.Scrollview):
                            entity.centre_move(mouse_move)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_down = True
                self.screen.window.deactivate_inputs()
                if event.button == 1:
                    if isinstance(self.screen.current_window, screen.Toggleview):
                        self.screen.current_window.untoggle()
                    for entity in self.screen.current_entity:
                        if isinstance(entity, screen.Button):
                            entity.pressed = True
                        if isinstance(entity, screen.Toggle):
                            entity.activate()
                        if isinstance(entity, screen.Spaceview):
                            entity.click(self.screen.mouse_pos)
                if event.button == 4:
                    for entity in self.screen.current_entity:
                        if isinstance(entity, screen.Scrollview):
                            entity.zoom_in()
                if event.button == 5:
                    for entity in self.screen.current_entity:
                        if isinstance(entity, screen.Scrollview):
                            entity.zoom_out()
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_down = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.screen.window.remove_last_from_active()
                elif event.key == pygame.K_CAPSLOCK or event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                    pass
                elif event.key == pygame.K_RETURN:
                    self.output = self.screen.window.get_inputs()
                else:
                    letter = event.unicode
                    self.screen.window.add_letter_to_active(letter)

    def add_map(self, size, name, default = False):
        self.maps[name] = map.Map(size)
        if default or not self.default_map:
            self.default_map = name

    def fill_map(self, type, colour = "greyscale", span = [0, 1]):
        if not self.default_map:
            return "There is no default map"
        if type == "random tiles":
            self.maps[self.default_map].fill_random_tiles(colour, span[0], span[1])

    def add_space(self, size, name, default = False, default_agent_radius = None, default_faction = None, default_colour = None, default_vision_radius = None, default_wall_thickness = None):
        self.spaces[name] = space.Space(size)
        if default or not self.default_space:
            self.default_space = name
        if default_agent_radius:
            self.spaces[name].default_agent_radius = default_agent_radius
        if default_faction:
            self.spaces[name].default_faction = default_faction
        if default_colour:
            self.spaces[name].default_colour = default_colour
        if default_vision_radius:
            self.spaces[name].default_vision_radius = default_vision_radius
        if default_wall_thickness:
            self.spaces[name].default_wall_thickness = default_wall_thickness

    def add_agent(self, loc, radius = None, colour = None, faction = None, vision_radius = None):
        if not self.default_space:
            return "There is no default space"
        self.spaces[self.default_space].add_agent(loc, radius = radius, colour = colour, faction = faction, vision_radius = vision_radius)

    def add_wall(self, start, end, thickness = None, colour = None):
        if not self.default_space:
            return "There is no default space"
        self.spaces[self.default_space].add_wall(start, end, thickness = thickness, colour = colour)

    def quit(self):
        pygame.quit()
        quit()
