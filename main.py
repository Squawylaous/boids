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
  all = []
  prevTime, tickTime, currentTime = 0, 0, 0
  size = 5
  limit = pygame.rect.Rect((0, 0), vector(screen_rect.size)*0.75)
  limit.center = screen_rect.center
  speed_lim = 500.0
  
  def __init__(self, pos=None):
    if pos is None:
      pos = vector(random()*screen_rect.w, random()*screen_rect.h)*0.5 +\
      vector(screen_rect.bottomright)*0.25
    self.pos = vector(pos)
    self.velocity = vector(1).rotate(random()*360)*250
    self.prevPos, self.prevVelocity = vector(), vector()
    boid.all.append(self)
  
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
  
  def edgePush(self):
    amount = vector()
    percent = 15/(fps if fps else 1)
    if self.x < boid.limit.left:
      amount.x = boid.limit.left-self.x
    elif self.x > boid.limit.right:
      amount.x = boid.limit.right-self.x
    if self.y < boid.limit.top:
      amount.y = boid.limit.top-self.y
    elif self.y > boid.limit.bottom:
      amount.y = boid.limit.bottom-self.y
    return amount*percent
  
  def move(self):
    self.prevPos, self.prevVelocity = vector(self.pos), vector(self.velocity)
    change = vector()
    change += self.edgePush()
    self.velocity += change
    if self.velocity.length_squared() > boid.speed_lim*boid.speed_lim:
      self.velocity.scale_to_length(boid.speed_lim)
    self.pos += self.velocity*(boid.currentTime-boid.prevTime)/1000
    self.x = max(min(self.x, screen_rect.right), screen_rect.left)
    self.y = max(min(self.y, screen_rect.bottom), screen_rect.top)
  
  def draw(self, color):
    update_rects.append(pygame.draw.circle(screen, color, self.intPos, boid.size))

def intVector(v):
  return int(v.x), int(v.y)

for i in range(5): boid()

screen.fill(background)
pygame.display.flip()

boid.currentTime = pygame.time.get_ticks()
while True:
  clock.tick(-1)
  fps = clock.get_fps()
  update_rects = [update_rects[1:]]
  
  if pygame.event.get(QUIT):
    break
  for event in pygame.event.get():
    if event.type == KEYDOWN:
      if event.key == K_ESCAPE:
        pygame.event.post(pygame.event.Event(QUIT))
  
  screen.fill(background)
  boid.prevTime, boid.currentTime = boid.currentTime, pygame.time.get_ticks()
  boid.tickTime = (boid.currentTime-boid.prevTime)
  
  for Boid in boid.all:
    Boid.move()
    Boid.draw(foreground)
  
  screen.blit(font.render(str(round(fps)), 0, foreground), (0,0))
  update_rects.append(pygame.rect.Rect((0,0), font.size(str(round(fps)))))
  pygame.display.update(update_rects[0]+update_rects[1:])
pygame.quit()
