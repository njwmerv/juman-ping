import pygame
from block import Block
from game_constants import FPS, CELL_SIZE, GRAVITY_ACC, MAX_GRAVITY_VEL

# Platform Constants
SPRITE_PATH : str = './Assets/platform.png'
BROKEN_PATH : str = './Assets/falling_platform.png'
PLATFORM_WIDTH : int = CELL_SIZE
PLATFORM_HEIGHT : int = CELL_SIZE // 2

class Platform(Block):
    # Attributes
    _vel_y : float = 0
    _falling : bool = False

    # Magic Methods
    def __init__(self, pos : (int, int)):
        pos = (pos[0] - PLATFORM_WIDTH // 2, pos[1] - PLATFORM_HEIGHT // 2)
        super().__init__(sprite_path=SPRITE_PATH, pos=pos, width=PLATFORM_WIDTH, height=PLATFORM_HEIGHT, bot=True, left=True, right=True)

    # Accessors/Setters

    # Methods
    def collide(self):
        self._falling = True
        self.image = pygame.transform.scale(pygame.image.load(BROKEN_PATH), size=(PLATFORM_WIDTH, PLATFORM_HEIGHT)).convert_alpha()

    def _accelerate_by_gravity(self):
        if self._falling:
            new_vel_y : float = self._vel_y + (GRAVITY_ACC / FPS)
            self._vel_y = new_vel_y if new_vel_y <= MAX_GRAVITY_VEL else MAX_GRAVITY_VEL

    def move(self):
        self._accelerate_by_gravity()
        self.rect.y += self._vel_y
