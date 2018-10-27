import pygame

from project.utils import Dimensions
from . import Entity


class Lemon(Entity):
    def __init__(self, *groups, **kwargs):
        super().__init__(*groups, **kwargs)

        self.image: pygame.Surface = pygame.image.load('assets/textures/lemon.png').convert_alpha()
        self.rect: pygame.Rect = self.image.get_rect()
        self.size = Dimensions(*self.rect.size)

    def update(self, time_delta, key_events, world):
        self.rect.topleft = self.position

        if self.rect.colliderect(world.player.rect):
            event = pygame.event.Event(pygame.USEREVENT + 1, lemon=self)
            pygame.event.post(event)
