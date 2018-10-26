from .player_entity import Player
from components import InputComponent


class PlayerInputComponent(InputComponent):
    def update(self, player: Player):
        try:
            key, up = self._get_input_key()
        except TypeError:
            return
