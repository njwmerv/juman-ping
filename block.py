import pygame

# Block Constants
DIRECTIONS : list[str] = ["top", "bot", "left", "right"]

class Block(pygame.sprite.Sprite):
    # Attributes
    _passthrough : dict[str, bool] = {"top":False, "bot":False, "left":False, "right":False}

    # Magic Methods
    def __init__(self, sprite_path: str, pos: (int, int), width: int, height: int, passthrough : dict[str, bool] = {}):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(sprite_path), size=(width, height)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        for direction in DIRECTIONS:
            if direction in passthrough.keys() and type(passthrough[direction]) == bool:
                self._passthrough[direction] = passthrough[direction]

    # Accessors/Setters
    @property
    def passthrough(self) -> dict[str, bool]:
        return self._passthrough

    # Methods
