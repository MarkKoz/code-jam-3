import pygame

PLAYER_SPEED = 200

# constants

PLAYER_SPEED = 300
GRAVITY = -20

# inputs
LEFT_KEYS = (pygame.K_LEFT, pygame.K_a)
RIGHT_KEYS = (pygame.K_RIGHT, pygame.K_d)
JUMP_KEYS = (pygame.K_SPACE, pygame.K_w, pygame.K_UP)


class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        self.image = pygame.Surface((16, 32))
        self.image.fill(pygame.Color('yellow'))
        self.rect = self.image.get_rect()
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 8)

        self.velocity = [0, 0]
        self.position = [0, 0]
        self._old_position = self.position[:]
        self.max_x = 0  # Maximum x-coordinate reached.
        self.is_jumping = False

    def update(self, time_delta, walls):
        self._old_position = self.position[:]

        self.position[0] += self.velocity[0] * time_delta

        # vertical movement
        if self.is_jumping:
            self.velocity[1] -= -50 * time_delta

        self.position[1] += self.velocity[1]

        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

        self.max_x = max(self.rect.center[0], self.max_x)

        if self.collides(walls['rects']):
            self.move_back()

    def move_back(self):
        self.position = self._old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def handle_input(self, event, up=False):
        speed = PLAYER_SPEED

        key = event.key
        current_keys = pygame.key.get_pressed()

        # vertical keys
        if key in JUMP_KEYS and self.is_jumping is False:

            if not up:
                self.is_jumping = True
                self.velocity[1] = -15

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

    def collides(self, obstacles):
        if self.feet.collidelist(obstacles) > -1:
            self.is_jumping = False
            return True
        return False
