import pygame
from config import *
from inventory import *
from shop import *
from sprites.Spritesheet import Spritesheet
from popup import *
import random
from sprites.Button import Button
from sprites.Block import Block
from sprites.Ground import Ground
from sprites.Player import Player
from sprites.Enemy import Enemy
from sprites.Attack import Attack
from ui import *
import sys


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Game")
        self.clock = pygame.time.Clock()
        self.shop_button = Button(10,608, 150, 44, "white", "#5A5A5A", "Shop", 32)
        self.quit_button = Button(10,654, 150, 44, "white", "#5A5A5A", "Quit", 32)
        self.running = True
        self.intro = True
        self.options=False
        self.inventory = Inventory()
        self.inventory.add_item("Sword Upgrade", 1)
        self.inventory.add_item("Health Potion", 2)
        self.inventory.add_item("Gold",10)
        self.font = pygame.font.Font("assets/font.ttf", 32)
        self.character_spritesheet = Spritesheet("assets/Player1.png")
        self.terrain_spritesheet = Spritesheet("assets/terrain.png")
        self.intro_background = pygame.transform.scale(pygame.image.load("assets/background.png"), (WIDTH, HEIGHT))
        self.black_skeleton_spritesheet = Spritesheet("assets/Black_Skeleton.png")
        self.goblin_king_spritesheet = Spritesheet("assets/Goblin_King.png")
        self.skeleton_spritesheet = Spritesheet("assets/Skeleton.png")
        self.attack_spritesheet = Spritesheet("assets/attack.png")
        self.tilemap = random.choice([tilemap1, tilemap2, tilemap3])
        self.theme = random.choice(['grass', 'castle'])
        self.player = None

    def createTilemap(self):
        for i,row in enumerate(self.tilemap):
            for j,column in enumerate(row):
                Ground(self, j, i, self.theme)
                if column == 'B':
                    Block(self, j, i,self.theme)
                if column == 'P':
                    self.player=Player(self, j, i)
                if column == 'E':
                    Enemy(self, j, i,1,self.skeleton_spritesheet)
                    
    def createEnemy(self):
        for i,row in enumerate(self.tilemap):
            for j,column in enumerate(row):
                if column == 'E':
                    if self.player.stats.level >=3:
                        enemy_type = random.choice(['black_skeleton', 'skeleton', 'goblin_king'])
                        if enemy_type == 'black_skeleton':
                            Enemy(self, j, i, 2,self.black_skeleton_spritesheet)
                        if enemy_type == 'goblin_king':
                            Enemy(self, j, i, 3,self.goblin_king_spritesheet) 
                        else:
                            Enemy(self, j, i, 1,self.skeleton_spritesheet)# Replace with the actual code to create a black skeleton
                    elif self.player.stats.level >= 2:  # Replace 10 with the desired level threshold
                        # The player is high enough level, so there's a chance to spawn a black skeleton or a goblin king
                        enemy_type = random.choice(['black_skeleton', 'skeleton'])
                        if enemy_type == 'black_skeleton':
                            Enemy(self, j, i, 2,self.black_skeleton_spritesheet)  # Replace with the actual code to create a black skeleton
                        else:
                            Enemy(self, j, i, 1,self.skeleton_spritesheet)
                            
                    else:
                        # The player is not high enough level, so spawn a normal enemy
                        Enemy(self, j, i, 1,self.skeleton_spritesheet)

    
    
    
    def new(self):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.buildings = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.enemy_attacks = pygame.sprite.LayeredUpdates()
        self.createTilemap()

    def update(self):
        self.all_sprites.update()

    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Press 'P' to use a potion
                    use_potion(self)
                if event.key == pygame.K_SPACE:
                    if self.player.facing =='up':
                        attack = Attack(self, self.player.rect.x, self.player.rect.y - TILESIZE, self.player.stats.strength, PLAYER_LAYER, self.attacks)
                        attack.attacker = self.player  # Set the attacker
                    if self.player.facing =='down':
                        attack = Attack(self, self.player.rect.x, self.player.rect.y + TILESIZE, self.player.stats.strength, PLAYER_LAYER, self.attacks)
                        attack.attacker = self.player  # Set the attacker
                    if self.player.facing =='left':
                        attack = Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y , self.player.stats.strength, PLAYER_LAYER, self.attacks)
                        attack.attacker = self.player  # Set the attacker
                    if self.player.facing =='right':
                        attack = Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y , self.player.stats.strength, PLAYER_LAYER, self.attacks)
                        attack.attacker = self.player  # Set the attacker
        for enemy in self.enemies:  # Assuming self.game.enemies is a list of Enemy objects
            enemy.is_player_in_range(self.player)

    
    
    def draw(self):
        self.screen.fill("black")
        self.all_sprites.draw(self.screen)
        draw_bottom_bar(self)
        self.screen.blit(self.shop_button.image, self.shop_button.rect)
        self.screen.blit(self.quit_button.image, self.quit_button.rect)
        self.clock.tick(FPS)
        font = pygame.font.Font(None, 32)

        # Create surfaces with the desired text
        potion_text = font.render("Press P to drink a potion", True, (255, 255, 255))
        attack_text = font.render("Press SPACE to Attack", True, (255, 255, 255))
        move_text = font.render("Move with WSAD", True, (255, 255, 255))
        self.screen.blit(move_text, (800, 608)) 
        self.screen.blit(attack_text, (800, 642)) 
        self.screen.blit(potion_text, (800, 676))
        
        
        draw_gold(self,self.inventory.get_item('Gold'), 190, 620)
        draw_hp(self,self.player.stats.health, self.player.stats.max_health, 190, 660)
        draw_xp(self,self.player.xp, self.player.xp_to_next_level, 290, 620)
        draw_level(self,self.player.stats.level, 290, 660)
        draw_strenght(self,self.player.stats.strength, 390, 620)
        draw_potions(self,self.inventory.get_item('Health Potion'), 390, 660)
        
        pygame.display.update()

    
    
    def get_random_position(self):
        x = random.randint(0, WIDTH - 100)  # Replace 'self.width' with the width of your game window
        y = random.randint(0, HEIGHT - 221)  # Replace 'self.height' with the height of your game window
        return x, y

    def game_loop(self):
        
        while self.playing:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if self.shop_button.is_pressed(mouse_pos, mouse_pressed):
                shop_menu(self)
            if self.quit_button.is_pressed(mouse_pos, mouse_pressed):
                pygame.quit()
                sys.exit()
            if len(self.enemies) < 3:
                self.createEnemy()

            pygame.display.flip()
            if self.player.stats.health <= 0:
                self.playing = False
            self.screen.fill("black")
            self.all_sprites.draw(self.screen)
            
            self.events()
            self.draw()
            self.update()
            
            self.clock.tick(FPS)
        self.running=False
