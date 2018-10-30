from collections import deque

from project.components import GraphicsComponent
from .player_entity import Player


class PlayerGraphicsComponent(GraphicsComponent):
    def __init__(self):
        super().__init__()

        self.idle = deque(self.load_textures('assets/textures/player/idle-0{}.png', 4))
        self.run = deque(self.load_textures('assets/textures/player/run-0{}.png', 6))
        self.jump = tuple(self.load_textures('assets/textures/player/jump-0{}.png', 4))
        self.fall = tuple(self.load_textures('assets/textures/player/fall-0{}.png', 2))

    def update(self, player: Player):
        if player.is_jumping:
            # TODO: Use jumping textures
            pass
        elif player.velocity.x > 0:
            player.image = self.run[0]
            self.run.rotate(-1)
        elif player.velocity.x == 0:
            player.image = self.idle[0]
            self.idle.rotate(-1)
