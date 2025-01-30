import pygame
from entity import Entity

class Block(Entity):
    # Constants
    SPRITE_PATH : str = "./Assets/goal_flag.png" # This is temporary
    DIRECTIONS : list[str] = ["top", "bot", "left", "right"]

    # Attributes
    _passthrough = {"top":False, "bot":False, "left":False, "right":False}

    # Magic Methods
    def __init__(self, x : int, y : int, width : int, height : int, passthrough : dict[str, bool] = {}):
        super().__init__(x=x, y=y, width=width, height=height)
        for direction in self.DIRECTIONS:
            if direction in passthrough.keys() and type(passthrough[direction]) == bool:
                self._passthrough[direction] = passthrough[direction]
        self._surface = pygame.transform.scale(pygame.image.load(self.SPRITE_PATH), (width, height))

    # Accessors/Setters
    @property
    def passthrough(self) -> (bool, bool, bool, bool):
        return self._passthrough.values()

    # Methods
