import pygame
import os

pygame.mixer.init()

assets = os.path.join(os.getcwd(), 'Assets')
dino = pygame.image.load(os.path.join(assets, 'dino.png'))
dino_died = pygame.image.load(os.path.join(assets, 'dino_died.png'))
dino_walking01 = pygame.image.load(os.path.join(assets, 'dino_walking01.png'))
dino_walking02 = pygame.image.load(os.path.join(assets, 'dino_walking02.png'))
dino_down = pygame.image.load(os.path.join(assets, 'dino_down.png'))
dino_down_walking01 = pygame.image.load(os.path.join(assets, 'dino_down_walking01.png'))
dino_down_walking02 = pygame.image.load(os.path.join(assets, 'dino_down_walking02.png'))
cactus01 = pygame.image.load(os.path.join(assets, 'cactus01.png'))
cactus02 = pygame.image.load(os.path.join(assets, 'cactus02.png'))
cactus03 = pygame.image.load(os.path.join(assets, 'cactus03.png'))
bird01 = pygame.image.load(os.path.join(assets, 'bird01.png'))
bird02 = pygame.image.load(os.path.join(assets, 'bird02.png'))

point_sound = pygame.mixer.Sound(os.path.join(assets, 'point.wav'))
