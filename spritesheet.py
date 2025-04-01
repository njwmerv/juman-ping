import pygame

class SpriteSheet:
	_sheet : pygame.image

	def __init__(self, image : pygame.image = None, image_path : str = ""):
		if image is None and image_path == "": raise ValueError("SpriteSheet: At least one of sprite_path or image must be provided")
		if image is not None: self._sheet = image
		else: self._sheet = pygame.image.load(image_path).convert_alpha()


	def get_frame(self, frame : int, width : int, height : int, scale : tuple[int, int], colour : tuple[int, int, int],
				  gap : int, x_offset : int = 0, y_offset : int = 0) -> pygame.Surface:
		image = pygame.Surface((width, height)).convert_alpha()
		image.blit(self._sheet, (0, 0), ((frame * gap) + x_offset, y_offset, width, height))
		image = pygame.transform.scale(image, size=scale)
		image.set_colorkey(colour)
		return image
