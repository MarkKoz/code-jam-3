import pygame

from core.renderer import Renderer
from core.world import World
from entities.player import Player, PlayerGraphicsComponent, PlayerPhysicsComponent, PlayerInputComponent
from utils import Dimensions, Point

DEFAULT_SIZE = Dimensions(1280, 720)
FPS = 60
MAP_PATH = 'assets/map.tmx'


class Game:
    def __init__(self):
        self.running = False
        self.debug = False

        self.renderer = Renderer(DEFAULT_SIZE)
        self.world = World(MAP_PATH)
        self.renderer.load_map(self.world.map_data)
        self.player = None

        self.add_player()

    def add_player(self):
        # y = 0 is top but the map starts at the bottom.
        # TODO: Read spawn point from map file?
        bottom = self.renderer.map_layer.data.map_size[1] * self.renderer.map_layer.data.tile_size[1]
        self.player = Player(
            PlayerGraphicsComponent(),
            PlayerInputComponent(),
            PlayerPhysicsComponent(),
            position=Point(64, bottom - 192),
            size=Dimensions(16, 32)
        )
        self.renderer.group.add(self.player)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.VIDEORESIZE:
                self.renderer.resize(event.w, event.h)
            elif event.type == pygame.KEYDOWN:
                self.handle_input(event)
            elif event.type == pygame.KEYUP:
                self.handle_input(event, True)

    def handle_input(self, event, up=False):
        if event.key == pygame.K_i and not up:
            self.debug = not self.debug

    def update(self, time_delta):
        self.renderer.group.update(time_delta, self.world)

    def run(self):
        """Starts the game's main loop."""
        self.running = True
        clock = pygame.time.Clock()

        try:
            while self.running:
                # Gets number of seconds since last call
                time_delta = clock.tick(FPS) / 1000

                self.handle_events()
                self.renderer.update(self.player, self.debug)
                self.update(time_delta)
        except KeyboardInterrupt:
            self.running = False
            pygame.quit()
