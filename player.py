import pygame
from block import Block
from entity import Entity
from platform import Platform
from game_constants import TERMINAL_VELOCITY, SCREEN_WIDTH, SCREEN_HEIGHT

# Size Constants
BLUE_WIDTH : int = 30 # px
BLUE_HEIGHT : int = 75 # px
# Movement Constants
MOVEMENT_SPEED : float = 300 # px/s
ACCELERATION : float = 1250 # px/s^2
DECELERATION : float = 1250 # px/s^2
AIRBORNE_MOVEMENT_FACTOR : float = 0.5
# Jump Constants
JUMP_STRENGTH : float = 600 # px/s
COYOTE_TIME : float = 0.1 # s
JUMP_BUFFER_TIME : float = 0.1 # s
# Platform Constants
MAX_PLATFORMS : int = 2

class Player(Entity):
    _on_ground : bool
    _jump_buffer_counter : float
    _coyote_time_counter : float
    _input_map : dict[pygame.key, bool]
    _platforms : list[Platform]
    _falling_platforms : list[Platform]
    _platform_group : pygame.sprite.Group = pygame.sprite.Group()

    # Public -----------------------------------------------------------------------------------------------------------

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos=pos, width=BLUE_WIDTH, height=BLUE_HEIGHT, sprite_path="./Assets/blue_person.png")
        self._jumping = False
        self._on_ground = False
        self._jump_buffer_counter = JUMP_BUFFER_TIME
        self._coyote_time_counter = COYOTE_TIME
        self._input_map = {
            pygame.K_SPACE: False, pygame.K_w: False, pygame.K_UP: False,
            pygame.K_a: False, pygame.K_LEFT: False,
            pygame.K_d: False, pygame.K_RIGHT: False
        }
        self._platforms = []
        self._falling_platforms = []
        self._platform_group = pygame.sprite.Group()

    def move(self, dt : float):
        """
        Wrapper for movement logic for the Player
        :param dt: float
        """
        # Update timers
        if not self._on_ground:
            self._coyote_time_counter -= dt
        else:
            self._coyote_time_counter = COYOTE_TIME

        if self._jump_buffer_counter > 0:
            self._jump_buffer_counter -= dt

        jumping : bool = self._input_map[pygame.K_SPACE] or self._input_map[pygame.K_w] or self._input_map[pygame.K_UP]
        moving_left : bool = self._input_map[pygame.K_a] or self._input_map[pygame.K_LEFT]
        moving_right : bool = self._input_map[pygame.K_d] or self._input_map[pygame.K_RIGHT]

        self._horizontal_movement(moving_left, moving_right, dt)
        self._vertical_movement(jumping, dt)

        self._handle_collisions([], dt)

    def handle_input(self, event : pygame.event):
        """
        Passes input into Player
        :param event: Event
        """
        if event.type == pygame.KEYDOWN:
            self._handle_keydown(event.key)
        elif event.type == pygame.KEYUP:
            self._handle_keyup(event.key)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mousedown(event)

    def add_platform(self, pos: tuple[int, int]):
        """
        Creates a platform
        :param pos: tuple[int, int]
        """
        if len(self._platforms) >= MAX_PLATFORMS:
            self._platform_group.remove(self._platforms[0])
            self._platforms = self._platforms[1:]
        self._platforms.append(Platform(pos=pos))
        self._platform_group.add(self._platforms[-1])

    def draw_platforms(self, window : pygame.Surface):
        """
        Draws the platforms of a Player
        :param window: pygame.Surface
        """
        self._platform_group.draw(window)

    # Private ----------------------------------------------------------------------------------------------------------

    def _handle_keydown(self, key : pygame.key):
        if key in self._input_map.keys(): self._input_map[key] = True
        if key == pygame.K_SPACE or key == pygame.K_w or key == pygame.K_UP:
            self._jump_buffer_counter = JUMP_BUFFER_TIME

    def _handle_keyup(self, key : pygame.key):
        if key in self._input_map.keys(): self._input_map[key] = False

    def _handle_mousedown(self, mouse):
        match mouse.button:
            case 1:
                self.add_platform(mouse.pos)

    def _horizontal_movement(self, left : bool, right : bool, dt : float):
        direction: int = 0
        if left: direction -= 1
        if right: direction += 1

        control_multiplier : float = 1 if self._on_ground else AIRBORNE_MOVEMENT_FACTOR

        if direction != 0:
            # Accelerate in direction of movement
            capped_vel_x = direction * MOVEMENT_SPEED
            acceleration : float = ACCELERATION * control_multiplier * dt

            if (direction > 0 and self._vel_x < capped_vel_x) or (direction < 0 and self._vel_x > capped_vel_x):
                self._vel_x += direction * acceleration
                # Cap velocity at maximum speed
                if direction > 0: self._vel_x = min(self._vel_x, capped_vel_x)
                else: self._vel_x = max(self._vel_x, capped_vel_x)
        else:
            # Decelerate when no direction input
            deceleration : float = DECELERATION * control_multiplier
            if self._vel_x > 0:
                self._vel_x -= deceleration * dt
                if self._vel_x < 0: self._vel_x = 0
            elif self._vel_x < 0:
                self._vel_x += deceleration * dt
                if self._vel_x > 0: self._vel_x = 0

    def _vertical_movement(self, jumping : bool, dt : float):
        if jumping: self._handle_jump()
        if not self._on_ground: self._accelerate_by_gravity(dt)
        if self._vel_y > TERMINAL_VELOCITY: self._vel_y = TERMINAL_VELOCITY

    def _handle_jump(self):
        if self._jump_buffer_counter > 0 and (self._on_ground or self._coyote_time_counter > 0):
            self._vel_y = -JUMP_STRENGTH
            self._on_ground = False
            self._jump_buffer_counter = 0

    def _handle_collisions(self, blocks : list[Block], dt : float):
        # Future movement
        dx : float = self._vel_x * dt
        dy : float = self._vel_y * dt

        self.rect.x += dx
        for block in blocks:
            if self.rect.colliderect(block.rect) and self._can_passthrough_horizontal(block):
                self._vel_x = 0
                if dx > 0: self.rect.right = block.rect.left
                elif dx < 0: self.rect.left = block.rect.right
        if self.rect.right > SCREEN_WIDTH:
            self._vel_x = 0
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self._vel_x = 0
            self.rect.left = 0

        self.rect.y += dy
        self._on_ground = False
        for block in blocks:
            if self.rect.colliderect(block.rect) and self._can_passthrough_vertical(block):
                self._vel_y = 0
                if dy > 0:
                    self.rect.bottom = block.rect.top
                    self._on_ground = True
                elif dy < 0:
                    self.rect.top = block.rect.bottom
        if self.rect.bottom > SCREEN_HEIGHT:
            self._vel_y = 0
            self.rect.bottom = SCREEN_HEIGHT
            self._on_ground = True

    def _can_passthrough_horizontal(self, block : Block) -> bool:
        passthrough : dict[str, bool] = block.passthrough
        if self._vel_x > 0 and passthrough["left"]: return True
        if self._vel_x < 0 and passthrough["right"]: return True
        return False

    def _can_passthrough_vertical(self, block : Block) -> bool:
        passthrough : dict[str, bool] = block.passthrough
        if self._vel_y > 0 and passthrough["top"]: return True
        if self._vel_y < 0 and passthrough["bot"]: return True
        return False
