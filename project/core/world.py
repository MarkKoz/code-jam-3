from typing import Tuple

import pygame
import pyscroll
import pytmx
from pytmx.util_pygame import load_pygame

from project.entities import Juice, Lemon
from project.entities.player import Player, PlayerGraphicsComponent, PlayerInputComponent, PlayerPhysicsComponent
from project.utils import Dimensions, Point, Triangle


class World:
    def __init__(self, file_path):
        tmx_data = load_pygame(file_path)  # Load data from pytmx
        self.map_data = pyscroll.data.TiledMapData(tmx_data)  # Create new data source for pyscroll
        self.rects, self.slopes = self._get_collisions(tmx_data)

        self.gravity = -50

        # y = 0 is top but the map starts at the bottom.
        right = self.map_data.map_size[0] * self.map_data.tile_size[0]
        bottom = self.map_data.map_size[1] * self.map_data.tile_size[1]

        # TODO: Read spawn positions from map file?
        self.player = Player(
            PlayerGraphicsComponent(),
            PlayerInputComponent(),
            PlayerPhysicsComponent(),
            position=Point(64, bottom - 192),
            size=Dimensions(16, 32)
        )
        self.lemons = [
            Lemon(position=Point(192, bottom - 64)),
            Lemon(position=Point(288, bottom - 96)),
            Lemon(position=Point(384, bottom - 128))
        ]
        self.juice = Juice(size=Dimensions(right, 1), position=Point(0, bottom))

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
