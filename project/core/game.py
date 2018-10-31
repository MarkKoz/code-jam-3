import pygame

from project.menu import MainMenu
from .constants import DEFAULT_SIZE, FPS, JUICE_FILL_RATE, MAP_PATH, TITLE
from .renderer import Renderer
from .world import World


class Game:
    def __init__(self):
        self.running = False
        self.debug = True

        self.renderer = Renderer(DEFAULT_SIZE.width, DEFAULT_SIZE.height)
        self.world = World(MAP_PATH)
        self.renderer.load_world(self.world)

        self.score = 0

    def handle_events(self):
        key_events = []
        col_event = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.VIDEORESIZE:
                self.renderer.resize(event.w, event.h)
            elif event.type == pygame.KEYDOWN:
                key_events.append((event.key, False))
            elif event.type == pygame.KEYUP:
                key_events.append((event.key, True))
            elif event.type == pygame.USEREVENT:
                col_event = event
            elif event.type == pygame.USEREVENT + 1:
                self.score += 1
                self.world.juice.size.height = self.score * JUICE_FILL_RATE
                event.lemon.kill()
            elif event.type == pygame.USEREVENT + 2:
                self.world = World(MAP_PATH)
                self.renderer.load_world(self.world)
                self.score = 0

        return key_events, col_event

    def handle_input(self, key, up=False):
        if key == pygame.K_i and not up:
            self.debug = not self.debug
        elif key == pygame.K_g and not up:
            self.world.gravity = 0 if self.world.gravity else -50

    def update(self, time_delta, key_events):
        self.renderer.group.update(time_delta, key_events, self.world)

        for e in key_events:
            self.handle_input(*e)

    def run(self):
        """Starts the game's main loop."""
        pygame.display.set_caption(TITLE)

        main_menu = MainMenu(DEFAULT_SIZE.width, DEFAULT_SIZE.height)
        if not main_menu.mainloop():
            return pygame.quit()

        self.running = True
        clock = pygame.time.Clock()

        pygame.mouse.set_visible(False)

        try:
            while self.running:
                # Gets number of seconds since last call
                time_delta = clock.tick(FPS) / 1000

                key_events, col_event = self.handle_events()
                self.update(time_delta, key_events)
                self.renderer.update(self.world.player, self.score, self.debug, col_event)
        except KeyboardInterrupt:
            self.running = False
            pygame.quit()
