import pygame
from enum import Enum
from utility.image_loader import ImageLoader
from utility.game_constants import FPS, NAME, SCREEN_WIDTH, SCREEN_HEIGHT
from game_objects.other.level import Level
from game_objects.entities.player import Player

# Constants
LEVEL_DATA_BASE_PATH : str = "./assets/levels/"

# Helper
def get_level_data(level : str) -> str:
    return f"./assets/levels/{level}.json"

class GameState(Enum):
    PLAY = 0
    WIN = 1
    QUIT = 2

class Game:
    window : pygame.Surface
    clock : pygame.time.Clock
    assets : ImageLoader
    level : Level
    player : Player

    def __init__(self):
        # PyGame Setup
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        pygame.display.init()
        self.window : pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(NAME)
        self.clock = pygame.time.Clock()

        # Load images
        self.assets = ImageLoader()

        self.level = Level(level_data=get_level_data("test"), assets=self.assets)

        self.player = Player(pos=self.level.start_pos, assets=self.assets)

    def run(self) -> GameState:
        delta_time: float = self.clock.tick(FPS) / 1000.0

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return GameState.QUIT
            self.player.handle_input(event)

        self.player.move(dt=delta_time, blocks=self.level.find_near_blocks(self.player))  # Movement

        # Check win?

        # Drawing Everything
        self.level.draw(self.window)
        self.player.draw(self.window)

        pygame.display.update()
        return GameState.PLAY

    def __del__(self):
        pygame.quit()