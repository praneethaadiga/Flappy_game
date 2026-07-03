import pygame
import math
import random


pygame.init()
screen = pygame.display.set_mode((600,800))
pygame.display.set_caption('Flappy Bird')
background = pygame.image.load('fb-background.jpg')

bird = pygame.image.load('bd.jpg').convert_alpha()
bird = pygame.transform.scale(bird, (50, 50))

PIPE_WIDTH = 80
PIPE_GAP = 200
PIPE_VELOCITY = 5

clock = pygame.time.Clock()
scroll = 0 
bg_width = background.get_width()
tiles = math.ceil(600 / (bg_width)) + 1

GREEN = (0, 255, 0)

class Bird:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.gravity = 0.5
        self.lift = -10
    
    def jump(self):
        self.velocity = self.lift

    def update(self):
        self.velocity += self.gravity
        self.y +=self.velocity

        if self.y > 750:
            self.y = 750
            self.velocity = 0
        if self.y < 0:
            self.y = 0
            self.velocity = 0

    def draw(self):
        screen.blit(bird,(self.x,self.y))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, 50, 50)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.width = PIPE_WIDTH
        self.gap = PIPE_GAP
        self.top_height = random.randint(100, 500)
        self.bottom_y = self.top_height + self.gap

    def update(self):
        self.x -= PIPE_VELOCITY
        if self.x < -self.width:
            self.x = 600
            self.top_height = random.randint(100, 500)
            self.bottom_y = self.top_height + self.gap

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.top_height))
        pygame.draw.rect(screen, GREEN, (self.x, self.bottom_y, self.width, 800 - self.bottom_y))

    def get_rects(self):
        top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        bottom_rect = pygame.Rect(self.x, self.bottom_y, self.width, 800 - self.bottom_y)
        return top_rect, bottom_rect

bir = Bird(100,300)
pipes = [Pipe(700),Pipe(1000)]

running = True
while running:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bir.jump()

    scroll-=5
    if abs(scroll) > bg_width:
        scroll = 0
    
    for i in range(tiles):
        screen.blit(background,(i * bg_width + scroll,0))
    
    for pipe in pipes:
        pipe.update()
        pipe.draw()

    bir.update()
    bir.draw()
    
    bird_rect = bir.get_rect()
    for pipe in pipes:
        top_rect, bottom_rect = pipe.get_rects()
        if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
            print("Game Over")
            running = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()

 