import pygame

from utils import Dimensions
from . import Entity


class Lemon(Entity):
    def __init__(self, *groups, **kwargs):
        super().__init__(*groups, **kwargs)

        self.image: pygame.Surface = pygame.image.load('assets/textures/lemon.png').convert_alpha()
        self.rect: pygame.Rect = self.image.get_rect()
        self.size = Dimensions(*self.rect.size)

    def update(self, *args):
        self.rect.topleft = self.position
