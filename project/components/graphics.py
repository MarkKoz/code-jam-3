import pygame

from .component import Component


class GraphicsComponent(Component):
    @staticmethod
    def load_textures(path: str, count: int, alpha: bool = True):
        for i in range(count):
            image: pygame.Surface = pygame.image.load(path.format(i))
            if alpha:
                image = image.convert_alpha()

            yield image
