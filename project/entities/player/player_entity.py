import pygame

from components import GraphicsComponent, InputComponent, PhysicsComponent
from entities import Entity
from utils import Direction


class Player(Entity, pygame.sprite.Sprite):
    def __init__(self, graphics: GraphicsComponent, _input: InputComponent, physics: PhysicsComponent, **kwargs):
        super().__init__(**kwargs)

        self.image = pygame.Surface(self.size)
        self.image.fill(pygame.Color('yellow'))
        self.rect: pygame.Rect = self.image.get_rect()

        self._graphics = graphics
        self._input = _input
        self._physics = physics

    @property
    def orientation(self) -> Direction:
        return Direction(self._orientation)

    @orientation.setter
    def orientation(self, direction: int):
        if direction not in (Direction.LEFT, Direction.RIGHT):
            raise ValueError('Player\'s orientation may only be left or right.')
        self._orientation = int(self._orientation)

    def update(self, *args):
        pass
