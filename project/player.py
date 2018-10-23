import pygame

PLAYER_SPEED = 200

# Key constants
UP_KEYS = (pygame.K_UP, pygame.K_w)
DOWN_KEYS = (pygame.K_DOWN, pygame.K_s)

LEFT_KEYS = (pygame.K_LEFT, pygame.K_a)
RIGHT_KEYS = (pygame.K_RIGHT, pygame.K_d)


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

    def handle_input(self, event, up=False):
        speed = PLAYER_SPEED

        key = event.key
        current_keys = pygame.key.get_pressed()

        # vertical keys
        if key in UP_KEYS:
            if up:
                down_pressed = any(current_keys[k] for k in DOWN_KEYS)
                speed = 0 if not down_pressed else -PLAYER_SPEED
            self.velocity[1] = -speed
        elif key in DOWN_KEYS:
            if up:
                up_pressed = any(current_keys[k] for k in UP_KEYS)
                speed = 0 if not up_pressed else -PLAYER_SPEED
            self.velocity[1] = speed

        # horizontal keys
        elif key in LEFT_KEYS:
            if up:
                right_pressed = any(current_keys[k] for k in RIGHT_KEYS)
                speed = 0 if not right_pressed else -PLAYER_SPEED
            self.velocity[0] = -speed
        elif key in RIGHT_KEYS:
            if up:
                left_pressed = any(current_keys[k] for k in LEFT_KEYS)
                speed = 0 if not left_pressed else -PLAYER_SPEED
            self.velocity[0] = speed
