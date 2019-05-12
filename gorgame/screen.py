import pygame

class Screen:
    def __init__(self):
        self.clock = pygame.time.Clock()
        pygame.init()
        self.display = pygame.display.set_mode((700,500))
        pygame.display.set_caption("Game")

    def loop(self):
        self.event_handle()
        self.draw()
        self.clock.tick(30)

    def event_handle(self):
        pass

    def draw(self):
        pass

    def quit(self):
        pygame.quit()
        quit()
