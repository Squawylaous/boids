import pygame
from pygame.locals import *
from pygame.math import Vector2 as vector
from random import random
from math import ceil, floor

pygame.init()

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 25)
background = Color(161, 161, 161)
foreground = Color(255, 255, 255)
screen = pygame.display.set_mode((0, 0), FULLSCREEN)
screen_rect = screen.get_rect()

update_rects = [[]]
fps = 0
drawLines = False

def intVector(v):
  return int(v.x), int(v.y)

class boid:
  all = []
  size, degrees = 7.5, 60
  limit = pygame.rect.Rect((0,0), screen_rect.size-vector(200, 200))
  limit.center = screen_rect.center
  speed_lim, sightRange = 15, 100**2
  
  def __init__(self, pos=None, velocity=None):
    if pos is None:
      pos = vector(random()*screen_rect.w, random()*screen_rect.h)
    self.pos = vector(pos)
    if velocity is None:
      self.velocity = vector(1,0).rotate(random()*360)*(random()*10 - 5)
    else:
      self.velocity = vector(velocity)
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
  
  def separation(self, others):
    others = [i for i in others if self.pos.distance_squared_to(i.pos) < 20*20]
    change = sum([self.pos - i.pos for i in others], vector())
    return change * 0.05
  
  def alignment(self, others):
    change = sum([i.velocity for i in others], vector())/len(others) - self.velocity
    return change * 0.05
  
  def cohesion(self, others):
    change = sum([i.pos for i in others], vector())/len(others) - self.pos
    return change * 0.005
  
  def edgePush(self):
    amount = 1.5
    if self.x < boid.limit.left:
      self.velocity.x += amount
    elif self.x > boid.limit.right:
      self.velocity.x -= amount
    if self.y < boid.limit.top:
      self.velocity.y += amount
    elif self.y > boid.limit.bottom:
      self.velocity.y -= amount

  def move(self):
    self.prevPos, self.prevVelocity = vector(self.pos), vector(self.velocity)
    self.edgePush()
    others = [i for i in boid.all if (i is not self and self.pos.distance_squared_to(i.pos)<boid.sightRange)]
    if others:
      self.velocity += sum(map(lambda x:getattr(self,x)(others), ["separation","alignment","cohesion"]), vector())
    if self.velocity.length_squared() > boid.speed_lim*boid.speed_lim:
      self.velocity.scale_to_length(boid.speed_lim)
    self.pos += self.velocity
  
  def draw(self, color=foreground):
    offset = self.velocity.normalize()*boid.size
    corner1 = offset.rotate(boid.degrees/2-180)+self.pos
    corner2 = offset.rotate(180-boid.degrees/2)+self.pos
    tip = 2*self.pos-corner1.lerp(corner2, 0.5)
    update_rects.append(pygame.draw.polygon(screen, color, [*map(intVector, [tip, corner1, corner2])]))

for i in range(100): boid()

screen.fill(background)
pygame.display.flip()

currentTime = pygame.time.get_ticks()

while True:
  clock.tick(-1)
  fps = clock.get_fps()
  update_rects = [update_rects[1:]]
  
  if pygame.event.get(QUIT):
    break
  for event in pygame.event.get():
    if event.type == KEYDOWN:
      if event.key == K_SPACE:
        drawLines = not drawLines
      elif event.key == K_ESCAPE:
        pygame.event.post(pygame.event.Event(QUIT))
  
  screen.fill(background)
  
  prevTime, currentTime = currentTime, pygame.time.get_ticks()
  [*map(boid.move, boid.all)]
  [*map(boid.draw, boid.all)]
  
  if fps != float("inf"):
    screen.blit(font.render(str(int(fps)), 0, foreground), (0,0))
    update_rects.append(pygame.rect.Rect((0,0), font.size(str(int(fps)))))
  pygame.display.update(update_rects[0]+update_rects[1:])
pygame.quit()
