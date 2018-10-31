import pygame

from project.core.constants import FONTS, SCREEN_SCALE


class Button:
    def __init__(self, width: int, height: int, colour: str, text: str = '', command=None, shortcut=None):
        self.command = command
        self.shortcut = shortcut
        self._surface = pygame.Surface((width, height))
        self._surface.fill(pygame.Color(colour))
        self.rect: pygame.Rect = self._surface.get_rect()

        self._text_surface = create_label(text, 'monogram', 32)
        self._text_rect: pygame.Rect = self._text_surface.get_rect(center=self.rect.center)

    def draw(self, surface: pygame.Surface):
        surface.blit(self._surface, self.rect)
        surface.blit(self._text_surface, self._text_rect)

    def refresh(self):
        self._text_rect.center = self.rect.center

    def handle_event(self, event):
        if event.type == pygame.KEYUP and event.key == self.shortcut:
            if self.command:
                self.command()

        elif event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            if self.rect.collidepoint((x / SCREEN_SCALE, y / SCREEN_SCALE)):
                # TODO: Hover effect
                pass

        elif event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            if self.rect.collidepoint((x / SCREEN_SCALE, y / SCREEN_SCALE)):
                if self.command:
                    self.command()
            return True


def create_label(text, font_name, size, fg: str = 'black', bg: str = None):
    if font_name in FONTS:
        font = pygame.font.Font(FONTS[font_name], size)
    else:
        font = pygame.font.SysFont(font_name, size)

    font_surface: pygame.Surface = font.render(text, False, pygame.Color(fg), pygame.Color(bg) if bg else bg)
    return font_surface


def create_multiline_label(text: str, font_name: str, size: int, fg: str = 'black', bg: str = None):
    if font_name in FONTS:
        font = pygame.font.Font(FONTS[font_name], size)
    else:
        font = pygame.font.SysFont(font_name, size)

    fg = pygame.Color(fg)
    surfaces = []
    heights = []
    width = 0
    height = 0

    for line in text.split('\n'):
        font_surface: pygame.Surface = font.render(line, False, fg)
        surfaces.append(font_surface)
        surface_width, surface_height = font_surface.get_size()
        heights.append(height)
        height += surface_height
        if surface_width > width:
            width = surface_width

    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    if bg:
        surface.fill(pygame.Color(bg))
    else:
        surface = surface.convert_alpha()

    for font_surface, height_offset in zip(surfaces, heights):
        surface.blit(font_surface, (width / 2 - font_surface.get_width() / 2, height_offset))
    return surface
