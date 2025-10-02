import pygame
from enum import Enum
from utility.image_loader import ImageLoader
from utility.game_constants import FPS, NAME, SCREEN_WIDTH, SCREEN_HEIGHT
from game_objects.other.level import Level
from game_objects.entities.player import Player
from game_objects.blocks.block_factory import BlockFactory

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
    factory : BlockFactory
    level : Level
    player : Player
    font : pygame.font

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

        self.factory : BlockFactory = BlockFactory(self.assets)

        self.level = Level(level_data=get_level_data("test"), assets=self.assets, factory=self.factory)

        self.player = Player(pos=self.level.start_pos, assets=self.assets)

        self.font = pygame.font.SysFont("arial", 30)

    def run(self, state : GameState) -> GameState:
        match state:
            case GameState.WIN: state = self._handle_win()
            case GameState.PLAY: state = self._handle_game()
        pygame.display.update()
        return state

    def __del__(self):
        pygame.quit()

    # Private Methods

    def _handle_game(self) -> GameState:
        next_state : GameState = GameState.PLAY
        delta_time : float = self.clock.tick(FPS) / 1000.0

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return GameState.QUIT
            self.player.handle_input(event)

        self.player.move(dt=delta_time, blocks=self.level.find_near_blocks(self.player))  # Movement

        # Check win?
        if self.player.rect.colliderect(self.level.get_goal()):
            self._handle_win()
            next_state = GameState.WIN

        # Drawing Everything
        self.level.draw(self.window)
        self.player.draw(self.window)

        return next_state

    def _handle_win(self) -> GameState:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return GameState.QUIT

        win_text = self.font.render(f"You win!", 1, (0, 0, 0))
        self.window.blit(win_text, ((SCREEN_WIDTH - win_text.get_width()) // 2, (SCREEN_HEIGHT - win_text.get_height()) // 2))
        return GameState.PLAY