import json
import pygame
from block import Block
from player import Player
from game_constants import NAME, CELL_SIZE

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

# Helpers
def generate_block(kind : int, x : int, y : int, width : int, height : int) -> Block | None:
    pos : (int, int) = (x * CELL_SIZE, y * CELL_SIZE)
    width *= CELL_SIZE
    height *= CELL_SIZE
    match kind:
        case 0: # Empty
            return None
        case 1: # Default Block
            return Block(sprite_path="./Assets/platform.png", pos=pos, width=width, height=height)

class Level:
    # Attributes
    _terrain : list[Block]
    _terrain_group : pygame.sprite.Group = pygame.sprite.Group()
    _start_pos : (int, int)

    # Magic Methods
    def __init__(self, level_data : str):
        self._terrain = []
        file = open(level_data)
        data = json.load(file)
        pygame.display.set_caption(f"{NAME} - {data[name_key]}")
        self._start_pos = data[start_pos_key]

        for block_data in data[terrain_key]:
            new_block : Block = generate_block(x=block_data[X_KEY], y=block_data[Y_KEY], kind=block_data[KIND_KEY], width=block_data[WIDTH_KEY], height=block_data[HEIGHT_KEY])
            if new_block is not None:
                self._terrain.append(new_block)
                self._terrain_group.add(new_block)

    # Accessors/Setters
    @property
    def terrain(self) -> list[Block]:
        return self._terrain

    @property
    def start_pos(self) -> (int, int):
        return self._start_pos

    # Methods
    def draw(self, surface : pygame.Surface):
        self._terrain_group.draw(surface)

    def find_near_blocks(self, player : Player) -> list[Block]:
        """
        Finds nearest Blocks (terrain) to a Player.
        :param player: Player
        :return list[Block]
        """
        nearest_blocks : list[Block] = []
        for block in self._terrain:
            if player.rect.colliderect(block.rect): nearest_blocks.append(block)
        return nearest_blocks