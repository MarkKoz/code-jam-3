import pygame

from components import GraphicsComponent, InputComponent, PhysicsComponent
from entities import Entity
from utils import Direction


class Player(Entity):
    def __init__(self, graphics: GraphicsComponent, inp: InputComponent, physics: PhysicsComponent, *groups, **kwargs):
        super().__init__(*groups, **kwargs)

        self.max_x: float = 0  # Maximum x-coordinate reached.
        self.is_jumping: bool = False

        self._graphics = graphics
        self._input = inp
        self._physics = physics

        self.image.fill(pygame.Color('yellow'))  # TODO: For testing purposes

    @property
    def orientation(self) -> Direction:
        return Direction(self._orientation)

    @orientation.setter
    def orientation(self, direction: int):
        self._orientation = direction % 360
        if self._orientation not in (Direction.LEFT, Direction.RIGHT):
            raise ValueError('Player\'s orientation may only be left or right.')

    def update(self, time_delta: float, key_events, world):
        for key, up in key_events:
            self._input.update(self, key, up)

        self._physics.update(self, time_delta, world)
        self._graphics.update()
