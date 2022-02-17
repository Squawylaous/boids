import pygame
from pygame.locals import *
from pygame.math import Vector2 as vector

pygame.init()

background = Color(0, 0, 0)
screen = pygame.display.set_mode((0, 0), FULLSCREEN)
screen_rect = screen.get_rect()
screen.fill(background)

while True:
    if pygame.event.get(QUIT):
        break
    for event in pygame.event.get():
        if event.type == KEYDOWN:
          if event.key == K_ESCAPE:
              pygame.event.post(pygame.event.Event(QUIT))

    screen.fill(background)
    pygame.display.flip()
pygame.quit()
