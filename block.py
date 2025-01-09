import pygame
from entity import Entity

class Block(Entity):
    # Constants
    SPRITE_PATH = "./Assets/goal_flag.png"

    # Attributes
    _colour : (int, int, int)

    # Magic Methods
    def __init__(self, x : int, y : int, width : int, height : int, red : int, green : int, blue : int):
        super().__init__(x=x, y=y, width=width, height=height)
        new_red = min(255, max(0, red))
        new_green = min(255, max(0, green))
        new_blue = min(255, max(0, blue))
        self._colour = (new_red, new_green, new_blue)
        self._surface = pygame.transform.scale(pygame.image.load(self.SPRITE_PATH), (width, height))

    # Accessors/Setters
    @property
    def colour(self) -> (int, int, int):
        return self._colour

    # Methods
