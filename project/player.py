from typing import List

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
        self._old_position = self.position[:]
        self.max_x = 0  # Maximum x-coordinate reached.
        self.is_jumping = False

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
            self.velocity[0] = -speed
        elif key in RIGHT_KEYS:
            if up:
                left_pressed = any(current_keys[k] for k in LEFT_KEYS)
                speed = 0 if not left_pressed else -PLAYER_SPEED
            self.velocity[0] = speed

    def collides(self, obstacles: List[pygame.Rect]):
        if self.feet.collidelist(obstacles) > -1:
            self.is_jumping = False
            self.velocity[1] = 0
            self.position = self._old_position
            self.rect.topleft = self.position
            self.feet.midbottom = self.rect.midbottom

            return True

    def collides_slope(self, objects: List[pytmx.TiledObject]):
        for obj in objects:
            # Player's x relative to the collision object
            x = self.rect.x + self.rect.width - obj.x
            top = -1 * x + obj.y  # y = mx + b

            if x > obj.width:
                # Prevents weird behaviour when at the top of the slope.
                # Sets the player's y to the top of the slope.
                self.is_jumping = False
                self.velocity[1] = 0
                self.position[1] = obj.y - obj.height - self.rect.height
            elif self.rect.y + self.rect.height > top:
                self.is_jumping = False
                self.velocity[1] = 0
                self.position[1] = top - self.rect.height
