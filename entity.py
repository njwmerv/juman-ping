import pygame
from game_constants import GRAVITY_ACC, TERMINAL_VELOCITY

class Entity(pygame.sprite.Sprite):
    # Attributes
    rect : pygame.Rect
    _image : pygame.image
    _width : int
    _height : int
    _vel_x : float = 0
    _vel_y : float = 0

    # Methods
    def __init__(self, pos : tuple[int, int], width : int, height : int, sprite_path : str = "", image : pygame.image = None):
        if sprite_path == "" and image is None: raise ValueError("Entity: At least one of sprite_path or image must be provided")
        super().__init__()
        if image is not None: self._image = pygame.transform.scale(image, size=(width, height)).convert_alpha()
        elif sprite_path != "": self._image = pygame.transform.scale(pygame.image.load(sprite_path), size=(width, height)).convert_alpha()
        self.rect = self._image.get_rect()
        self._width = width
        self._height = height
        self.rect.x, self.rect.y = pos

    def _accelerate_by_gravity(self, dt : float):
        new_vel_y : float = self._vel_y + (GRAVITY_ACC * dt)
        self._vel_y = min(TERMINAL_VELOCITY, new_vel_y)

    # Accessors/Setters
    @property
    def width(self) -> int: return self._width

    @property
    def height(self) -> int: return self._height

    @property
    def vel(self) -> tuple[float, float]: return self._vel_x, self._vel_y