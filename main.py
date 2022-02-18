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
prevTime, currentTime = 0, 0

def intVector(v):
  return int(v.x), int(v.y)

class boid:
  all = []
  tickTime = 0
  size = 5
  limit = pygame.rect.Rect((0, 0), vector(screen_rect.size)*0.75)
  limit.center = screen_rect.center
  speed_lim = 375.0
  drawParticle = lambda self:
    update_rects.append(pygame.draw.circle(screen, color, intVector(self.pos), int(boid.size*self.timeLeftPercent)))
  
  def __init__(self, pos=None, velocity=None, speed=250):
    if pos is None:
      pos = vector(random()*screen_rect.w, random()*screen_rect.h)*0.5 +\
      vector(screen_rect.bottomright)*0.25
    self.pos = vector(pos)
    if velocity is None:
      self.velocity = vector(1,0).rotate(random()*360)*speed
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
  
  #separation: avarage of diff in pos
  #alignment: avarage of velocity
  #cohesion: avarage of realitive location
  
  def edgePush(self):
    amount = 500/(fps if fps else 1)
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
    change = vector()
    self.velocity += change
    if self.velocity.length_squared() > boid.speed_lim*boid.speed_lim:
      self.velocity.scale_to_length(boid.speed_lim)
    self.pos += self.velocity*(currentTime-prevTime)/1000
    self.x = max(min(self.x, screen_rect.right), screen_rect.left)
    self.y = max(min(self.y, screen_rect.bottom), screen_rect.top)
  
  def draw(self, color=foreground):
    particle(self.pos, 1000, boid.drawParticle)

class particle:
  all = []
  
  def __init__(self, pos, time, draw):
    self.pos, self._draw = vector(pos), draw
    self.begin, self.lastFor, self.end = currentTime, time, time+currentTime
    particle.all.append(self)
  
  @property
  def time(self):
    return currentTime - self.begin
  
  @property
  def timeLeft(self):
    return self.end - currentTime
  
  @property
  def timePercent(self):
    return self.time/self.lastFor
  
  @property
  def timeLeftPercent(self):
    return self.timeLeft/self.lastFor
  
  def draw(self):
    self._draw(self)
    if currentTime>self.end:
      particle.all.remove(self)
    

for i in range(5): boid()

screen.fill(background)
pygame.display.flip()

currentTime = pygame.time.get_ticks()

while True:
  clock.tick(31-1)
  fps = clock.get_fps()
  update_rects = [update_rects[1:]]
  
  if pygame.event.get(QUIT):
    break
  for event in pygame.event.get():
    if event.type == KEYDOWN:
      if event.key == K_ESCAPE:
        pygame.event.post(pygame.event.Event(QUIT))
  
  screen.fill(background)
  
  prevTime, currentTime = currentTime, pygame.time.get_ticks()
  boid.tickTime = (currentTime-prevTime)
  
  for Boid in boid.all:
    Boid.move()
    Boid.draw()
  [*map(particle.draw, particle.all)]
  
  screen.blit(font.render(str(round(fps)), 0, foreground), (0,0))
  update_rects.append(pygame.rect.Rect((0,0), font.size(str(round(fps)))))
  pygame.display.update(update_rects[0]+update_rects[1:])
pygame.quit()
