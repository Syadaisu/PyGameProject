import pygame
from config import *

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y,theme):
        self.game = game
        self.groups = game.all_sprites
        self._layer = GROUND_LAYER
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.theme = theme
        
        if theme == "grass":
            self.image = self.game.terrain_spritesheet.getSprite(64, 352, self.width, self.height)
        elif theme == "castle":
            self.image = self.game.terrain_spritesheet.getSprite(928, 640, self.width, self.height)


        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
