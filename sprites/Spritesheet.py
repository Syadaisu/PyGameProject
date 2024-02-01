import pygame
from config import *

class Spritesheet:
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert()

    def getSprite(self, x, y, width, height):
        sprite = pygame.Surface((width, height))
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey("black")
        return sprite