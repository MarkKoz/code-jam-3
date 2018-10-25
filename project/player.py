import math
import operator
from itertools import combinations
from typing import List, Tuple

import pygame
import pytmx

# constants

PLAYER_SPEED = 300
GRAVITY = -50

# inputs
LEFT_KEYS = (pygame.K_LEFT, pygame.K_a)
RIGHT_KEYS = (pygame.K_RIGHT, pygame.K_d)
JUMP_KEYS = (pygame.K_SPACE, pygame.K_w, pygame.K_UP)


class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        self.image = pygame.Surface((16, 32))
        self.image.fill(pygame.Color('yellow'))
        self.rect = self.image.get_rect()
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 8)

        self.velocity = [0, 0]
        self.position = [0, 0]
        self._orientation = 90
        self._old_position = self.position[:]
        self.max_x = 0  # Maximum x-coordinate reached.
        self.is_jumping = True

    @property
    def orientation(self):
        """The direction the player is facing, in degrees.

        Directions are clockwise with 0 representing up.
        """
        return self._orientation

    @orientation.setter
    def orientation(self, degrees):
        self._orientation = degrees % 360  # Ensures range is 0-360.

    def update(self, time_delta, collisions):
        self._old_position = self.position[:]

        self.position[0] += self.velocity[0] * time_delta

        # prevent player from moving further left than the screen
        self.position[0] = max(self.groups()[0].view[0], self.position[0])

        # vertical movement
        if self.is_jumping:
            self.velocity[1] -= GRAVITY * time_delta

        self.position[1] += self.velocity[1]

        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

        self.max_x = max(self.rect.center[0], self.max_x)

        if not self.collides(collisions['rects']):
            self.collides_slope(collisions['slopes'])

    def handle_input(self, event, up=False):
        speed = PLAYER_SPEED
        orientation = self.orientation

        key = event.key
        current_keys = pygame.key.get_pressed()

        # vertical keys
        if key in JUMP_KEYS and self.is_jumping is False:
            if not up:
                self.is_jumping = True
                self.velocity[1] = -15

        # horizontal keys
        elif key in LEFT_KEYS:
            if up:
                right_pressed = any(current_keys[k] for k in RIGHT_KEYS)
                speed = 0 if not right_pressed else -PLAYER_SPEED

                if right_pressed:
                    orientation = 90
            else:
                orientation = -90

            self.orientation = orientation
            self.velocity[0] = -speed
        elif key in RIGHT_KEYS:
            if up:
                left_pressed = any(current_keys[k] for k in LEFT_KEYS)
                speed = 0 if not left_pressed else -PLAYER_SPEED

                if left_pressed:
                    orientation = -90
            else:
                orientation = 90

            self.orientation = orientation
            self.velocity[0] = speed

    def collides(self, obstacles: List[pygame.Rect]):
        index = self.feet.collidelist(obstacles)
        if index > -1:
            collision_rect = obstacles[index]

            self.is_jumping = False
            self.velocity[1] = 0
            self.position = [self._old_position[0], collision_rect.top - self.rect.height]
            self.rect.topleft = self.position
            self.feet.midbottom = self.rect.midbottom

            return True

    def collides_slope(self, objects: List[pytmx.TiledObject]):
        # Don't check slopes if jumping up
        if self.velocity[1] < 0:
            return

        for obj in objects:
            # Skip slopes not in the same area as player
            if not ((obj.x <= self.rect.left <= obj.x + obj.width) or (obj.x <= self.rect.right <= obj.x + obj.width)):
                continue

            # TODO: Remove leeway of 5 because flat surface collision isn't precise
            if self.rect.bottom - 5 > obj.y or self.rect.bottom + 5 < obj.y - obj.height:
                continue

            # Skip if player is above the slope with offset of 5
            # This is to prevent snapping when jumping above the top of the slope
            # TODO: With this enabled, it's possible to fall off the map when landing on the slope.
            # if self.rect.bottom <= obj.y - obj.height - 5:
            #     continue

            slope = self._get_slope(obj.points)
            x = self._get_relative_x(obj)
            top = self._slope_intercept(obj, slope, x)

            if self.orientation == 90:
                compare = operator.lt if slope < 0 else operator.gt
            else:
                compare = operator.gt if slope < 0 else operator.lt

            if self.orientation == 90 and x > obj.width:
                # Prevents weird behaviour when at the end of the slope.
                self.is_jumping = False
                self.velocity[1] = 0
                self.position[1] = self._slope_intercept(obj, slope, obj.width) - self.rect.height
            elif self.orientation == 270 and x < 0:
                # Prevents weird behaviour when at the end of the slope.
                self.is_jumping = False
                self.velocity[1] = 0
                self.position[1] = self._slope_intercept(obj, slope, 0) - self.rect.height
            elif compare(top, self.rect.bottom):
                self.is_jumping = False
                self.velocity[1] = 0
                self.position[1] = top - self.rect.height

    def _get_relative_x(self, obj: pytmx.TiledObject) -> float:
        """Returns player's x position relative to the collision object."""
        player_x = self.rect.x + self.rect.width * 0.5
        return player_x - obj.x

    @staticmethod
    def _slope_intercept(obj: pytmx.TiledObject, slope: float, x: float) -> float:
        """For a given x, calculates the y position on a slope."""
        b = obj.y if slope < 0 else obj.y - obj.height  # y-intercept
        return slope * x + b  # y = mx + b

    @staticmethod
    def _point_distance(p: Tuple[Tuple[float]]) -> float:
        """Calculates the distance between two points."""
        return math.sqrt((p[0][0] - p[1][0]) ** 2 + (p[0][1] - p[1][1]) ** 2)

    @staticmethod
    def _get_slope(points: Tuple[Tuple[float]]) -> float:
        """Determines the slope of a triangle given its points."""
        combs = combinations(points, 2)
        a, b = max(combs, key=Player._point_distance)  # Finds the longest side; it's the hypotenuse
        return (b[1] - a[1]) / (b[0] - a[0])  # (y2 - y1) / (x2 - x2)

    def __repr__(self):
        return f'{self.rect.x}, {self.rect.y}'
