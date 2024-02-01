import pygame
from config import *
import sys
from inventory import *
from shop import *
from sprites.Spritesheet import Spritesheet
from popup import *
from game import Game
from ui import *


g = Game()
while g.intro:
    intro_screen(g)
    if g.options:
        g.options_screen()
chosen_sprite = choose_player_sprite()
print(f'You chose: {chosen_sprite}')
g.character_spritesheet = Spritesheet(f'{chosen_sprite}')
g.new()
inventory = Inventory()

while g.running:
    g.game_loop()
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    game_over(g)

pygame.quit()
sys.exit()
