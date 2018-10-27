from abc import ABC, abstractmethod

from pygame import Rect, Surface, sprite

from project.utils.point import Dimensions, Point


class Entity(sprite.Sprite, ABC):
    def __init__(self, *groups, **kwargs):
        super().__init__(*groups)

        self.position: Point = kwargs.get('position', Point(0, 0))
        self.velocity: Point = kwargs.get('velocity', Point(0, 0))
        self.size: Dimensions = kwargs.get('size', Dimensions(0, 0))
        self.image: Surface = kwargs.get('image', Surface(self.size))
        self._orientation: float = kwargs.get('orientation', 0)

        self.rect: Rect = self.image.get_rect()

    @property
    def orientation(self) -> float:
        return self._orientation

    @orientation.setter
    def orientation(self, degrees):
        self._orientation = degrees % 360

    @abstractmethod
    def update(self, *args):
        raise NotImplementedError

    def __repr__(self):
        return '{}\nV: ({:.3f}, {:.3f})\nJump: {}'.format(
            self.rect.bottomright, *self.velocity, self.is_jumping)
