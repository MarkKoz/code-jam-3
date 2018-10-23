import pygame
import pyscroll
from pytmx.util_pygame import load_pygame

from player import Player

DEFAULT_SIZE = (1280, 720)
PLAYER_SPEED = 200
FPS = 60
MAP_PATH = 'assets/map.tmx'

# Key Contants
UP_KEYS = (pygame.K_UP, pygame.K_w)
DOWN_KEYS = (pygame.K_DOWN, pygame.K_s)

LEFT_KEYS = (pygame.K_LEFT, pygame.K_a)
RIGHT_KEYS = (pygame.K_RIGHT, pygame.K_d)


class Game:
    def __init__(self):
        self.running = False
        self.screen = None
        self.surface = None

        self.set_screen(*DEFAULT_SIZE)
        self.map_layer = self.init_map()
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer)

        self.player = Player()

        # y = 0 is top but the map starts at the bottom.
        bottom = self.map_layer.data.map_size[1] * self.map_layer.data.tile_size[1]
        self.player.position = [64, bottom - 192]

        self.group.add(self.player, layer=3)

    def draw(self, surface):
        camera_pos = list(self.player.rect.center)
        camera_pos[0] = max(camera_pos[0], self.player.max_x)

        self.group.center(camera_pos)
        self.group.draw(surface)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.VIDEORESIZE:
                self.set_screen(event.w, event.h)
                self.map_layer.set_size((event.w / 2, event.h / 2))
            elif event.type == pygame.KEYDOWN:
                self.handle_input(event)
            elif event.type == pygame.KEYUP:
                self.handle_input(event, True)

    def handle_input(self, event, up=False):
        speed = PLAYER_SPEED

        key = event.key
        current_keys = pygame.key.get_pressed()

        # vertical keys
        if key in UP_KEYS:
            if up:
                down_pressed = any(current_keys[k] for k in DOWN_KEYS)
                speed = 0 if not down_pressed else -PLAYER_SPEED
            self.player.velocity[1] = -speed
        elif key in DOWN_KEYS:
            if up:
                up_pressed = any(current_keys[k] for k in UP_KEYS)
                speed = 0 if not up_pressed else -PLAYER_SPEED
            self.player.velocity[1] = speed

        # horizontal keys
        elif key in LEFT_KEYS:
            if up:
                right_pressed = any(current_keys[k] for k in RIGHT_KEYS)
                speed = 0 if not right_pressed else -PLAYER_SPEED
            self.player.velocity[0] = -speed
        elif key in RIGHT_KEYS:
            if up:
                left_pressed = any(current_keys[k] for k in LEFT_KEYS)
                speed = 0 if not left_pressed else -PLAYER_SPEED
            self.player.velocity[0] = speed

    def update(self, time_delta):
        self.group.update(time_delta)

    def run(self):
        """Starts the game's main loop."""
        self.running = True
        clock = pygame.time.Clock()

        try:
            while self.running:
                # Gets number of seconds since last call
                time_delta = clock.tick(FPS) / 1000

                self.handle_events()
                self.update(time_delta)
                self.draw(self.surface)

                # Resizes the surface and sets it as the new screen.
                pygame.transform.scale(
                    self.surface, self.screen.get_size(), self.screen)

                pygame.display.flip()  # Updates the display.
        except KeyboardInterrupt:
            self.running = False
            pygame.quit()

    def set_screen(self, width, height):
        """Simple wrapper to keep the screen resizeable."""
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.surface = pygame.Surface((width / 2, height / 2)).convert()

    def init_map(self):
        """Loads map data and creates a renderer."""
        tmx_data = load_pygame(MAP_PATH)  # Load data from pytmx

        # Create new data source for pyscroll
        map_data = pyscroll.data.TiledMapData(tmx_data)

        w, h = self.screen.get_size()

        # Create new renderer (camera)
        return pyscroll.BufferedRenderer(
            map_data, (w / 2, h / 2), clamp_camera=True
        )


def main():
    pygame.init()
    # pygame.font.init()

    try:
        game = Game()
        game.run()
    except Exception:
        pygame.quit()
        raise


if __name__ == '__main__':
    main()
