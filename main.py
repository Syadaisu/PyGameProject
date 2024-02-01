import pygame
from config import *
import sys
from inventory import *
from shop import *
from sprites.Spritesheet import Spritesheet
from popup import *
from game import Game


g = Game()
while g.intro:
    g.intro_screen()
    if g.options:
        g.options_screen()
chosen_sprite = g.choose_player_sprite()
print(f'You chose: {chosen_sprite}')
g.character_spritesheet = Spritesheet(f'{chosen_sprite}')
g.new()
inventory = Inventory()

while g.running:
    g.game_loop()
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    g.game_over()

pygame.quit()
sys.exit()
