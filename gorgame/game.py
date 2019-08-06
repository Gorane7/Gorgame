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

    def loop(self):
        self.reset()
        self.event_handle()
        self.screen.draw()
        self.clock.tick(30)

    def reset(self):
        self.screen.window.reset()

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
                if event.button == 1:
                    for entity in self.screen.current_entity:
                        if isinstance(entity, screen.Button):
                            entity.pressed = True
                        if isinstance(entity, screen.Input):
                            self.screen.window.deactivate_inputs()
                            entity.activate()
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

    def add_map(self, size, name):
        self.maps[name] = map.Map(size)

    def add_space(self, size, name):
        self.spaces[name] = space.Space(size)

    def quit(self):
        pygame.quit()
        quit()
