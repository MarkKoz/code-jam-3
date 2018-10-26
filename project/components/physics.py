from .component import Component
from utils import Point


class PhysicsComponent(Component):
    def __init__(self):
        self._old_position: Point = Point(0, 0)
