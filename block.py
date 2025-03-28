import pygame

# Block Constants
DIRECTIONS : list[str] = ["top", "bot", "left", "right"]

class Block(pygame.sprite.Sprite):
    # Attributes
    _passthrough : dict[str, bool]

    # Magic Methods
    def __init__(self, pos: tuple[int, int], width: int, height: int,
                 top : bool = False, bot : bool = False, left : bool = False, right : bool = False,
                 sprite_path: str = "", image : pygame.image = None):
        if sprite_path == "" and image is None: raise ValueError("Block: At least one of sprite_path or image must be provided")
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(sprite_path), size=(width, height)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self._passthrough = {"top": top, "bot": bot, "left": left, "right": right}

    # Accessors/Setters
    @property
    def passthrough(self) -> dict[str, bool]: return self._passthrough

    # Methods
    def collide(self): return
