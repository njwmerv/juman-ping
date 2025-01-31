from abc import ABC, abstractmethod
from pygame import SurfaceType

class Entity(ABC):
    # Constants

    # Attributes
    _x : int
    _y : int
    _width : int
    _height : int
    _surface : SurfaceType

    # Methods
    def __init__(self, x : int, y : int, width : int, height : int):
        self._x = x if x > 0 else 0
        self._y = y if y > 0 else 0
        self._width = width if width > 0 else 0
        self._height = height if height > 0 else 0

    # Accessors/Setters
    @property
    @abstractmethod
    def surface(self):
        pass

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
    def top(self) -> int:
        return self._y

    @property
    def bot(self) -> int:
        return self._y + self._height

    @property
    def left(self) -> int:
        return self._x

    @property
    def right(self) -> int:
        return self._x + self._width

    @property
    def center(self) -> (int, int):
        return self._x + (self._width / 2), self._y + (self._height / 2)
