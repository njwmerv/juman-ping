import json
import pygame
from block import Block
from player import Player
from game_constants import NAME, CELL_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT

# Constants
name_key : str = 'level_name'
terrain_key : str = 'terrain'
start_pos_key : str = 'start_pos'

# Helpers
def generate_block(kind : int, x : int, y : int) -> Block | None:
    pos : (int, int) = (x * CELL_SIZE, y * CELL_SIZE)
    match kind:
        case 0: # Empty
            return None
        case 1: # Default Block
            return Block(sprite_path="./Assets/goal_flag.png", pos=pos, width=CELL_SIZE, height=CELL_SIZE)

class Level:
    # Attributes
    _terrain : list[list[Block]]
    _terrain_group : pygame.sprite.Group = pygame.sprite.Group()
    _start_pos : (int, int)

    # Magic Methods
    def __init__(self, level_data : str):
        self._terrain = []
        file = open(level_data)
        data = json.load(file)
        pygame.display.set_caption(f"{NAME} - {data[name_key]}")
        self._start_pos = data[start_pos_key]
        for row in range(len(data[terrain_key])):
            new_row : list[Block] = []
            for col in range(len(data[terrain_key][row])):
                new_block : Block = generate_block(kind=data[terrain_key][row][col], y=row, x=col)
                new_row.append(new_block)
                if new_block is not None:
                    self._terrain_group.add(new_block)
            self._terrain.append(new_row)

    # Accessors/Setters
    @property
    def terrain(self) -> list[list[Block]]:
        return self._terrain

    @property
    def terrain_group(self) -> pygame.sprite.Group:
        return self._terrain_group

    @property
    def start_pos(self) -> (int, int):
        return self._start_pos

    # Methods
    def find_near_blocks(self, player : Player) -> list[Block]:
        """
        Finds nearest Blocks (terrain) to a Player.
        :param player: Player
        :return list[Block]
        """
        # Find Possible Collisions
        top : int = round(player.rect.top) // CELL_SIZE
        bot : int = min(round(player.rect.bottom) // CELL_SIZE, SCREEN_HEIGHT // CELL_SIZE - 1)
        left : int = round(player.rect.left) // CELL_SIZE
        right : int = min(round(player.rect.right) // CELL_SIZE, SCREEN_WIDTH // CELL_SIZE - 1)
        nearest_blocks : list[Block] = []
        for row in range(top, bot + 1):
            for col in range(left, right + 1):
                if self._terrain[row][col] is not None:
                    nearest_blocks.append(self._terrain[row][col])
        return nearest_blocks