import pygame
from block import Block
from entity import Entity
from platform import Platform
from game_constants import FPS, CELL_SIZE, GRAVITY_ACC, MAX_GRAVITY_VEL, SCREEN_WIDTH, SCREEN_HEIGHT

# Player Constants
BLUE_WIDTH : int = 2 * CELL_SIZE
JUMP_SPEED : float = -6
JUMP_TIMER : int = 7
BLUE_HEIGHT : int = 3 * CELL_SIZE
JUMP_WINDOW : int = round(FPS / 2)
SPRITE_PATH : str = './Assets/blue_person.png'
ACCELERATION : float = 30
MAX_PLATFORMS : int = 2
MOVEMENT_SPEED : float = 4.5

class Player(Entity):
    # Attributes
    _grounded : bool = False
    _jump_timer : int = 0
    _platforms_queue : list[Platform] = []
    _falling_platforms : list[Platform] = []
    _platforms: pygame.sprite.Group = pygame.sprite.Group()

    # Magic Methods
    def __init__(self, pos : (int, int)):
        super().__init__(sprite_path=SPRITE_PATH, pos=pos, width=BLUE_WIDTH, height=BLUE_HEIGHT)

    # Accessors/Setters
    @property
    def platforms(self) -> pygame.sprite.Group:
        return self._platforms

    # Private Methods
    def _accelerate_by_gravity(self, dt : float):
        if not self._grounded:
            new_vel_y : float = self._vel_y + (GRAVITY_ACC * dt)
            self._vel_y = min(new_vel_y, MAX_GRAVITY_VEL)

    def _jump(self):
        if self._jump_timer >= 0 and self._grounded:
            self._vel_y = JUMP_SPEED
            self._jump_timer -= 1
            self._grounded = False

    def _is_grounded(self, blocks : list[Block]) -> bool:
        for block in blocks:
            if block.rect.top <= self.rect.bottom <= block.rect.bottom:
                self._be_grounded()
                return True
        return False

    def _be_grounded(self):
        """
        Modifies a Player object to be grounded, i.e. can jump again
        """
        self._grounded = True
        self._vel_y = 0
        self._jump_timer = JUMP_TIMER

    def _vertical_move(self, jumping : bool, dt : float):
        self._accelerate_by_gravity(dt)
        if jumping: self._jump()
        self.rect.y += self._vel_y * dt * FPS

    def _horizontal_move(self, moving_left : bool, moving_right : bool, dt : float):
        if moving_left:
            self._vel_x = max(-MOVEMENT_SPEED, self._vel_x - ACCELERATION * dt)
        else:
            self._vel_x = max(0.0, self._vel_x)
        if moving_right:
            self._vel_x = min(MOVEMENT_SPEED, self._vel_x + ACCELERATION * dt)
        else:
            self._vel_x = min(0.0, self._vel_x)
        self.rect.x += self._vel_x * dt * FPS

    def _can_passthrough(self, block : Block) -> bool:
        if self._vel_x > 0 and block.passthrough.get("left", False):
            return True
        elif self._vel_x < 0 and block.passthrough.get("right", False):
            return True
        elif self._vel_y > 0 and block.passthrough.get("top", False):
            return True
        elif self._vel_y < 0 and block.passthrough.get("bot", False):
            return True
        return False

    def _horizontal_block_collision(self, block : Block):
        if (self.rect.bottom - 1) <= block.rect.top or self.rect.top - 1 >= block.rect.bottom: return
        if self.rect.right > block.rect.left > self.rect.right - BLUE_WIDTH // 4:
            self.rect.right = block.rect.left
            self._vel_x *= -1
        if self.rect.left < block.rect.right < self.rect.left + BLUE_WIDTH // 4:
            self.rect.left = block.rect.right
            self._vel_x *= -1

    def _horizontal_collisions(self, blocks : list[Block]):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        for block in blocks:
            if not self._can_passthrough(block): self._horizontal_block_collision(block)

    def _vertical_block_collisions(self, block : Block):
        if self.rect.right <= block.rect.left or self.rect.left >= block.rect.right: return
        if self.rect.bottom > block.rect.top > self.rect.bottom - CELL_SIZE:
            self._be_grounded()
            self.rect.bottom = block.rect.top + 1
        if self.rect.top < block.rect.bottom < self.rect.top + CELL_SIZE:
            self.rect.top = block.rect.bottom
            self._vel_y *= 0.1

    def _vertical_collisions(self, blocks : list[Block]):
        self._grounded = self._is_grounded(blocks)
        if self.rect.bottom >= SCREEN_HEIGHT:
            self._be_grounded()
            self.rect.bottom = SCREEN_HEIGHT

        # Terrain
        for block in blocks:
            if not self._can_passthrough(block): self._vertical_block_collisions(block)

        # Platform Collisions
        for platform in self._platforms_queue:
            if self.rect.colliderect(platform.rect) and not self._can_passthrough(platform) and platform.rect.top <= self.rect.bottom <= platform.rect.bottom:
                self._be_grounded()
                self._vertical_block_collisions(platform)
                platform.collide()
                self._falling_platforms.append(platform)
                self._platforms_queue.remove(platform)
        for platform in self._falling_platforms:
            if self.rect.colliderect(platform.rect) and not self._can_passthrough(platform) and platform.rect.top <= self.rect.bottom <= platform.rect.bottom:
                self._be_grounded()
                self._vertical_block_collisions(platform)

    # Public Methods
    def move(self, pressed_keys : pygame.key.ScancodeWrapper, near_blocks : list[Block], dt : float):
        """
        Wrapper for movement logic for the Player
        :param pressed_keys: pygame.key.ScancodeWrapper
        :param near_blocks: list[Block]
        :param dt: float
        """
        moving_left : bool = pressed_keys[pygame.K_a] or pressed_keys[pygame.K_LEFT]
        moving_right : bool = pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]
        self._horizontal_move(moving_left, moving_right, dt)
        self._horizontal_collisions(near_blocks)

        jumping : bool = pressed_keys[pygame.K_SPACE] or pressed_keys[pygame.K_w] or pressed_keys[pygame.K_UP]
        self._vertical_move(jumping, dt)
        self._vertical_collisions(near_blocks)

        for platform in self._falling_platforms:
            platform.move(dt)
            if platform.rect.top >= SCREEN_HEIGHT:
                self._falling_platforms.remove(platform)
                self._platforms.remove(platform)

    def add_platform(self, pos : (int, int)):
        """
        Creates a new Platform at the given position (pos), and deletes the oldest Platform if there are too many
        :param pos: (int, int)
        """
        new_platform : Platform = Platform(pos=pos)
        while len(self._platforms_queue) >= MAX_PLATFORMS:
            self._platforms.remove(self._platforms_queue[0])
            self._platforms_queue.pop(0)
        self._platforms.add(new_platform)
        self._platforms_queue.append(new_platform)
