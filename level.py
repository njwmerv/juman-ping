import json
from abc import ABC
from block import Block
from player import Player
from game_constants import CELL_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT

def generate_block(kind : int, x : int, y : int) -> Block | None:
    match kind:
        case 0: # Empty
            return None
        case _: # Default Block
            return Block(x=(x * CELL_SIZE), y=(y * CELL_SIZE), width=CELL_SIZE, height=CELL_SIZE)

class Level(ABC):
    # Constants

    # Attributes
    _terrain : list[list[Block]]

    # Magic Methods
    def __init__(self, level_data : str):
        self._terrain = []
        file = open(level_data)
        data = json.load(file)
        for row in range(len(data['terrain'])):
            new_row : list[Block] = []
            for col in range(len(data['terrain'][row])):
                new_row.append(generate_block(data['terrain'][row][col], y=row, x=col))
            self._terrain.append(new_row)

    # Accessors/Setters
    @property
    def terrain(self) -> list[list[Block]]:
        return self._terrain

    # Methods
    def find_near_blocks(self, player : Player) -> list[Block]:
        """
        Finds nearest Blocks (terrain) to a Player.
        :param player: Player
        :return list[Block]
        """
        # Find Possible Collisions
        top : int = round(player.top) // CELL_SIZE
        bot : int = min(round(player.bot) // CELL_SIZE, SCREEN_HEIGHT // CELL_SIZE - 1)
        left : int = round(player.left) // CELL_SIZE
        right : int = min(round(player.right) // CELL_SIZE, SCREEN_WIDTH // CELL_SIZE - 1)
        nearest_blocks : list[Block] = []
        for row in range(top, bot + 1):
            for col in range(left, right + 1):
                if self._terrain[row][col] is not None:
                    nearest_blocks.append(self._terrain[row][col])
        return nearest_blocks