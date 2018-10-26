from abc import ABC, abstractmethod
from typing import Optional, Tuple

import pygame

from .component import Component


class InputComponent(ABC, Component):
    @staticmethod
    @abstractmethod
    def _get_input_key() -> Optional[Tuple[int, bool]]:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return event.key, False
            elif event.type == pygame.KEYUP:
                return event.key, True
