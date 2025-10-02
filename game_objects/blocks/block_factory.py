from utility.image_loader import ImageLoader
from utility.game_constants import CELL_SIZE
from game_objects.blocks.goal import Goal
from game_objects.blocks.block import Block

# Block Types
EMPTY : int = 0
REGULAR_BLOCK : int = 1
GOAL_BLOCK : int = 2

class BlockFactory:
    _assets : ImageLoader

    def __init__(self, assets: ImageLoader):
        self._assets = assets

    def generate_block(self, kind: int, x: int, y: int, width: int = 0, height: int = 0) -> Block | None:
        pos: (int, int) = (x * CELL_SIZE, y * CELL_SIZE)
        width *= CELL_SIZE
        height *= CELL_SIZE
        match kind:
            case 0:  # Empty
                return None
            case 1:  # Default Block
                return Block(image=self._assets.get_image("blocks", "platform.png"), pos=pos, width=width, height=height)
            case 2:  # Goal
                return Goal(pos=pos, image=self._assets.get_image("blocks", "goal_flag.png"))