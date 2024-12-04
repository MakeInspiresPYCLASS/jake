import pygame
from pygame.locals import *
import sys
import random
import os
 
pygame.init()
 
vec = pygame.math.Vector2 
HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60
FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

class Player(pygame.sprite.Sprite):
    def __init__(self, image_name = 'kirby.jpg'):
        super().__init__() 
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128,255,40))
        self.rect = self.surf.get_rect()
   
        self.pos = vec((10, 385))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        
        self.jumps = 0
        
        self.update_image(image_name)
        
    def update_image(self, image_name = 'kirby.jpg'):
        image = pygame.image.load(os.path.abspath(image_name))
        image = pygame.transform.scale(image, self.rect.size)
        image = image.convert()
        
        self.surf.blit(image, self.rect)

    def move(self):
        self.acc = vec(0,0.5)
    
        pressed_keys = pygame.key.get_pressed()            
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
             
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
         
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
            
        self.rect.midbottom = self.pos
        
    def update(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if P1.vel.y > 0:
            if hits:
                self.pos.y = hits[0].rect.top + 2
                self.vel.y = 0
            
    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        
        if self.jumps == 1:
            self.vel.y = -10
            self.jumps = 0

        if hits:
            self.vel.y = -15
            self.jumps += 1

class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((random.randint(50, 100), 12))
        self.surf.fill((0,255,0))
        self.rect = self.surf.get_rect(center = (random.randint(0, WIDTH - 10), random.randint(0, HEIGHT - 30)))
        
def plat_gen():
    while len(platforms) < 7:
        width = random.randrange(50, 100)
        p = platform()
        p.rect.center = (random.randrange(0, WIDTH - width), random.randrange(-50, 5))
        platforms.add(p)
        all_sprites.add(p)

PT1 = platform()
PT1.surf = pygame.Surface((WIDTH, 20))
PT1.surf.fill((255,0,0))
PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))

P1 = Player()

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)

platforms = pygame.sprite.Group()
platforms.add(PT1)

for i in range(random.randint(5, 6)):
    pl = platform()
    platforms.add(pl)
    all_sprites.add(pl)
 
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                P1.jump()
     
    displaysurface.fill((0,0,0))
 
    P1.move()
    P1.update()
    
    if P1.rect.top <= HEIGHT / 3:
        P1.pos.y == abs(P1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()
                plat_gen()

    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
    
    pygame.display.update()
    FramePerSec.tick(FPS)