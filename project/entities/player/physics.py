import copy

from .player_entity import Player
from components import PhysicsComponent
from utils import Point


class PlayerPhysicsComponent(PhysicsComponent):
    def __init__(self):
        self.max_x: float = 0  # Maximum x-coordinate reached.
        self._old_position: Point = Point(0, 0)

    def update(self, player: Player, time_delta):
        self._old_position = copy.copy(player.position)
        player.position.x += player.velocity.x * time_delta

        # Prevents movement further left than the screen.
        player.position.x = max(player.groups()[0].view[0], player.position.x)

        player.position.y += player.velocity.y * time_delta
        player.rect.topleft = player.position

        self.max_x = max(player.rect.centerx, self.max_x)
