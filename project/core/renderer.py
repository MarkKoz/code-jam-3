import pygame
import pyscroll

from project.entities.player import Player
from project.menu import DeathMenu
from .constants import FONTS, SCREEN_SCALE
from .world import World


class Renderer:
    def __init__(self, width: int, height: int):
        self.screen: pygame.Surface = None
        self.surface: pygame.Surface = None
        self._set_screen(width, height)

        self.map_layer = None
        self.group = None

        self.death_menu = DeathMenu(*self.surface.get_size())

    def load_world(self, world: World):
        w, h = self.screen.get_size()
        self.map_layer = pyscroll.BufferedRenderer(world.map_data,
                                                   (w / SCREEN_SCALE, h / SCREEN_SCALE),
                                                   clamp_camera=True)
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=4)
        self.group.add(world.player)
        self.group.add(world.lemons)
        self.group.add(world.juice, layer=5)

    def draw(self, player: Player):
        # Prevents the camera from tracking the player when moving left
        camera_pos = list(player.rect.center)
        camera_pos[0] = max(camera_pos[0], player.max_x)

        self.group.center(camera_pos)
        self.group.draw(self.surface)

    def draw_score(self, score):
        text = f'Lemons: {score}'
        font = pygame.font.Font(FONTS['monogram'], 16)
        font_surface: pygame.Surface = font.render(text, False, pygame.Color('white'))
        x = self.surface.get_size()[0] - font_surface.get_width()
        self.surface.blit(font_surface, (x - 4, 4))

    def resize(self, width, height):
        self._set_screen(width, height)
        self.map_layer.set_size((width / SCREEN_SCALE, height / SCREEN_SCALE))
        if self.death_menu.display:
            self.death_menu.resize(*self.surface.get_size())

    def _draw_debug_info(self, player: Player, col_event):
        # TODO: Move somewhere else?
        text = repr(player).split('\n')
        if col_event:
            text.extend((
                f'Collision: {col_event.collision}',
                f'Position: {col_event.position} (offset: {col_event.offset})',
                f'Surface: {col_event.surface}'
            ))

        font = pygame.font.Font(FONTS['monogram'], 16)
        height = 0
        for line in text:
            font_surface: pygame.Surface = font.render(line, False, pygame.Color('white'))
            bg_surface: pygame.Surface = pygame.Surface(font_surface.get_size(), pygame.SRCALPHA, 32)
            bg_surface.fill((51, 51, 51, 159))
            bg_surface.blit(font_surface, (0, 0))
            self.surface.blit(bg_surface, (0, height))
            height += font_surface.get_height()

    def update(self, player: Player, score: int, debug: bool, col_event):
        self.draw(player)

        self.death_menu.update(score, self.surface)
        if not self.death_menu.display:
            self.draw_score(score)

        if debug:
            self._draw_debug_info(player, col_event)

        # Resizes the surface and sets it as the new screen.
        pygame.transform.scale(self.surface, self.screen.get_size(), self.screen)
        pygame.display.flip()  # Updates the display.

    def _set_screen(self, width, height):
        """Simple wrapper to keep the screen resizeable."""
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.surface = pygame.Surface((width / SCREEN_SCALE, height / SCREEN_SCALE)).convert()
