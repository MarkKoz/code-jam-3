from pygame.sprite import Sprite

from components import GraphicsComponent, InputComponent, PhysicsComponent
from entities.entity import Entity
from utils.direction import Direction


class Player(Entity, Sprite):
    def __init__(self, graphics: GraphicsComponent, _input: InputComponent, physics: PhysicsComponent, **kwargs):
        super().__init__(**kwargs)

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
