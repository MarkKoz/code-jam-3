import copy
from typing import Sequence

import pygame

from project.components import PhysicsComponent
from project.utils import Direction, Point, Triangle
from .player_entity import Player


class PlayerPhysicsComponent(PhysicsComponent):
    def update(self, player: Player, time_delta: float, world):
        self._old_position = copy.copy(player.position)
        player.position.x += player.velocity.x * time_delta

        # Prevents movement further left than the screen.
        player.position.x = max(player.groups()[0].view[0], player.position.x)

        if player.is_jumping:
            player.velocity.y -= world.gravity * time_delta

        player.position.y += player.velocity.y
        player.rect.topleft = player.position

        player.max_x = max(player.rect.centerx, player.max_x)

        # Player fell into the lemon juice.
        if player.rect.colliderect(world.juice.rect):
            event = pygame.event.Event(pygame.USEREVENT + 2)
            pygame.event.post(event)

        if not self._handle_slope_collision(player, world.slopes):
            if not self._handle_rect_collision(player, world.rects) and not player.is_jumping:
                player.is_jumping = True

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
                player.position.y = obj.top - player.rect.height + 1
            # TODO: These checks need to be changed to reflect intended behavior. Copied to prevent falling through
            elif top_left or bottom_left:
                player.is_jumping = False
                player.velocity.y = 0
                player.position.y = obj.top - player.rect.height + 1
            elif top_right or bottom_right:
                player.is_jumping = False
                player.velocity.y = 0
                player.position.y = obj.top - player.rect.height + 1

                player.rect.topleft = player.position

            self.post_collision('rect', obj.top, 1, (obj.topleft, obj.topright))
            return True

    @staticmethod
    def _handle_slope_collision(player: Player, objects: Sequence[Triangle]) -> bool:
        # Don't check slopes if jumping up
        if player.velocity.y < 0:
            return False

        for obj in objects:
            # Skip slopes not in the same area as player
            if not (
                obj.x <= player.rect.centerx <= obj.x + obj.width
                and obj.y >= player.rect.bottom - 1 >= obj.y - obj.height
            ):
                continue

            x = player.rect.centerx - obj.x  # Player's x relative to the object
            y = obj.slope_intercept(x)

            # Skip if player is more than 1 unit above the slope.
            # This prevents snapping to the bottom while jumping over the slope.
            if player.rect.bottom <= y - 1:
                continue

            # Prevents weird behaviour when at the end of the slope.
            if player.orientation == Direction.RIGHT and x > obj.width:
                y = obj.hypotenuse[1].y
            elif player.orientation == Direction.LEFT and x < 0:
                y = obj.hypotenuse[0].y

            player.is_jumping = False
            player.velocity.y = 0
            player.position.y = y - player.rect.height + 1

            PlayerPhysicsComponent.post_collision('slope', int(y), 1, obj.hypotenuse)
            return True

        return False
