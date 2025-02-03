import pygame
from block import Block
from entity import Entity
from platform import Platform
from game_constants import FPS, CELL_SIZE, GRAVITY_ACC, MAX_GRAVITY_VEL, SCREEN_WIDTH, SCREEN_HEIGHT

# Player Constants
BLUE_WIDTH : int = CELL_SIZE * 2
JUMP_SPEED : float = -6
JUMP_TIMER : int = 7
BLUE_HEIGHT : int = CELL_SIZE * 3
JUMP_WINDOW : int = round(FPS / 2)
SPRITE_PATH : str = './Assets/blue_person.png'
ACCELERATION : float = 0.5
MAX_PLATFORMS : int = 2
MOVEMENT_SPEED : float = 3

class Player(Entity):
    # Attributes
    _airborne : bool = True
    _jump_timer : int = 0
    _jump_window : int = 0
    _platforms_queue : list[Platform] = []
    _platforms: pygame.sprite.Group = pygame.sprite.Group()

    # Magic Methods
    def __init__(self, pos : (int, int)):
        super().__init__(sprite_path=SPRITE_PATH, pos=pos, width=BLUE_WIDTH, height=BLUE_HEIGHT)

    # Accessors/Setters
    @property
    def platforms(self) -> pygame.sprite.Group:
        return self._platforms

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
        self._jump_timer = JUMP_TIMER
        self._jump_window = JUMP_WINDOW

    def _no_jump(self):
        self._jump_timer = -1
        self._airborne = True

    def _vertical_move(self, jumping : bool):
        self._accelerate_by_gravity()

        if jumping:
            self._jump()
            self.rect.y -= 1

        if not self._airborne:
            self._is_grounded()
        elif self._jump_window > 0:
            self._jump_window -= 1
        else:
            self._no_jump()
        self.rect.y += self._vel_y

    def _horizontal_move(self, moving_left : bool, moving_right : bool):
        if moving_left:
            self._vel_x = max(-MOVEMENT_SPEED, self._vel_x - ACCELERATION)
        else:
            self._vel_x = max(0.0, self._vel_x)
        if moving_right:
            self._vel_x = min(MOVEMENT_SPEED, self._vel_x + ACCELERATION)
        else:
            self._vel_x = min(0.0, self._vel_x)
        self.rect.x += self._vel_x

    # Public Methods
    def move(self, pressed_keys : pygame.key.ScancodeWrapper):
        """
        Wrapper for movement logic for the Player
        :param pressed_keys: pygame.key.ScancodeWrapper
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
        if self.rect.bottom > SCREEN_HEIGHT:
            self._is_grounded()
            self.rect.bottom = SCREEN_HEIGHT
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        # TODO: define when a Player is colliding with a Block
        for block in blocks:
            pass

    def add_platform(self, pos : (int, int)):
        """
        Creates a new Platform at the given position (pos), and deletes the oldest Platform if there are too many
        :param pos: (int, int)
        """
        new_platform : Platform = Platform(pos=pos)
        if len(self._platforms_queue) == MAX_PLATFORMS:
            self._platforms.remove(self._platforms_queue[0])
            self._platforms_queue.pop(0)
        self._platforms.add(new_platform)
        self._platforms_queue.append(new_platform)
