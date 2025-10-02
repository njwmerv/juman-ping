import pygame
from utility.game_constants import GOAL_WIDTH, GOAL_HEIGHT
from game_objects.blocks.block import Block

class Goal(Block):
    def __init__(self, pos: tuple[int, int], image : pygame.Surface):
        super().__init__(pos=pos, width=GOAL_WIDTH, height=GOAL_HEIGHT, top=True, bot=True, left=True, right=True, image=image)

    def get_box(self) -> tuple[int]:
        return self.rect.top, self.rect.bot, self.rect.left, self.rect.bottom