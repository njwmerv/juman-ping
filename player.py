import pygame
from block import Block
from entity import Entity
from platform import Platform
from pygame.key import ScancodeWrapper
from game_constants import FPS, GRAVITY_ACC, MAX_GRAVITY_VEL, JUMP_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT

class Player(Entity):
    # Constants
    JUMP_TIMER : int = 7
    JUMP_WINDOW : int = round(FPS / 2)
    MAX_PLATFORMS : int = 2
    MOVEMENT_SPEED : float = 3

    # Attributes
    _vel_y : float
    _airborne : bool
    _jump_timer : int
    _jump_window : int
    _platforms_queue : list[Platform]

    # Magic Methods
    def __init__(self, x : int, y : int, width : int, height : int, vel_y : float, sprite_path : str):
        super().__init__(x=x, y=y, width=width, height=height)
        self._vel_y = vel_y
        self._airborne = True
        self._jump_timer = 0
        self._jump_window = 0
        self._platforms_queue = []
        self._surface = pygame.transform.scale(pygame.image.load(sprite_path), (width, height))

    # Accessors/Setters
    @property
    def vel(self) -> float:
        return self._vel_y

    @property
    def platforms(self) -> list[Platform]:
        return self._platforms_queue

    # Private Methods
    def _accelerate_by_gravity(self):
        if self._airborne: # accelerate by gravity if airborne only
            new_vel_y : float = self._vel_y + (GRAVITY_ACC / FPS)
            self._vel_y = new_vel_y if new_vel_y <= MAX_GRAVITY_VEL else MAX_GRAVITY_VEL

    def _jump(self):
        if self._jump_timer >= 0 and not self._airborne:
            self._vel_y = JUMP_SPEED
            self._jump_timer -= 1
            self._airborne = True

    def _is_grounded(self):
        """
        Modifies a Player object to be grounded, i.e. can jump again
        :return:
        """
        self._vel_y = 0
        self._airborne = False
        self._jump_timer = self.JUMP_TIMER
        self._jump_window = self.JUMP_WINDOW

    def _no_jump(self):
        self._jump_timer = -1
        self._airborne = True

    def _vertical_move(self, pressed_keys : ScancodeWrapper):
        self._accelerate_by_gravity()

        if pressed_keys[pygame.K_SPACE] or pressed_keys[pygame.K_w] or pressed_keys[pygame.K_UP]:
            self._jump()
            self._y -= 1

        if not self._airborne:
            self._is_grounded()
        elif self._jump_window > 0:
            self._jump_window -= 1
        else:
            self._no_jump()
        self._y += self._vel_y

    def _horizontal_move(self, pressed_keys : ScancodeWrapper):
        if pressed_keys[pygame.K_a] or pressed_keys[pygame.K_LEFT]:
            self._x -= self.MOVEMENT_SPEED
        if pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]:
            self._x += self.MOVEMENT_SPEED

    # Public Methods
    def move(self, pressed_keys : ScancodeWrapper):
        """
        Handles movement logic for the Player
        :param pressed_keys: ScancodeWrapper
        """
        self._horizontal_move(pressed_keys)
        self._vertical_move(pressed_keys)

    def check_collisions(self, blocks : list[Block]):
        """
        Checks if a Player is colliding with terrain, like bottom/sides of the screen, or Blocks.
        Will make them "grounded" (can jump again) if yes.
        If a player ends up off-screen (horizontally), fix that too.
        :param blocks: list[Block]
        """
        if self._y + self._height > SCREEN_HEIGHT:
            self._is_grounded()
            self._y = SCREEN_HEIGHT - self._height
        if self._x < 0:
            self._x = 0
        elif self._x + self._width > SCREEN_WIDTH:
            self._x = SCREEN_WIDTH - self._width

        # TODO: define when a Player is colliding with a Block
        for block in blocks:
            pass

    def add_platform(self, pos : (int, int)):
        """
        Creates a new Platform at the given position (pos), and deletes the oldest Platform if there are too many
        :param pos: (int, int)
        """
        new_platform = Platform(x=pos[0], y=pos[1])
        if len(self._platforms_queue) == self.MAX_PLATFORMS:
            self._platforms_queue.pop(0)
        self._platforms_queue.append(new_platform)