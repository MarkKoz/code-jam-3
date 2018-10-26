import pygame
import pyscroll

from project.entities.player import Player
from project.utils import Dimensions


class Renderer:
    def __init__(self, resolution: Dimensions):
        self.screen: pygame.Surface = None
        self.surface: pygame.Surface = None
        self._set_screen(*resolution)

        self.map_layer = None
        self.group = None

    def load_map(self, map_data: pyscroll.data.TiledMapData):
        w, h = self.screen.get_size()
        self.map_layer = pyscroll.BufferedRenderer(map_data, (w / 2, h / 2), clamp_camera=True)
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=4)

    def draw(self, player: Player):
        # Prevents the camera from tracking the player when moving left
        camera_pos = list(player.rect.center)
        camera_pos[0] = max(camera_pos[0], player.max_x)

        self.group.center(camera_pos)
        self.group.draw(self.surface)

    def resize(self, width, height):
        self._set_screen(width, height)
        self.map_layer.set_size((width / 2, height / 2))

    def _draw_debug_info(self, player: Player):
        # TODO: Move somewhere else?
        font = pygame.font.SysFont('Arial', 14)
        text = repr(player).split('\n')
        height = 0
        for line in text:
            font_surface: pygame.Surface = font.render(line, False, (255, 255, 255), (0, 0, 0))
            self.surface.blit(font_surface, (0, height))
            height += font_surface.get_height()

    def update(self, player: Player, debug: bool):
        self.draw(player)
        if debug:
            self._draw_debug_info(player)

        # Resizes the surface and sets it as the new screen.
        pygame.transform.scale(self.surface, self.screen.get_size(), self.screen)
        pygame.display.flip()  # Updates the display.

    def _set_screen(self, width, height):
        """Simple wrapper to keep the screen resizeable."""
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.surface = pygame.Surface((width / 2, height / 2)).convert()
