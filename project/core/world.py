from typing import Tuple

import pygame
import pyscroll
import pytmx
from pytmx.util_pygame import load_pygame

from project.entities import Lemon
from project.utils import Point, Triangle


class World:
    def __init__(self, file_path):
        tmx_data = load_pygame(file_path)  # Load data from pytmx
        self.map_data = pyscroll.data.TiledMapData(tmx_data)  # Create new data source for pyscroll
        self.rects, self.slopes = self._get_collisions(tmx_data)
        self.gravity = -50
        self.lemons = [
            Lemon(position=Point(192, 3136)),
            Lemon(position=Point(288, 3104)),
            Lemon(position=Point(384, 3072))
        ]

    @staticmethod
    def _get_collisions(tmx_data: pytmx.TiledMap) -> Tuple:
        rects = []
        slopes = []

        obj: pytmx.TiledObject
        for obj in tmx_data.objects:
            points = getattr(obj, 'points', None)
            if points:
                slopes.append(Triangle(obj))
            else:
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                rects.append(rect)

        return tuple(rects), tuple(slopes)
