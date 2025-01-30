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
    ACCELERATION : float = 0.5

    # Attributes
    _vel_x : float
    _vel_y : float
    _airborne : bool
    _jump_timer : int
    _jump_window : int
    _platforms_queue : list[Platform]

    # Magic Methods
    def __init__(self, x : int, y : int, width : int, height : int, sprite_path : str):
        super().__init__(x=x, y=y, width=width, height=height)
        self._vel_x = 0
        self._vel_y = 0
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

    @property
    def surface(self) -> pygame.SurfaceType:
        return self._surface

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

    def _vertical_move(self, jumping : bool):
        self._accelerate_by_gravity()

        if jumping:
            self._jump()
            self._y -= 1

        if not self._airborne:
            self._is_grounded()
        elif self._jump_window > 0:
            self._jump_window -= 1
        else:
            self._no_jump()
        self._y += self._vel_y

    def _horizontal_move(self, moving_left : bool, moving_right : bool):
        if moving_left:
            self._vel_x = max(-self.MOVEMENT_SPEED, self._vel_x - self.ACCELERATION)
        else:
            self._vel_x = max(0.0, self._vel_x)
        if moving_right:
            self._vel_x = min(self.MOVEMENT_SPEED, self._vel_x + self.ACCELERATION)
        else:
            self._vel_x = min(0.0, self._vel_x)
        self._x += self._vel_x

    # Public Methods
    def move(self, pressed_keys : ScancodeWrapper):
        """
        Wrapper for movement logic for the Player
        :param pressed_keys: ScancodeWrapper
        """
        moving_left : bool = pressed_keys[pygame.K_a] or pressed_keys[pygame.K_LEFT]
        moving_right : bool = pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]
        self._horizontal_move(moving_left, moving_right)
        jumping : bool = pressed_keys[pygame.K_SPACE] or pressed_keys[pygame.K_w] or pressed_keys[pygame.K_UP]
        self._vertical_move(jumping)

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
