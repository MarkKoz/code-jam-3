from abc import ABC, abstractmethod

from utils.point import Point


class Entity(ABC):
    def __init__(self, **kwargs):
        self.position: Point = kwargs.get('position', Point(0, 0))
        self.velocity: Point = kwargs.get('velocity', Point(0, 0))
        self.size: Point = kwargs.get('size', Point(0, 0))
        self._orientation: float = kwargs.get('orientation', 0)

    @property
    def orientation(self) -> float:
        return self._orientation

    @orientation.setter
    def orientation(self, degrees):
        self._orientation = degrees % 360

    @abstractmethod
    def update(self, *args):
        raise NotImplementedError
