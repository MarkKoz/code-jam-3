import pygame

from .player_entity import Player
from components import InputComponent
from utils import Direction

ACCELERATION = 300
JUMP_KEYS = (pygame.K_SPACE, pygame.K_w, pygame.K_UP)
CONTROLS = {
    Direction.LEFT: (pygame.K_LEFT, pygame.K_a),
    Direction.RIGHT: (pygame.K_RIGHT, pygame.K_d)
}


class PlayerInputComponent(InputComponent):
    def update(self, player: Player, key: int, up: bool):
        if not up and not player.is_jumping and key in JUMP_KEYS:
            player.is_jumping = True
            player.velocity.y = -15
        elif key in CONTROLS[Direction.LEFT]:
            self._move(player, Direction.LEFT, up)
        elif key in CONTROLS[Direction.RIGHT]:
            self._move(player, Direction.RIGHT, up)

    @staticmethod
    def _move(player: Player, direction: Direction, up: bool):
        current_keys = pygame.key.get_pressed()
        accel = ACCELERATION if direction == direction.RIGHT else -ACCELERATION

        if up:
            if any(current_keys[k] for k in CONTROLS[-direction % 360]):
                player.velocity.x = -accel
                player.orientation = -direction
            else:
                player.velocity.x = 0
        else:
            player.velocity.x = accel
            player.orientation = direction
