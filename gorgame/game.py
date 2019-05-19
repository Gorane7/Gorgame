from gorgame import screen
from gorgame import basics
import pygame

class Game:
    def __init__(self, size):
        self.clock = pygame.time.Clock()
        pygame.init()
        self.screen = screen.Screen(size)

    def loop(self):
        self.event_handle()
        self.screen.draw()
        self.clock.tick(30)

    def event_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.MOUSEMOTION:
                self.screen.mouse_pos = basics.Coords([event.pos[0], event.pos[1]])
                self.screen.current_entity = self.screen.window.get_current_entity(self.screen.mouse_pos)
                self.screen.current_window = self.screen.window.get_current_window(self.screen.mouse_pos)

    def quit(self):
        pygame.quit()
        quit()
