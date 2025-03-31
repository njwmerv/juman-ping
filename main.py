import pygame
from level import Level
from player import Player
from game_constants import FPS, NAME, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE

# PyGame Setup
pygame.font.init()
pygame.mixer.init()

# WINDOW / SCREEN CONSTANTS
WIN : pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(NAME)

# FONTS
DEBUG_FONT = pygame.font.SysFont("arial", 30)

if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()

    # Entities
    LEVEL : Level = Level('./Assets/levels/test.json')
    BLUE : Player = Player(pos=LEVEL.start_pos)
    PLAYER : pygame.sprite.GroupSingle = pygame.sprite.GroupSingle(BLUE)

    running = True
    while running:
        delta_time : float = clock.tick(FPS) / 1000.0
        pressed_keys = pygame.key.get_pressed()

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                break
            BLUE.handle_input(event)

        BLUE.move(pressed_keys, LEVEL.find_near_blocks(BLUE), delta_time) # Movement

        # Drawing Everything
        WIN.fill(WHITE)
        LEVEL.terrain_group.draw(WIN)
        BLUE.draw_platforms(WIN)
        PLAYER.draw(WIN)

        pygame.display.update()

pygame.quit()
