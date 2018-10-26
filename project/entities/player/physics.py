import copy
import operator
from typing import Sequence

import pygame

from .player_entity import Player
from components import PhysicsComponent
from utils import Direction, Triangle, Point

GRAVITY = -50


class PlayerPhysicsComponent(PhysicsComponent):
    def update(self, player: Player, time_delta: float, world):
        self._old_position = copy.copy(player.position)
        player.position.x += player.velocity.x * time_delta

        # Prevents movement further left than the screen.
        player.position.x = max(player.groups()[0].view[0], player.position.x)

        if player.is_jumping:
            player.velocity.y -= GRAVITY * time_delta

        player.position.y += player.velocity.y
        player.rect.topleft = player.position

        player.max_x = max(player.rect.centerx, player.max_x)

        if not self._handle_slope_collision(player, world.slopes):
            self._handle_rect_collision(player, world.rects)

    def _handle_rect_collision(self, player: Player, objects: Sequence[pygame.Rect]) -> bool:
        index = player.rect.collidelist(objects)
        if index > -1:
            obj = objects[index]

            top_left = obj.collidepoint(player.rect.topleft)
            top_right = obj.collidepoint(player.rect.topright)
            bottom_left = obj.collidepoint(player.rect.bottomleft)
            bottom_right = obj.collidepoint(player.rect.bottomright)

            if (top_left and bottom_left) or (top_right and bottom_right):
                player.position.x = self._old_position.x
            elif top_left and top_right:
                player.velocity.y = 0
                player.position = Point(self._old_position.x, obj.bottom)
            elif bottom_left and bottom_right:
                player.is_jumping = False
                player.velocity.y = 0
                player.position = Point(self._old_position.x, obj.top - player.rect.height)
            # TODO: These checks need to be changed to reflect intended behavior. Copied to prevent falling through
            elif top_left or bottom_left:
                player.is_jumping = False
                player.velocity.y = 0
                player.position = Point(self._old_position.x, obj.top - player.rect.height)
            elif top_right or bottom_right:
                player.is_jumping = False
                player.velocity.y = 0
                player.position = Point(self._old_position.x, obj.top - player.rect.height)

                player.rect.topleft = player.position

            return True

    @staticmethod
    def _handle_slope_collision(player: Player, objects: Sequence[Triangle]) -> bool:
        # Don't check slopes if jumping up
        if player.velocity.y < 0:
            return False

        for obj in objects:
            # Skip slopes not in the same area as player
            if not (obj.x <= player.rect.left <= obj.x + obj.width or obj.x <= player.rect.right <= obj.x + obj.width):
                continue

            # TODO: Remove leeway of 5 because flat surface collision isn't precise
            if player.rect.bottom - 5 > obj.y or player.rect.bottom + 5 < obj.y - obj.height:
                continue

            # Skip if player is above the slope with offset of 5
            # This is to prevent snapping when jumping above the top of the slope
            # TODO: With this enabled, it's possible to fall off the map when landing on the slope.
            # if self.rect.bottom <= obj.y - obj.height - 5:
            #     continue

            x = player.rect.x + player.rect.width * 0.5 - obj.x  # Player's x relative to the object
            y = obj.slope_intercept(x)

            if player.orientation == Direction.RIGHT:
                compare = operator.lt if obj.slope < 0 else operator.gt
            else:
                compare = operator.gt if obj.slope < 0 else operator.lt

            # Prevents weird behaviour when at the end of the slope.
            if player.orientation == Direction.RIGHT and x > obj.width:
                y = obj.slope_intercept(obj.width)
            elif player.orientation == Direction.LEFT and x < 0:
                y = obj.slope_intercept(0)
            elif not compare(y, player.rect.bottom):
                y = None

            if y is not None:
                player.is_jumping = False
                player.velocity.y = 0
                player.position.y = y - player.rect.height

                return True

        return False
