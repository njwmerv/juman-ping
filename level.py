import json
import pygame
from block import Block
from player import Player
from image_loader import ImageLoader
from game_constants import NAME, CELL_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT

# Constants
name_key : str = 'level_name'
terrain_key : str = 'terrain'
start_pos_key : str = 'start_pos'
# Block Constants
X_KEY : str = "x"
Y_KEY : str = "y"
KIND_KEY : str = "kind"
WIDTH_KEY : str = "width"
HEIGHT_KEY : str = "height"
BACKGROUND_KEY : str = "background"

# Helpers
def generate_block(kind : int, x : int, y : int, width : int, height : int, assets : ImageLoader) -> Block | None:
    pos : (int, int) = (x * CELL_SIZE, y * CELL_SIZE)
    width *= CELL_SIZE
    height *= CELL_SIZE
    match kind:
        case 0: # Empty
            return None
        case 1: # Default Block
            return Block(image=assets.get_image("blocks", "platform.png"), pos=pos, width=width, height=height)

class Level:
    # Attributes
    _terrain : list[Block]
    _terrain_group : pygame.sprite.Group = pygame.sprite.Group()
    _start_pos : (int, int)
    _background : pygame.Surface

    # Magic Methods
    def __init__(self, level_data : str, assets : ImageLoader):
        self._terrain = []
        file = open(level_data)
        data = json.load(file)
        pygame.display.set_caption(f"{NAME} - {data[name_key]}")
        self._start_pos = data[start_pos_key]

        for block_data in data[terrain_key]:
            new_block : Block = generate_block(x=block_data[X_KEY], y=block_data[Y_KEY], kind=block_data[KIND_KEY], width=block_data[WIDTH_KEY], height=block_data[HEIGHT_KEY], assets=assets)
            if new_block is not None:
                self._terrain.append(new_block)
                self._terrain_group.add(new_block)
        self._background = pygame.transform.scale(assets.get_image("backgrounds", data[BACKGROUND_KEY]), size=(SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()

    # Accessors/Setters
    @property
    def terrain(self) -> list[Block]:
        return self._terrain

    @property
    def start_pos(self) -> (int, int):
        return self._start_pos

    # Methods
    def draw(self, surface : pygame.Surface):
        surface.blit(self._background, (0, 0))
        self._terrain_group.draw(surface)

    def find_near_blocks(self, player : Player) -> list[Block]:
        """
        Finds nearest Blocks (terrain) to a Player.
        :param player: Player
        :return list[Block]
        """
        # TEMPORARY
        return self._terrain
        # nearest_blocks : list[Block] = []
        # for block in self._terrain:
        #     nearest_blocks.append(block)
        # return nearest_blocks
