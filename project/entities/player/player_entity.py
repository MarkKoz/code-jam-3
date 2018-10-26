import pygame

from components import GraphicsComponent, InputComponent, PhysicsComponent
from entities import Entity
from utils import Direction


class Player(Entity, pygame.sprite.Sprite):
    def __init__(self, graphics: GraphicsComponent, inp: InputComponent, physics: PhysicsComponent, *groups, **kwargs):
        pygame.sprite.Sprite.__init__(self, *groups)
        Entity.__init__(self, **kwargs)

        self.image = pygame.Surface(self.size)
        self.image.fill(pygame.Color('yellow'))
        self.rect: pygame.Rect = self.image.get_rect()

        self.max_x: float = 0  # Maximum x-coordinate reached.

        self._graphics = graphics
        self._input = inp
        self._physics = physics

    @property
    def orientation(self) -> Direction:
        return Direction(self._orientation)

    @orientation.setter
    def orientation(self, direction: int):
        if direction not in (Direction.LEFT, Direction.RIGHT):
            raise ValueError('Player\'s orientation may only be left or right.')
        self._orientation = int(self._orientation)

    def update(self, time_delta: float, world):
        self._input.update(self)
        self._physics.update(self, time_delta)
        self._graphics.update()
