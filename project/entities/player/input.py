import pygame

from project.components import InputComponent
from project.utils import Direction
from .player_entity import Player

JUMP_KEYS = (pygame.K_SPACE, pygame.K_w, pygame.K_UP)
CONTROLS = {
    Direction.LEFT: (pygame.K_LEFT, pygame.K_a),
    Direction.RIGHT: (pygame.K_RIGHT, pygame.K_d)
}

ACCELERATION = 300
WALK_ACCELERATION = 20
JUMP_VELOCITY = -15


class PlayerInputComponent(InputComponent):
    def __init__(self):
        self.acceleration = ACCELERATION

    def update(self, player: Player, key: int, up: bool):
        if key == pygame.K_LSHIFT and not up:
            self.acceleration = ACCELERATION if self.acceleration == WALK_ACCELERATION else WALK_ACCELERATION
        if not up and not player.is_jumping and key in JUMP_KEYS:
            player.is_jumping = True
            player.velocity.y = JUMP_VELOCITY
        elif key in CONTROLS[Direction.LEFT]:
            self._move(player, Direction.LEFT, up)
        elif key in CONTROLS[Direction.RIGHT]:
            self._move(player, Direction.RIGHT, up)

    def _move(self, player: Player, direction: Direction, up: bool):
        current_keys = pygame.key.get_pressed()
        accel = self.acceleration if direction == direction.RIGHT else -self.acceleration

        if up:
            if any(current_keys[k] for k in CONTROLS[-direction % 360]):
                player.velocity.x = -accel
                player.orientation = -direction
            else:
                player.velocity.x = 0
        else:
            player.velocity.x = accel
            player.orientation = direction
