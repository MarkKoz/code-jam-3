import pygame

from project.core import Game

pygame.init()

try:
    game = Game()
    game.run()
except Exception:
    pygame.quit()
    raise
