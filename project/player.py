import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        self.image = pygame.Surface((32, 48))
        self.image.fill(pygame.Color('yellow'))
        self.rect = self.image.get_rect()
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 8)

        self.velocity = [0, 0]
        self.position = [0, 0]
        self.max_x = 0  # Maximum x-coordinate reached.

    def update(self, time_delta):
        self.position[0] += self.velocity[0] * time_delta
        self.position[1] += self.velocity[1] * time_delta
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

        self.max_x = max(self.rect.center[0], self.max_x)
