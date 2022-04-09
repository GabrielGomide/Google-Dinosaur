import pygame
from settings import *

class Sprite:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Obstacle(Sprite):
    def __init__(self, x, y, width, height, image):
        super().__init__(x, y, width, height)
        self.image = image

    def get_image(self):
        return pygame.transform.scale(self.image, (self.width, self.height))

    def update(self, speed):
        self.x -= speed

class Player(Sprite):
    def __init__(self, x, y, width, height, speed, image):
        super().__init__(x, y, width, height)
        self.image = image
        self.speed = speed
        self.jumping = False
        self.falling = False
        self.down = False
        self.max_jumps = 22
        self.jumps_left = self.max_jumps
        self.wait_to_squat = False

    def get_image(self):
        return pygame.transform.scale(self.image, (self.width, self.height))

    def squat(self):
        if not self.down:
            if not self.jumping and not self.falling:
                self.down = True
                self.image = dino_down
                self.width = 68
                self.height = 33
                self.y += 20
            else:
                self.wait_to_squat = True

    def raise_dino(self):
        if self.down:
            self.down = False
            self.image = dino
            self.width = 50
            self.height = 53
            self.y -= 20

    def handle_movement(self, key):
        if self.wait_to_squat:
            self.wait_to_squat = False
            self.squat()

        if key[pygame.K_SPACE] or key[pygame.K_w] or key[pygame.K_UP]:
            if not self.jumping and not self.falling:
                self.jumping = True
                self.image = dino
                self.raise_dino()

        if self.jumping:
            self.y -= self.speed
            self.jumps_left -= 1

            if self.jumps_left == 0:
                self.jumping = False
                self.falling = True
                self.jumps_left = self.max_jumps

        if self.falling:
            self.y += self.speed
            self.jumps_left -= 1

            if self.jumps_left == 0:
                self.falling = False
                self.jumps_left = self.max_jumps

