import pygame
import pyscroll
from pytmx.util_pygame import load_pygame

DEFAULT_SIZE = (1280, 720)
MAP_PATH = 'assets/map.tmx'


class Game:
    def __init__(self):
        self.running = False
        self.screen = None
        self.surface = None

        self.set_screen(*DEFAULT_SIZE)
        self.map_layer = self.init_map()
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer)

    def draw(self, surface):
        # y = 0 is top, but map starts at bottom.
        bottom = self.map_layer.data.map_size[1] * self.map_layer.data.tile_size[1]
        self.group.center((0, bottom))
        self.group.draw(surface)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.VIDEORESIZE:
                self.set_screen(event.w, event.h)
                self.map_layer.set_size((event.w / 2, event.h / 2))

    def run(self):
        """Starts the game's main loop."""
        self.running = True

        try:
            while self.running:
                self.handle_events()
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
