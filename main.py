import pygame
from block import Block
from player import Player
from game_constants import FPS, SCREEN_WIDTH, SCREEN_HEIGHT, BLUE_WIDTH, BLUE_HEIGHT, WHITE

pygame.font.init()
pygame.mixer.init()

# WINDOW / SCREEN CONSTANTS
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Juman Ping")

# FONTS
DEBUG_FONT = pygame.font.SysFont("arial", 30)

if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()

    # Entities
    BLUE = Player(x=0, y=0, width=BLUE_WIDTH, height=BLUE_HEIGHT, vel_y=0, sprite_path="./Assets/blue_person.png")
    GROUND = Block(x=0, y=(SCREEN_HEIGHT - 25), width=SCREEN_WIDTH, height=25, red=0, green=0, blue=0)

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
                BLUE.add_platform(pygame.mouse.get_pos())

        BLUE.move(pressed_keys) # Movement
        BLUE.check_collisions([GROUND] + [BLUE.platforms]) # Double check positions

        # Drawing Everything
        WIN.fill(WHITE)
        WIN.blit(GROUND.surface, GROUND.pos)
        for platform in BLUE.platforms:
            WIN.blit(platform.surface, platform.pos)
        WIN.blit(BLUE.surface, BLUE.pos)

            # Debug
        # ready_text = DEBUG_FONT.render(str(BLUE.vel())+ " " + str(BLUE._airborne) + " " + str(BLUE.pos()) + " " + str(BLUE._jump_timer >= 0 and not BLUE._airborne), 1, BLACK)
        # WIN.blit(ready_text, ((WIDTH - ready_text.get_width()) // 2, (HEIGHT - ready_text.get_height()) // 2))

        pygame.display.update()

pygame.quit()
