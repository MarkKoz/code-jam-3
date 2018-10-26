from project.utils import Point
from .component import Component


class PhysicsComponent(Component):
    def __init__(self):
        self._old_position: Point = Point(0, 0)
