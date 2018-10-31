import pygame

from project.utils import Dimensions
from .widgets import Button, create_label


class DeathMenu:
    def __init__(self, width, height):
        self.surface: pygame.Surface = self._get_surface(width, height)

        self.score = 0
        self.display = False

        self._title_label = create_label('YOU DIED', 'too much ink', 32, '#d95763')
        self._title_rect = self._title_label.get_rect()
        self._score_label = create_label(f'Final Score: {self.score}', 'monogram', 16)
        self._score_rect = self._score_label.get_rect()
        self._buttons = []
        self._buttons.append(Button('Play Again', Dimensions(144, 32), command=self._play, shortcut=pygame.K_SPACE))
        self._buttons.append(Button('Quit', Dimensions(144, 32), command=self._quit, shortcut=pygame.K_ESCAPE))

        self.resize(width, height)

    def draw(self, surface):
        self.surface.blit(self._title_label, self._title_rect)
        self.surface.blit(self._score_label, self._score_rect)
        for button in self._buttons:
            button.draw(self.surface)

        surface.blit(self.surface, (0, 0))

    def resize(self, width, height):
        self.surface = self._get_surface(width, height)
        x = self.surface.get_rect().centerx

        self._title_rect.centerx = x
        self._title_rect.top = 20
        height = self._title_rect.bottom + 10

        self._score_rect.centerx = x
        self._score_rect.top = height
        height = self._score_rect.bottom + 20

        for button in self._buttons:
            button.rect.centerx = x
            button.rect.top = height
            height += button.rect.height + 20

    def update(self, score: int, surface: pygame.Surface):
        if not self.display:
            return
        if score != self.score:
            self.score = score

            self._score_label = create_label(f'Final Score: {self.score}', 'monogram', 16)
            self._score_rect = self._score_label.get_rect()
            self.resize(*self.surface.get_size())

        self.draw(surface)

    def handle_events(self, event):
        if not self.display:
            return
        if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.KEYUP):
            for button in self._buttons:
                button.handle_event(event)

    def _play(self):
        self.display = False
        event = pygame.event.Event(pygame.USEREVENT + 3)
        pygame.event.post(event)
        pygame.mouse.set_visible(False)

    def _quit(self):
        self.display = False
        event = pygame.event.Event(pygame.QUIT)
        pygame.event.post(event)

    @staticmethod
    def _get_surface(width, height) -> pygame.Surface:
        surface = pygame.Surface((width, height), pygame.SRCALPHA, 32).convert_alpha()
        surface.fill(pygame.Color(51, 51, 51, 159))
        return surface
