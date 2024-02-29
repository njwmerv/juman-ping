import pygame
import os

pygame.font.init()
pygame.mixer.init()

# WINDOW / SCREEN CONSTANTS
WIDTH, HEIGHT = 1500, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juman Ping")
FPS = 60

# COLOURS
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0,0,0)

# FONTS
DEBUG_FONT = pygame.font.SysFont("arial", 30)
INTRO_FONT = pygame.font.SysFont("comic sans", 60)

# USER EVENTS

# PHYSICS CONSTANTS
MAX_GRAVITY_VEL = 50
GRAVITY_ACC = 10
JUMP_SPEED = -7.5

# Player Constants
BLUE_WIDTH, BLUE_HEIGHT = 10, 25
BLUE_VEL = 3
BLUE_JUMP_TIMER = 6
BLUE_JUMP_SPEED = -6
BLUE_JUMP_WINDOW = 30

# Platform Constants
PLATFORM_WIDTH, PLATFORM_HEIGHT = 30, 10
MAX_PLATFORMS = 1

# Goal Constants
GOAL_WIDTH, GOAL_HEIGHT = 50, 50

# Images
BLUE_PERSON = pygame.transform.scale(pygame.image.load(os.path.join("Assets","blue_person.png")), (BLUE_WIDTH, BLUE_HEIGHT))
PLATFORM = pygame.transform.scale(pygame.image.load(os.path.join("Assets","platform.png")), (PLATFORM_WIDTH, PLATFORM_HEIGHT))
FALLING_PLATFORM = pygame.transform.scale(pygame.image.load(os.path.join("Assets","falling_platform.png")), (PLATFORM_WIDTH, PLATFORM_HEIGHT))
GOAL = pygame.transform.scale(pygame.image.load(os.path.join("Assets","goal_flag.png")), (GOAL_WIDTH,GOAL_HEIGHT))

##################################################################################################################################
def vertical_movement(player, platforms, falling_platforms):
    for platform in falling_platforms:
        platform.y_vel = platform.accelerate_by_gravity()
        platform.y += platform.y_vel
        if platform.y >= HEIGHT:
            falling_platforms.remove(platform)
    
    if player.on_ground_check():
        player.y = HEIGHT - BLUE_HEIGHT
        player.y_vel = 0
    elif not player.on_any_platforms_check(platforms, falling_platforms):
        player.y_vel = player.accelerate_by_gravity()
        player.y += player.y_vel
    else:
        player.y_vel = 0
        for platform in falling_platforms:
            if player.on_platform_check(platform): player.y = platform.y - player.height + 1

##################################################################################################################################
class Object:
    x = 0
    y = 0
    y_vel = 0
    width = 0
    height = 0
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def accelerate_by_gravity(self) -> int:
        return min(self.y_vel + GRAVITY_ACC/FPS, MAX_GRAVITY_VEL)

class Player(Object):
    y_vel = 0
    vel = BLUE_VEL
    width = BLUE_WIDTH
    height = BLUE_HEIGHT
    jump_timer = BLUE_JUMP_TIMER
    jump_window = BLUE_JUMP_WINDOW
    jumped = False

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def move_player(self, pressed_keys):
        if pressed_keys[pygame.K_a] and self.x > 0:
            self.x -= self.vel
        elif pressed_keys[pygame.K_a] and self.x <= 0:
            self.x = 0
        if pressed_keys[pygame.K_d] and self.x + self.width < WIDTH:
            self.x += self.vel
        elif pressed_keys[pygame.K_d] and self.x + self.width >= WIDTH:
            self.x = WIDTH - self.width

    def reset_jump(self):
        self.jump_timer = BLUE_JUMP_TIMER
        self.jumped = False
        self.jump_window = BLUE_JUMP_WINDOW
    def no_jump(self):
        self.jump_timer = -1
        self.jumped = True

    def on_ground_check(self) -> bool:
        if self.y + self.height >= HEIGHT:
            return True
        return False
    
    def jump(self, pressed_keys):
        if (pressed_keys[pygame.K_w] or pressed_keys[pygame.K_SPACE]) and self.jump_timer >= 0 and not self.jumped:
            self.y_vel = 0
            self.y_vel += BLUE_JUMP_SPEED
            self.jump_timer -= 1

    def on_platform_check(self, platform) -> bool:
        if platform.y <= self.y + self.height <= platform.y + platform.height and self.y_vel >= 0:
            if platform.x <= self.x <= self.x + self.width <= platform.x + platform.width:
                return True
            elif self.x <= platform.x <= self.x + self.width:
                return True
            elif self.x <= platform.x + platform.width <= self.x + self.width:
                return True
        return False

    def on_any_platforms_check(self, platforms, falling_platforms) -> bool:
        for platform in platforms:
            if self.on_platform_check(platform): return True
        for f_platform in falling_platforms:
            if self.on_platform_check(f_platform): return True
        return False

    def platform_break(self, platforms, falling_platforms):
        for platform in platforms:
            if self.on_platform_check(platform):
                falling_platforms.append(platform)
                platforms.remove(platform)

    #def in_goal_check(self, goal) -> bool:


