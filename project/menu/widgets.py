import pygame

from project.core.constants import FONTS, SCREEN_SCALE
from project.utils import Dimensions, Point

SCALE = 2


class ButtonBorder(pygame.sprite.Sprite):
    def __init__(self, image_path: str, flip_x: bool = False, flip_y: bool = False, *groups):
        super().__init__(groups)

        self.image: pygame.Surface = pygame.image.load(image_path)
        self.image = pygame.transform.flip(self.image, flip_x, flip_y)
        w, h = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (w * SCALE, h * SCALE))
        self.rect: pygame.Rect = self.image.get_rect()


class ButtonText(pygame.sprite.Sprite):
    def __init__(self, text: str, min_size: Dimensions, *groups):
        super().__init__(groups)

        self.text = text
        self.min_size = min_size
        self.image: pygame.Surface = self.get_text()
        self.rect: pygame.Rect = self.image.get_rect()

    def get_text(self) -> pygame.Surface:
        text_surface = create_label(self.text, 'monogram', 32, 'black')
        size = Dimensions(*text_surface.get_size())
        pos = Point(0, 0)
        if size < self.min_size:
            pos.x = (self.min_size.width - size.width) // 2
            pos.y = (self.min_size.height - size.height) // 2 - 3  # TODO: Implement proper fix for centering on y
            size = self.min_size

        image: pygame.Surface = pygame.Surface(size)
        image.fill(pygame.Color('white'))
        image.blit(text_surface, pos)

        return image


class Button:
    def __init__(self, text: str, min_size: Dimensions, command=None, shortcut=None):
        self.command = command
        self.shortcut = shortcut

        self.group = pygame.sprite.LayeredUpdates()

        text_sprite = ButtonText(text, min_size)
        self.group.add(text_sprite, layer=0)

        w, h = text_sprite.rect.size
        self.surface: pygame.Surface = pygame.Surface((w + 8 * SCALE, h + 8 * SCALE))
        self.rect: pygame.Rect = self.surface.get_rect()
        text_sprite.rect.center = self.rect.center

        for y in range(self.rect.height):
            left = ButtonBorder('assets/textures/button/side.png')
            right = ButtonBorder('assets/textures/button/side.png', True)
            left.rect.topleft = (self.rect.left, y)
            right.rect.topright = (self.rect.right, y)
            self.group.add(left, layer=1)
            self.group.add(right, layer=1)

        for x in range(self.rect.width):
            top = ButtonBorder('assets/textures/button/top.png')
            bottom = ButtonBorder('assets/textures/button/bottom.png')
            top.rect.topleft = (x, self.rect.top)
            bottom.rect.bottomleft = (x, self.rect.bottom)
            self.group.add(top, layer=1)
            self.group.add(bottom, layer=1)

        top_left = ButtonBorder('assets/textures/button/corner.png')
        top_right = ButtonBorder('assets/textures/button/corner.png', True)
        bottom_left = ButtonBorder('assets/textures/button/corner.png', False, True)
        bottom_right = ButtonBorder('assets/textures/button/corner.png', True, True)
        top_left.rect.topleft = self.rect.topleft
        top_right.rect.topright = self.rect.topright
        bottom_left.rect.bottomleft = self.rect.bottomleft
        bottom_right.rect.bottomright = self.rect.bottomright
        self.group.add(top_left, layer=2)
        self.group.add(top_right, layer=2)
        self.group.add(bottom_left, layer=2)
        self.group.add(bottom_right, layer=2)

        left_centre = ButtonBorder('assets/textures/button/left-centre.png')
        right_centre = ButtonBorder('assets/textures/button/right-centre.png')
        left_centre.rect.midleft = (self.rect.left + 3 * SCALE, self.rect.centery)
        right_centre.rect.midright = (self.rect.right - 3 * SCALE, self.rect.centery)
        self.group.add(left_centre, layer=2)
        self.group.add(right_centre, layer=2)

    def draw(self, surface: pygame.Surface):
        self.group.draw(self.surface)
        surface.blit(self.surface, self.rect)

    def handle_event(self, event):
        if event.type == pygame.KEYUP and event.key == self.shortcut:
            if self.command:
                self.command()
        elif event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            if self.rect.collidepoint((x / SCREEN_SCALE, y / SCREEN_SCALE)):
                # TODO: Hover effect
                pass
        elif event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            if self.rect.collidepoint((x / SCREEN_SCALE, y / SCREEN_SCALE)):
                if self.command:
                    self.command()
            return True


def create_label(text, font_name, size, fg: str = 'white', bg: str = None):
    if font_name in FONTS:
        font = pygame.font.Font(FONTS[font_name], size)
    else:
        font = pygame.font.SysFont(font_name, size)

    font_surface: pygame.Surface = font.render(text, False, pygame.Color(fg), pygame.Color(bg) if bg else bg)
    return font_surface


def create_multiline_label(text: str, font_name: str, size: int, fg: str = 'white', bg: str = None):
    if font_name in FONTS:
        font = pygame.font.Font(FONTS[font_name], size)
    else:
        font = pygame.font.SysFont(font_name, size)

    fg = pygame.Color(fg)
    surfaces = []
    heights = []
    width = 0
    height = 0

    for line in text.split('\n'):
        font_surface: pygame.Surface = font.render(line, False, fg)
        surfaces.append(font_surface)
        surface_width, surface_height = font_surface.get_size()
        heights.append(height)
        height += surface_height
        if surface_width > width:
            width = surface_width

    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    if bg:
        surface.fill(pygame.Color(bg))
    else:
        surface = surface.convert_alpha()

    for font_surface, height_offset in zip(surfaces, heights):
        surface.blit(font_surface, (width / 2 - font_surface.get_width() / 2, height_offset))
    return surface
