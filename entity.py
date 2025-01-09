from abc import abstractproperty
from pygame import SurfaceType

class Entity:
    # Constants

    # Attributes
    _x : int
    _y : int
    _width : int
    _height : int
    _surface : SurfaceType = abstractproperty

    # Methods
    def __init__(self, x : int, y : int, width : int, height : int):
        self._x = x if x > 0 else 0
        self._y = y if y > 0 else 0
        self._width = width if width > 0 else 0
        self._height = height if height > 0 else 0

    # Accessors/Setters
    @property
    def pos(self) -> (int, int):
        return self._x, self._y

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def surface(self) -> SurfaceType:
        return self._surface
