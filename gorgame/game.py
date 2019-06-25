import pygame
from gorgame import screen
from gorgame import basics
from gorgame import map


class Game:
    def __init__(self, size):
        self.clock = pygame.time.Clock()
        pygame.init()
        self.screen = screen.Screen(size)
        self.maps = {}
        self.mouse_down = False

    def loop(self):
        self.event_handle()
        self.screen.draw()
        self.clock.tick(30)

    def event_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.MOUSEMOTION:
                new_pos = basics.Coords([event.pos[0], event.pos[1]])
                mouse_move = self.screen.mouse_pos.subtract(new_pos)
                self.screen.mouse_pos = new_pos
                self.screen.current_entity = self.screen.window.get_current_entity(self.screen.mouse_pos)
                self.screen.current_window = self.screen.window.get_current_window(self.screen.mouse_pos)
                if self.mouse_down:
                    if isinstance(self.screen.current_entity, screen.Gridview):
                        self.screen.current_entity.centre_move(mouse_move)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_down = True
                if isinstance(self.screen.current_entity, screen.Gridview):
                    if event.button == 4:
                        self.screen.current_entity.zoom_in()
                    elif event.button == 5:
                        self.screen.current_entity.zoom_out()
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_down = False

    def add_map(self, size, name):
        self.maps[name] = map.Map(size)

    def quit(self):
        pygame.quit()
        quit()
