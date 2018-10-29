import pygame

from project.core.constants import SCREEN_SCALE


class Button:
    def __init__(self, width: int, height: int, colour: str, text: str = '', command=None):
        self.command = command
        self._surface = pygame.Surface((width, height))
        self._surface.fill(pygame.Color(colour))
        self.rect: pygame.Rect = self._surface.get_rect()

        self._text_surface = create_label(text, 'Arial', 22)
        self._text_rect: pygame.Rect = self._text_surface.get_rect(center=self.rect.center)

    def draw(self, surface: pygame.Surface):
        # self._surface.blit(self._text_surface, self._surface.get_rect())

        surface.blit(self._surface, self.rect)
        surface.blit(self._text_surface, self._text_rect)

    def refresh(self):
        self._text_rect.center = self.rect.center

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
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


def create_label(text, font, size, fg: str='black', bg: str=None):
    font = pygame.font.SysFont(font, size)
    font_surface: pygame.Surface = font.render(text, False, pygame.Color(fg), pygame.Color(bg) if bg else bg)
    return font_surface
