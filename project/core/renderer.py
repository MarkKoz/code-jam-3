import pygame
import pyscroll

from utils import Dimensions


class Renderer:
    def __init__(self, resolution: Dimensions, map_data: pyscroll.data.TiledMapData):
        self.screen: pygame.Surface = None
        self.surface: pygame.Surface = None
        self._set_screen(*resolution)

        w, h = self.screen.get_size()
        self.map_layer = pyscroll.BufferedRenderer(map_data, (w / 2, h / 2), clamp_camera=True)
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=4)

    def draw(self, camera_pos):
        self.group.center(camera_pos)
        self.group.draw(self.surface)

        pygame.transform.scale(self.surface, self.screen.get_size(), self.screen)
        pygame.display.flip()  # Updates the display.

    def _set_screen(self, width, height):
        """Simple wrapper to keep the screen resizeable."""
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.surface = pygame.Surface((width / 2, height / 2)).convert()
