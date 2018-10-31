from project.utils import Dimensions

TITLE = 'The Lemon Apocalypse'
DEFAULT_SIZE = Dimensions(1280, 720)
FPS = 60
MAP_PATH = 'assets/map.tmx'
JUICE_FILL_RATE = 5
SCREEN_SCALE = 2

FONTS = {
    'too much ink': 'assets/fonts/TooMuchInk.ttf',
    'monogram': 'assets/fonts/monogram_extended.ttf'
}

CONTROLS_HELP_TEXT = b"""\
Forward: D or \xe2\x86\x92
Back: A or \xe2\x86\x90
Jump: W or SPACE or \xe2\x86\x91
Slow: SHIFT
Reset: R
Quit: ESC""".decode('utf-8')