class Platform(Object):
    width = PLATFORM_WIDTH
    height = PLATFORM_HEIGHT

class Goal(Object):
    width = GOAL_WIDTH
    height = GOAL_HEIGHT

class GameState:
    platforms = []
    falling_platforms = []
    goal = Goal(WIDTH, HEIGHT)

    def __init__(self):
        self.state = 0

    def draw_window(self, blue):
        WIN.fill(BLACK)
        WIN.blit(GOAL, (self.goal.x, self.goal.y))
        WIN.blit(BLUE_PERSON, (blue.x, blue.y))

        for platform in self.platforms:
            WIN.blit(PLATFORM, (platform.x, platform.y))
        for platform in self.falling_platforms:
            if platform.y + platform.y_vel < HEIGHT:
                WIN.blit(FALLING_PLATFORM, (platform.x, platform.y))
            else:
                self.falling_platforms.remove(platform)

        pygame.display.update()

    def intro(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.platforms = []
                self.falling_platforms = []
                self.goal = Goal(WIDTH-GOAL_WIDTH, HEIGHT-GOAL_HEIGHT)
                self.state += 1
        
        ready_text = INTRO_FONT.render("Click to Play", 1, WHITE)
        WIN.blit(ready_text, ((WIDTH - ready_text.get_width())//2, (HEIGHT - ready_text.get_height())//2))

        pygame.display.update()

    def level_one(self):
        pressed_keys = pygame.key.get_pressed()

        landed = BLUE.on_ground_check() or BLUE.on_any_platforms_check(self.platforms, self.falling_platforms)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                  
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_w or event.key == pygame.K_SPACE) and landed and not BLUE.jumped:
                    BLUE.jumped = True
                    BLUE.y -= 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.platforms.append(Platform(mouse_x - PLATFORM_WIDTH//2, mouse_y - PLATFORM_HEIGHT//2))
                if len(self.platforms) > MAX_PLATFORMS:
                    for i in range(0, MAX_PLATFORMS):
                        self.platforms.remove(self.platforms[i])
            
        # Gravity
        vertical_movement(BLUE, self.platforms, self.falling_platforms)

        # Left-Right Movement
        BLUE.move_player(pressed_keys)
            
        # Jumping
        BLUE.jump(pressed_keys)
        if landed: 
            BLUE.reset_jump()
        elif BLUE.jump_window > 0:
            BLUE.jump_window -= 1
        else:
            BLUE.no_jump()

        # Platforms
        BLUE.platform_break(self.platforms, self.falling_platforms)

        self.draw_window(BLUE)

    def level_two():
        pressed_keys = pygame.key.get_pressed()

        landed = BLUE.on_ground_check() or BLUE.on_any_platforms_check(self.platforms, self.falling_platforms)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                  
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_w or event.key == pygame.K_SPACE) and landed and not BLUE.jumped:
                    BLUE.jumped = True
                    BLUE.y -= 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.platforms.append(Platform(mouse_x - PLATFORM_WIDTH//2, mouse_y - PLATFORM_HEIGHT//2))
                if len(self.platforms) > MAX_PLATFORMS:
                    for i in range(0, MAX_PLATFORMS):
                        self.platforms.remove(self.platforms[i])
            
        # Gravity
        vertical_movement(BLUE, self.platforms, self.falling_platforms)

        # Left-Right Movement
        BLUE.move_player(pressed_keys)
            
        # Jumping
        BLUE.jump(pressed_keys)
        if landed: 
            BLUE.reset_jump()
        elif BLUE.jump_window > 0:
            BLUE.jump_window -= 1
        else:
            BLUE.no_jump()

        # Platforms
        BLUE.platform_break(self.platforms, self.falling_platforms)

        self.draw_window(BLUE)

    def state_manager(self):
        if self.state == 0:
            self.intro()
        elif self.state == 1:
            self.level_one()
        #elif self.state == 2:
        #    self.level_two()

if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    game_state = GameState()

    BLUE = Player(0, HEIGHT - BLUE_HEIGHT, BLUE_WIDTH, BLUE_HEIGHT)

    while True:
        clock.tick(FPS)
        game_state.state_manager()