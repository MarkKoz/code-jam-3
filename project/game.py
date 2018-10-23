import pygame
import pyscroll
from pytmx.util_pygame import load_pygame

from player import Player

DEFAULT_SIZE = (1280, 720)
PLAYER_SPEED = 100
FPS = 60
MAP_PATH = 'assets/map.tmx'


class Game:
    def __init__(self):
        self.running = False
        self.screen = None
        self.surface = None

        self.set_screen(*DEFAULT_SIZE)
        self.map_layer = self.init_map()
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer)

        self.player = Player()

        # y = 0 is top but the map starts at the bottom.
        bottom = self.map_layer.data.map_size[1] * self.map_layer.data.tile_size[1]
        self.player.position = [64, bottom - 192]

        self.group.add(self.player)

    def draw(self, surface):
        self.group.center(self.player.rect.center)
        self.group.draw(surface)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.VIDEORESIZE:
                self.set_screen(event.w, event.h)
                self.map_layer.set_size((event.w / 2, event.h / 2))
            elif event.type == pygame.KEYDOWN:
                self.handle_input(event)
            elif event.type == pygame.KEYUP:
                self.handle_input(event, True)

    def handle_input(self, event, up=False):
        # Set velocity to 0 if key is released.
        speed = 0 if up else PLAYER_SPEED

        # TODO: Options/constants for controls
        if event.key in (pygame.K_UP, pygame.K_w):
            self.player.velocity[1] = -speed
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.player.velocity[1] = speed

        if event.key in (pygame.K_LEFT, pygame.K_a):
            self.player.velocity[0] = -speed
        elif event.key in (pygame.K_RIGHT, pygame.K_d):
            self.player.velocity[0] = speed

    def update(self, time_delta):
        self.player.update(time_delta)

    def run(self):
        """Starts the game's main loop."""
        self.running = True
        clock = pygame.time.Clock()

        try:
            while self.running:
                # Gets number of seconds since last call
                time_delta = clock.tick(FPS) / 1000

                self.handle_events()
                self.update(time_delta)
                self.draw(self.surface)

                # Resizes the surface and sets it as the new screen.
                pygame.transform.scale(
                    self.surface, self.screen.get_size(), self.screen)

                pygame.display.flip()  # Updates the display.
        except KeyboardInterrupt:
            self.running = False
            pygame.quit()

    def set_screen(self, width, height):
        """Simple wrapper to keep the screen resizeable."""
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.surface = pygame.Surface((width / 2, height / 2)).convert()

    def init_map(self):
        """Loads map data and creates a renderer."""
        tmx_data = load_pygame(MAP_PATH)  # Load data from pytmx

        # Create new data source for pyscroll
        map_data = pyscroll.data.TiledMapData(tmx_data)

        w, h = self.screen.get_size()

        # Create new renderer (camera)
        return pyscroll.BufferedRenderer(
            map_data, (w / 2, h / 2), clamp_camera=True
        )


def main():
    pygame.init()
    # pygame.font.init()

    try:
        game = Game()
        game.run()
    except Exception:
        pygame.quit()
        raise


if __name__ == '__main__':
    main()
