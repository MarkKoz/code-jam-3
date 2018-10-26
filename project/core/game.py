from collections import defaultdict

import pygame
import pyscroll
import pytmx
from pytmx.util_pygame import load_pygame

from project.player import Player

DEFAULT_SIZE = (1280, 720)
FPS = 60
MAP_PATH = 'assets/map.tmx'
TILE_SIZE = 32


class Game:
    def __init__(self):
        self.running = False
        self.debug = False
        self.screen = None
        self.surface = None
        self.collisions = defaultdict(list)

        self.set_screen(*DEFAULT_SIZE)
        self.map_layer = self.init_map()
        self.group = pyscroll.PyscrollGroup(
            map_layer=self.map_layer, default_layer=4)

        self.player = Player()

        # y = 0 is top but the map starts at the bottom.
        bottom = self.map_layer.data.map_size[1] * self.map_layer.data.tile_size[1]
        self.player.position = [64, bottom - 192]

        self.group.add(self.player)

    def draw(self, surface):
        # Prevents the camera from tracking the player when moving left
        camera_pos = list(self.player.rect.center)
        camera_pos[0] = max(camera_pos[0], self.player.max_x)

        self.group.center(camera_pos)
        self.group.draw(surface)

        if self.debug:
            self.debug_info(surface)

    def debug_info(self, surface):
        font = pygame.font.SysFont('Arial', 14)
        font_surface = font.render(repr(self.player), False, (255, 255, 255), (0, 0, 0))
        surface.blit(font_surface, (0, 0))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.VIDEORESIZE:
                self.set_screen(event.w, event.h)
                self.map_layer.set_size((event.w / 2, event.h / 2))
            elif event.type == pygame.KEYDOWN:
                self.player.handle_input(event)
                self.handle_input(event)
            elif event.type == pygame.KEYUP:
                self.player.handle_input(event, True)
                self.handle_input(event, True)

    def handle_input(self, event, up=False):
        if event.key == pygame.K_i and not up:
            self.debug = not self.debug

    def update(self, time_delta):
        self.group.update(time_delta, self.collisions)

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
        self.populate_collisions(tmx_data)

        # Create new data source for pyscroll
        map_data = pyscroll.data.TiledMapData(tmx_data)
        w, h = self.screen.get_size()

        # Create new renderer (camera)
        return pyscroll.BufferedRenderer(
            map_data, (w / 2, h / 2), clamp_camera=True)

    def populate_collisions(self, tmx_data: pytmx.TiledMap):
        # TODO: Pixel-perfect collision detection for polygons
        obj: pytmx.TiledObject
        for obj in tmx_data.objects:
            points = getattr(obj, 'points', None)
            if points:
                self.collisions['slopes'].append(obj)
            else:
                rect = pygame.Rect(
                    obj.x, obj.y, obj.width, obj.height)
                self.collisions['rects'].append(rect)


def main():
    pygame.init()

    try:
        game = Game()
        game.run()
    except Exception:
        pygame.quit()
        raise


if __name__ == '__main__':
    main()
