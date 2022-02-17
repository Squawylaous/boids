import pygame
from pygame.locals import *
from pygame.math import Vector2 as vector
from random import random

pygame.init()

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 25)
background = Color(161, 161, 161)
foreground = Color(255, 255, 255)
screen = pygame.display.set_mode((0, 0), FULLSCREEN)
screen_rect = screen.get_rect()

update_rects = []
fps = 0

class boid:
  size = 5
  
  def __init__(self, pos=None):
    if pos is None:
      pos = random()*screen_rect.w, random()*screen_rect.h
    self.pos = vector(pos)
    self.velocity = (vector(random(), random())-(0.5, 0.5))*10
    self.prevPos, self.prevVelocity = vector(), vector()
  
  def __str__(self):
    return str(self.pos)+", "+str(self.velocity)
  
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
  
  @property
  def rect(self):
    Rect = pygame.rect.Rect(self.pos, vector(boid.size, boid.size)*2)
    Rect.center = self.pos-Rect.size
    return Rect
  
  def move(self):
    self.prevPos, self.prevVelocity = vector(self.pos), vector(self.velocity)
    self.pos += self.velocity
  
  def draw(self, color):
    pygame.draw.circle(screen, color, self.intPos, boid.size)
    update_rects.append(self.rect)

def intVector(v):
  return int(v.x), int(v.y)

boid1 = boid()
print(boid1)
print(boid1.rect)

screen.fill(background)
pygame.display.flip()

while True:
  clock.tick(30)
  fps = str(round(clock.get_fps()))
  update_rects = []
  if pygame.event.get(QUIT):
    break
  for event in pygame.event.get():
    if event.type == KEYDOWN:
      if event.key == K_ESCAPE:
        pygame.event.post(pygame.event.Event(QUIT))
  
  screen.fill(background)
  boid1.move()
  boid1.draw(foreground)
  screen.blit(font.render(fps, 0, foreground), (0,0))
  update_rects.append(pygame.rect.Rect((0,0), font.size(fps)))
  pygame.display.update(update_rects)
pygame.quit()
