import pygame
from block import Block
from game_constants import CELL_SIZE, GRAVITY_ACC, TERMINAL_VELOCITY

# Platform Constants
SPRITE_PATH : str = './Assets/platform.png'
BROKEN_PATH : str = './Assets/falling_platform.png'
PLATFORM_WIDTH : int = 2 * CELL_SIZE
PLATFORM_HEIGHT : int = CELL_SIZE

class Platform(Block):
    # Attributes
    _vel_y : float = 0
    _falling : bool = False

    # Magic Methods
    def __init__(self, pos : tuple[int, int]):
        pos = (pos[0] - PLATFORM_WIDTH // 2, pos[1])
        super().__init__(sprite_path=SPRITE_PATH, pos=pos, width=PLATFORM_WIDTH, height=PLATFORM_HEIGHT, bot=True)

    # Accessors/Setters
    @property
    def is_falling(self) -> bool: return self._falling

    # Methods
    def collide(self):
        self._falling = True
        self.image = pygame.transform.scale(pygame.image.load(BROKEN_PATH), size=(PLATFORM_WIDTH, PLATFORM_HEIGHT)).convert_alpha()

    def _accelerate_by_gravity(self, dt : float):
        if self._falling:
            new_vel_y : float = self._vel_y + (GRAVITY_ACC * dt)
            self._vel_y = min(new_vel_y, TERMINAL_VELOCITY)

    def move(self, dt : float):
        self._accelerate_by_gravity(dt)
        self.rect.y += self._vel_y * dt
