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
        clock.tick(FPS)
        pressed_keys = pygame.key.get_pressed()

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]: BLUE.add_platform(pygame.mouse.get_pos())
                elif pygame.mouse.get_pressed()[2]:
                    BLUE.rect.x, BLUE.rect.y = pygame.mouse.get_pos()

        BLUE.move(pressed_keys, LEVEL.find_near_blocks(BLUE)) # Movement

        # Drawing Everything
        WIN.fill(WHITE)
        LEVEL.terrain_group.draw(WIN)
        BLUE.platforms.draw(WIN)
        PLAYER.draw(WIN)

        pygame.display.update()

pygame.quit()
