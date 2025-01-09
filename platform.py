import pygame
from block import Block
from game_constants import FPS, GRAVITY_ACC, MAX_GRAVITY_VEL, PLATFORM_WIDTH, PLATFORM_HEIGHT

class Platform(Block):
    # Constants
    WIDTH : int = 35
    HEIGHT : int = 15
    SPRITE_PATH : str = "./Assets/platform.png"
    BROKEN_PATH : str = "./Assets/falling_platform.png"

    # Attributes
    _falling : bool
    _vel_y: float

    # Magic Methods
    def __init__(self, x : int, y : int, red = 255, green = 255, blue = 255):
        super().__init__(x=x, y=y, width=PLATFORM_WIDTH, height=PLATFORM_HEIGHT, red=red, green=green, blue=blue)
        self._falling = False
        self._vel_y = 0
        self._surface = pygame.transform.scale(pygame.image.load(self.SPRITE_PATH), (PLATFORM_WIDTH, PLATFORM_HEIGHT))

    # Accessors/Setters

    # Methods
    def collide(self):
        self._falling = True
        self._surface = pygame.transform.scale(pygame.image.load(self.BROKEN_PATH), (PLATFORM_WIDTH, PLATFORM_HEIGHT))

    def _accelerate_by_gravity(self):
        if self._falling:
            new_vel_y : float = self._vel_y + (GRAVITY_ACC / FPS)
            self._vel_y = new_vel_y if new_vel_y <= MAX_GRAVITY_VEL else MAX_GRAVITY_VEL

    def move(self):
        self._accelerate_by_gravity()
        self._y += self._vel_y
