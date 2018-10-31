import pygame

from project.core import CONTROLS_HELP_TEXT, SCREEN_SCALE, TITLE
from .widgets import Button, create_label, create_multiline_label


class MainMenu:
    def __init__(self, width, height):
        self.screen: pygame.Surface = None
        self.surface: pygame.Surface = None
        self.running = False
        self.exit = False

        self._title_label = create_label(TITLE, 'too much ink', 32)
        self._title_rect: pygame.Rect = self._title_label.get_rect()
        self._buttons = []
        self._buttons.append(Button(200, 40, 'green', text='Start', command=self._start, shortcut=pygame.K_SPACE))
        self._buttons.append(Button(200, 40, 'green', text='Quit', command=self._exit, shortcut=pygame.K_ESCAPE))

        self._controls_info = create_multiline_label(CONTROLS_HELP_TEXT, 'Arial', 16)
        self._controls_info_rect: pygame.Rect = self._controls_info.get_rect()

        self._set_screen(width, height)

    def _set_screen(self, width, height):
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.surface = pygame.Surface((width / SCREEN_SCALE, height / SCREEN_SCALE)).convert()
        self.surface.fill(pygame.Color('white'))

    def resize(self, width, height):
        self._set_screen(width, height)
        x = self.surface.get_rect().centerx

        self._title_rect.centerx = x
        self._title_rect.top = 20
        self._controls_info_rect.centerx = x
        height = self._title_rect.bottom + 50
        for button in self._buttons:
            button.rect.centerx = x
            button.rect.top = height
            button.refresh()
            height += button.rect.height + 20
        self._controls_info_rect.top = height

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit = True
            elif event.type == pygame.VIDEORESIZE:
                self.resize(event.w, event.h)
            elif event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.KEYUP):
                for button in self._buttons:
                    button.handle_event(event)
            # TODO: Direction key menu navigation

    def _start(self):
        self.running = False

    def _exit(self):
        self.exit = True

    def draw(self):
        self.surface.blit(self._title_label, self._title_rect)
        for button in self._buttons:
            button.draw(self.surface)
        self.surface.blit(self._controls_info, self._controls_info_rect)

    def update(self):
        self.draw()
        pygame.transform.scale(self.surface, self.screen.get_size(), self.screen)
        pygame.display.flip()

    def mainloop(self):
        pygame.mouse.set_visible(True)
        self.running = True
        try:
            while self.running:
                self.handle_events()
                if self.exit:
                    return False
                self.update()
        except KeyboardInterrupt:
            pygame.quit()
        return True
