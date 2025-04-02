import os
import pygame

def load_image(path : str) -> pygame.Surface:
    """
    Given a path to a file, loads it into Pygame
    :param path:
    :return: pygame.Surface
    """
    img : pygame.Surface = pygame.image.load(path).convert_alpha()
    return img

def load_images(path) -> dict[str, pygame.Surface]:
    """
    Given a path, loads all files as images and returns them.
    :param path: str
    :return: list[pygame.Surface]
    """
    images : dict[str, pygame.Surface] = {}
    for img_name in os.listdir(path):
        images[img_name] = load_image(f"{path}/{img_name}")
    return images

# Constants
ASSET_SUB_DIRECTORIES : list[str] = ["backgrounds", "blocks", "entities"]

class ImageLoader:
    _catalog : dict[str, dict[str, pygame.Surface]]

    def __init__(self):
        self._catalog = {}
        for sub_dir in ASSET_SUB_DIRECTORIES:
            self._catalog[sub_dir] = load_images(f"./Assets/{sub_dir}")

    def get_image(self, category : str, name : str) -> pygame.Surface | None:
        if category not in ASSET_SUB_DIRECTORIES: return None
        return self._catalog[category].get(name, None)