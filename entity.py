import pygame

class Entity(pygame.sprite.Sprite):
    # Attributes
    _width : int
    _height : int
    _vel_x : float = 0
    _vel_y : float = 0

    # Methods
    def __init__(self, sprite_path : str, pos : (int, int), width : int, height : int):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(sprite_path), size=(width, height)).convert_alpha()
        self.rect = self.image.get_rect()
        self._width = width
        self._height = height
        self.rect.x, self.rect.y = pos

    # Accessors/Setters
    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def vel(self) -> (float, float):
        return self._vel_x, self._vel_y