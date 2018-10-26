from pygame.sprite import Sprite

from components import GraphicsComponent, InputComponent, PhysicsComponent
from entities.entity import Entity


class Player(Entity, Sprite):
    def __init__(self, graphics: GraphicsComponent, _input: InputComponent, physics: PhysicsComponent, **kwargs):
        super().__init__(**kwargs)

        self._graphics = graphics
        self._input = _input
        self._physics = physics

    def update(self, *args):
        pass
