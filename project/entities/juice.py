import pygame

from . import Entity

COLOUR = pygame.Color(255, 244, 79, 150)


class Juice(Entity):
    def __init__(self, *groups, **kwargs):
        super().__init__(*groups, **kwargs)

        self.image = pygame.Surface(self.size, pygame.SRCALPHA, 32)
        self.image.fill(COLOUR)

    def update(self, time_delta, key_events, world):
        if self.image.get_size() != tuple(self.size):
            self.position.y -= self.size.height - self.image.get_size()[1]
            self.image = pygame.transform.scale(self.image, self.size)
            self.image.fill(COLOUR)
            self.rect = self.image.get_rect()

        self.rect.topleft = self.position
