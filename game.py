import pygame
from config import *
import sys
import time
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


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Game")
        self.clock = pygame.time.Clock()
        self.shop_button = Button(550,650, 150, 50, "white", "#5A5A5A", "Shop", 32)
        self.running = True
        self.intro = True
        self.options=False
        self.inventory = Inventory()
        self.inventory.add_item("Sword")
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

    def choose_player_sprite(self):
        pygame.init()

        # Load the two player sprites
        player_sprite1 = 'assets/Player1.png'
        player_sprite2 = 'assets/Player2.png'

        # Create a window
        screen = pygame.display.set_mode((WIDTH, HEIGHT))

        # Main loop
        while True:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # If the player clicks on the left half of the screen, choose player_sprite1
                    if pygame.mouse.get_pos()[0] < screen.get_width() / 2:
                        return player_sprite1
                    # If the player clicks on the right half of the screen, choose player_sprite2
                    else:
                        return player_sprite2

            # Draw the sprites
            screen.blit(pygame.image.load(f'{player_sprite1}'), (0, 0))
            screen.blit(pygame.image.load(f'{player_sprite2}'), (screen.get_width() / 2, 0))
            # Update the display
            pygame.display.flip()

    # Use the function
    
    
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
                    self.use_potion()
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

    def use_potion(self):
        if self.inventory.get_item('Health Potion')>0:  # Check if there are any potions
            self.inventory.remove_item('Health Potion')  # Use one potion
            self.player.stats.health += 5  # Increase health by 50
            if self.player.stats.health > self.player.stats.max_health:  # Don't exceed max health
                self.player.stats.health = self.player.stats.max_health
    
    
    def draw(self):
        self.screen.fill("black")
        self.all_sprites.draw(self.screen)
        self.draw_bottom_bar()
        self.screen.blit(self.shop_button.image, self.shop_button.rect)
        self.clock.tick(FPS)
        self.draw_inventory()  # Call the new function here
        self.draw_player_stats()  # Call the new function here
        pygame.display.update()

    def draw_bottom_bar(self):
        pygame.draw.rect(self.screen, (64, 64, 64), pygame.Rect(0, self.screen.get_height() - 100, self.screen.get_width(), 100))
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(0, self.screen.get_height() - 100, self.screen.get_width(), 100), 2)

    def draw_player_stats(self):
        font = pygame.font.Font(None, 32)  # Create a font object
        player_stats_text = "Player Stats: " + ", ".join(f"{stat}: {value}" for stat, value in vars(self.player.stats).items())
        player_stats_text += f", XP: {self.player.xp}"
        player_stats_surface = font.render(player_stats_text, True, (255, 255, 255))  # Create a surface with the player stats text
        self.screen.blit(player_stats_surface, (10, 50))  # Draw the player stats text on the screen
    
    def draw_inventory(self):
        font = pygame.font.Font(None, 32)  # Create a font object
        inventory_text = "Inventory: " + ", ".join(f"{item}: {quantity}" for item, quantity in self.inventory.get_inventory().items())
        text_surface = font.render(inventory_text, True, (255, 255, 255))  # Create a surface with the inventory text
        self.screen.blit(text_surface, (10, 10))  # Draw the inventory text on the screen
    
    def intro_screen(self):
        play_button = Button(550, 150, 150, 50, "white","#5A5A5A", "Play", 32)
        options_button = Button(505, 220, 240, 50, "white", "#5A5A5A", "Options", 32)
        quit_menu = Button(550, 290, 150, 50, "white", "#5A5A5A", "Quit", 32)
        menu_text = self.font.render("AdventureQuest", True, "#ff6b51")
        menu_rect = menu_text.get_rect(center=(640, 100))
        while self.intro:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.intro = False
                    self.running = False

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                print("play")
                self.intro = False

            if options_button.is_pressed(mouse_pos, mouse_pressed):
                self.options = True
                break

            if quit_menu.is_pressed(mouse_pos, mouse_pressed):
                self.intro = False
                self.running = False

            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(menu_text, menu_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.screen.blit(options_button.image, options_button.rect)
            self.screen.blit(quit_menu.image, quit_menu.rect)

            self.clock.tick(FPS)
            pygame.display.update()

    def options_screen(self):
        menu_text = self.font.render("This is the options menu", True, "#ff6b51")
        menu_rect = menu_text.get_rect(center=(640, 100))
        back_button = Button(550, 150, 150, 50, "white", "#5A5A5A", "Back", 32)

        while self.options:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print ("quit")
                    self.running= False


            options_mouse_pos = pygame.mouse.get_pos()
            options_mouse_pressed = pygame.mouse.get_pressed()

            if back_button.is_pressed(options_mouse_pos, options_mouse_pressed):
                self.options = False
                print("quit2")
                break

            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(menu_text, menu_rect)
            self.screen.blit(back_button.image, back_button.rect)

            self.clock.tick(FPS)
            pygame.display.update()

    def game_over(self):
        pass
    
    def get_random_position(self):
        x = random.randint(0, WIDTH - 100)  # Replace 'self.width' with the width of your game window
        y = random.randint(0, HEIGHT - 221)  # Replace 'self.height' with the height of your game window
        return x, y

    def game_loop(self):
        
        while self.playing:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if self.shop_button.is_pressed(mouse_pos, mouse_pressed):
                self.shop_menu()
            if len(self.enemies) < 3:
                self.createEnemy()

            pygame.display.flip()
            if self.player.stats.health <= 0:
                self.playing = False
                print("Player has died")
            self.screen.fill("black")
            self.all_sprites.draw(self.screen)
            
            self.events()
            self.draw()
            self.update()
            
            self.clock.tick(FPS)
        self.running=False

    def shop_menu(self):
        shop = Shop()
        back_button = Button(350, 550, 150, 50, "white", "#5A5A5A", "Back", 32)
        sword_button = ShopButton(100, 100, 150, 50, "white", "#5A5A5A", "Sword", 32)
        health_potion_button = ShopButton(100, 150, 150, 50, "white", "#5A5A5A", "Health Potion", 32)

        shop_running = True
        show_popup = False
        while shop_running:
            self.screen.fill("black")
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    shop_running = False
                    self.running = False

                if back_button.is_pressed(mouse_pos, mouse_pressed):
                    shop_running = False

                if sword_button.is_pressed(mouse_pos, mouse_pressed, self.inventory, shop):
                    if self.inventory.get_item('Gold') >= 10:
                        print("Bought a sword")
                        self.inventory.remove_item('Gold',10)
                        self.player.stats.strength += 1
                    else:
                        show_popup = True
                        message = "You don't have enough gold to buy a sword"
                        print("Not enough gold")

                if health_potion_button.is_pressed(mouse_pos, mouse_pressed, self.inventory, shop):
                    if self.inventory.get_item('Gold') >= 5:
                        print("Bought a health potion")
                        self.inventory.remove_item('Gold',5)
                    else: 
                        show_popup = True
                        message = "You don't have enough gold to buy a health potion"
                        print("Not enough gold")
            if show_popup:
                popup = Popup(300, 100, message)
                popup_surface = popup.render()
                self.screen.blit(popup_surface, (100, 100))
                pygame.display.flip()
                time.sleep(0.5)
                show_popup = False
                

            self.screen.fill("black")
            self.screen.blit(back_button.image, back_button.rect)
            self.screen.blit(sword_button.image, sword_button.rect)
            self.screen.blit(health_potion_button.image, health_potion_button.rect)

            self.clock.tick(FPS)
            pygame.display.update()
