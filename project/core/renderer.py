import pygame
import pyscroll

from project.entities.player import Player
from project.utils import Dimensions
from .world import World


class Renderer:
    def __init__(self, resolution: Dimensions):
        self.screen: pygame.Surface = None
        self.surface: pygame.Surface = None
        self._set_screen(*resolution)

        self.map_layer = None
        self.group = None

    def load_world(self, world: World):
        w, h = self.screen.get_size()
        self.map_layer = pyscroll.BufferedRenderer(world.map_data, (w / 2, h / 2), clamp_camera=True)
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=4)
        self.group.add(world.player)
        self.group.add(world.lemons)

    def draw(self, player: Player):
        # Prevents the camera from tracking the player when moving left
        camera_pos = list(player.rect.center)
        camera_pos[0] = max(camera_pos[0], player.max_x)

        self.group.center(camera_pos)
        self.group.draw(self.surface)

    def draw_score(self, score):
        text = f'Score: {score}'
        font = pygame.font.SysFont('Arial', 14)
        font_surface: pygame.Surface = font.render(text, False, (255, 255, 255), (0, 0, 0))
        x = self.surface.get_size()[0] - font_surface.get_width()
        self.surface.blit(font_surface, (x, 0))

    def resize(self, width, height):
        self._set_screen(width, height)
        self.map_layer.set_size((width / 2, height / 2))

    def _draw_debug_info(self, player: Player, col_event):
        # TODO: Move somewhere else?
        text = repr(player).split('\n')
        if col_event:
            text.extend((
                f'Collision: {col_event.collision}',
                f'Position: {col_event.position} (offset: {col_event.offset})',
                f'Surface: {col_event.surface}'
            ))

        font = pygame.font.SysFont('Arial', 14)
        height = 0
        for line in text:
            font_surface: pygame.Surface = font.render(line, False, (255, 255, 255), (0, 0, 0))
            self.surface.blit(font_surface, (0, height))
            height += font_surface.get_height()

    def update(self, player: Player, score: int, debug: bool, col_event):
        self.draw(player)
        self.draw_score(score)
        if debug:
            self._draw_debug_info(player, col_event)

        # Resizes the surface and sets it as the new screen.
        pygame.transform.scale(self.surface, self.screen.get_size(), self.screen)
        pygame.display.flip()  # Updates the display.

    def _set_screen(self, width, height):
        """Simple wrapper to keep the screen resizeable."""
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.surface = pygame.Surface((width / 2, height / 2)).convert()
