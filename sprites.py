import pygame
from config import *
import math
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, game,x ,y):
        self.groups = game.all_sprites
        self._layer = PLAYER_LAYER
        self.game = game
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = "down"

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.movement()

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x_change -= PLAYER_SPEED
            self.facing = "left"
        if keys[pygame.K_d]:
            self.x_change += PLAYER_SPEED
            self.facing = "right"
        if keys[pygame.K_w]:
            self.y_change -= PLAYER_SPEED
            self.facing = "up"
        if keys[pygame.K_s]:
            self.y_change += PLAYER_SPEED
            self.facing = "down"


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, self.game.blocks
        self._layer = BLOCK_LAYER
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill("green")
        self.rect = self.image.get_rect()

        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
