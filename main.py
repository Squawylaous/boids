import pygame
from pygame.locals import *
from pygame.math import Vector2 as vector
from random import random

pygame.init()

background = Color(0, 0, 0)
foreground = Color(255, 255, 255)
screen = pygame.display.set_mode((0, 0), FULLSCREEN)
screen_rect = screen.get_rect()
screen.fill(background)

class boid:
  def __init__(self, pos=None):
    if pos is None:
      pos = random()*screen_rect.w, random()*screen_rect.h
    self.pos = vector(pos)
    self.velocity = vector(random(), random())*20-10
  
  def __str__(self):
    return "("+str(self.pos)+", "+str(self.velocity)+")"
  
  @property
  def x(self):
    return self.pos.x
  
  @x.setter
  def x(self, value):
    self.pos.x = value
  
  @property
  def y(self):
    return self.pos.y
  
  @y.setter
  def y(self, value):
    self.pos.y = value
  
  @property
  def intPos(self):
    return int(self.x), int(self.y)
  
  def draw(self, color):
    pygame.draw.circle(screen, color, self.intPos, 5)

def intVector(v):
  return int(v.x), int(v.y)

boid1 = boid()
print(boid1)

while True:
  if pygame.event.get(QUIT):
    break
  for event in pygame.event.get():
    if event.type == KEYDOWN:
      if event.key == K_ESCAPE:
        pygame.event.post(pygame.event.Event(QUIT))
  
  screen.fill(background)
  boid1.draw(foreground)
  pygame.display.flip()
pygame.quit()
