import pygame

from .player_entity import Player
from components import InputComponent
from utils import Direction

ACCELERATION = 300
CONTROLS = {
    Direction.LEFT: (pygame.K_LEFT, pygame.K_a),
    Direction.RIGHT: (pygame.K_RIGHT, pygame.K_d)
}


class PlayerInputComponent(InputComponent):
    def update(self, player: Player, key: int, up: bool):
        if key in CONTROLS[Direction.LEFT]:
            self._move(player, Direction.LEFT, up)
        elif key in CONTROLS[Direction.RIGHT]:
            self._move(player, Direction.RIGHT, up)

    @staticmethod
    def _move(player: Player, direction: Direction, up: bool):
        current_keys = pygame.key.get_pressed()

        if up:
            if any(current_keys[k] for k in CONTROLS[-direction % 360]):
                player.velocity.x = -ACCELERATION
                player.orientation = -direction
            else:
                player.velocity.x = 0
        else:
            player.velocity.x = -ACCELERATION
            player.orientation = direction
