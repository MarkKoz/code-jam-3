from typing import Tuple

import pygame

from project.utils import Point
from .component import Component


class PhysicsComponent(Component):
    def __init__(self):
        self._old_position: Point = Point(0, 0)

    @staticmethod
    def post_collision(collision: str, position: int, offset: int, surface: Tuple = None):
        event = pygame.event.Event(
            pygame.USEREVENT,
            collision=collision,
            position=position,
            offset=offset,
            surface=surface
        )
        pygame.event.post(event)
