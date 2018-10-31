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
        self.tmx_data = load_pygame(file_path)  # Load data from pytmx
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)  # Create new data source for pyscroll
        self.rects, self.slopes = self._get_collisions(self.tmx_data)

        self.gravity = -50
        self.player: Player = None
        self.juice: Juice = None
        self.lemons: Tuple[Lemon] = tuple(self._get_lemons(self.tmx_data))

        self.reset()

    def reset(self):
        # y = 0 is top but the map starts at the bottom.
        right = self.map_data.map_size[0] * self.map_data.tile_size[0]
        bottom = self.map_data.map_size[1] * self.map_data.tile_size[1]

        self.player = self._get_player(self.tmx_data)
        self.juice = Juice(size=Dimensions(right, 1), position=Point(0, bottom))

    @staticmethod
    def _get_collisions(tmx_data: pytmx.TiledMap) -> Tuple:
        rects = []
        slopes = []

        obj: pytmx.TiledObject
        for obj in tmx_data.get_layer_by_name('collision'):
            points = getattr(obj, 'points', None)
            if points:
                slopes.append(Triangle(obj))
            else:
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                rects.append(rect)

        return tuple(rects), tuple(slopes)

    @staticmethod
    def _get_lemons(tmx_data: pytmx.TiledMap):
        obj: pytmx.TiledObject
        for obj in tmx_data.get_layer_by_name('spawns'):
            if obj.name == 'lemon':
                yield Lemon(position=Point(obj.x, obj.y))

    @staticmethod
    def _get_player(tmx_data: pytmx.TiledMap):
        player: pytmx.TiledObject = tmx_data.get_object_by_name('player')
        size = Dimensions(27, 35)
        return Player(
            PlayerGraphicsComponent(),
            PlayerInputComponent(),
            PlayerPhysicsComponent(),
            position=Point(player.x, player.y - size.height),
            size=size
        )
