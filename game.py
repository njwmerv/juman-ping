import pygame # type: ignore
import game_constants as const
from sys import exit

pygame.init()

screen = pygame.display.set_mode((const.WINDOW_WIDTH, const.WINDOW_HEIGHT))
pygame.display.set_caption('Juman Ping')

clock = pygame.time.Clock()

test_surface = pygame.Surface((100, 200))
test_surface.fill('Red')

image_surface = pygame.image.load('juman-ping/Assets/blue_person.png')

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()

  screen.blit(test_surface, (0, 0))

  screen.blit(image_surface, (150, 0))

  pygame.display.update()
  clock.tick(60)