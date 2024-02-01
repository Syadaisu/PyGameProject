import pygame
from config import *
import sys
from sprites.Button import Button
from shop import *
from popup import *
import time

def use_potion(self):
        if self.inventory.get_item('Health Potion')>0:  # Check if there are any potions
            self.inventory.remove_item('Health Potion')  # Use one potion
            self.player.stats.health += 5  # Increase health by 50
            if self.player.stats.health > self.player.stats.max_health:  # Don't exceed max health
                self.player.stats.health = self.player.stats.max_health
    
def draw_gold(self, amount,x,y):
    # Load the sprite sheet
    sprite_sheet = pygame.image.load('assets/gold.png')

        # Define the rectangle that contains the gold icon
        # Replace x, y, width, and height with the actual values
    gold_icon_rect = pygame.Rect(0, 0, 16, 16)

        # Extract the gold icon from the sprite sheet
    gold_icon = sprite_sheet.subsurface(gold_icon_rect)

        # Draw the gold icon
    self.screen.blit(gold_icon, (x, y))

        # Create a font object
    font = pygame.font.Font(None, 32)

        # Create a surface with the amount text
    amount_text = font.render(str(amount), True, (255, 255, 255))

        # Draw the amount text next to the gold icon
    self.screen.blit(amount_text, (gold_icon.get_width() + x+10, y))
    
def draw_hp(self, current_hp, max_hp, x, y):
    # Extract the HP icon from the sprite sheet
    sprite_sheet = pygame.image.load('assets/hearts.png')
        
    hp_icon_rect = pygame.Rect(0, 0, 16, 16)
    hp_icon = sprite_sheet.subsurface(hp_icon_rect)

        # Draw the HP icon
    self.screen.blit(hp_icon, (x, y))

        # Create a font object
    font = pygame.font.Font(None, 32)

        # Create a surface with the HP text
    hp_text = font.render(f"{current_hp}/{max_hp}", True, (255, 255, 255))

        # Draw the HP text next to the HP icon
    self.screen.blit(hp_text, (hp_icon.get_width() + x + 10, y))
        
def draw_strenght(self, amount,x,y):
    # Load the sprite sheet
    sprite_sheet = pygame.image.load('assets/weapons.png')

        # Define the rectangle that contains the gold icon
        # Replace x, y, width, and height with the actual values
    weapon_icon_rect = pygame.Rect(112, 0, 16, 16)

        # Extract the gold icon from the sprite sheet
    weapon_icon = sprite_sheet.subsurface(weapon_icon_rect)

        # Draw the gold icon
    self.screen.blit(weapon_icon, (x, y))

        # Create a font object
    font = pygame.font.Font(None, 32)

        # Create a surface with the amount text
    amount_text = font.render(str(amount), True, (255, 255, 255))

        # Draw the amount text next to the gold icon
    self.screen.blit(amount_text, (weapon_icon.get_width() + x+10, y))
        
def draw_xp(self, xp, xp_to_next_level, x, y):
    # Extract the HP icon from the sprite sheet
    sprite_sheet = pygame.image.load('assets/xp.png')
        
    xp_icon_rect = pygame.Rect(0, 0, 16, 16)
    xp_icon = sprite_sheet.subsurface(xp_icon_rect)

        # Draw the HP icon
    self.screen.blit(xp_icon, (x, y))

        # Create a font object
    font = pygame.font.Font(None, 32)

        # Create a surface with the HP text
    xp_text = font.render(f"{xp}/{xp_to_next_level}", True, (255, 255, 255))

        # Draw the HP text next to the HP icon
    self.screen.blit(xp_text, (xp_icon.get_width() + x + 10, y))
    
def draw_potions(self, amount,x,y):
    # Load the sprite sheet
    sprite_sheet = pygame.image.load('assets/potions.png')

        # Define the rectangle that contains the gold icon
        # Replace x, y, width, and height with the actual values
    potion_icon_rect = pygame.Rect(144, 0, 16, 16)

        # Extract the gold icon from the sprite sheet
    potion_icon = sprite_sheet.subsurface(potion_icon_rect)

        # Draw the gold icon
    self.screen.blit(potion_icon, (x, y))

        # Create a font object
    font = pygame.font.Font(None, 32)

        # Create a surface with the amount text
    amount_text = font.render(str(amount), True, (255, 255, 255))

        # Draw the amount text next to the gold icon
    self.screen.blit(amount_text, (potion_icon.get_width() + x+10, y))
    
def draw_level(self, amount,x,y):
    # Load the sprite sheet
    sprite_sheet = pygame.image.load('assets/level.png')

        # Define the rectangle that contains the gold icon
        # Replace x, y, width, and height with the actual values
    level_icon_rect = pygame.Rect(0, 0, 16, 16)

        # Extract the gold icon from the sprite sheet
    level_icon = sprite_sheet.subsurface(level_icon_rect)

        # Draw the gold icon
    self.screen.blit(level_icon, (x, y))

        # Create a font object
    font = pygame.font.Font(None, 32)

        # Create a surface with the amount text
    amount_text = font.render(str(amount), True, (255, 255, 255))

        # Draw the amount text next to the gold icon
    self.screen.blit(amount_text, (level_icon.get_width() + x+10, y))
    
def choose_player_sprite():
    pygame.init()

    # Load the sprite sheet
    sprite_sheet1 = pygame.image.load('assets/Player1.png')
    sprite_sheet2 = pygame.image.load('assets/Player2.png')
    choice1 = 'assets/Player1.png'
    choice2 = 'assets/Player2.png'
    

    # Define the rectangles that contain the player sprites
    # Replace x, y, width, and height with the actual values
    player_sprite1_rect = pygame.Rect(0, 0, TILESIZE, TILESIZE)
    player_sprite2_rect = pygame.Rect(0, 0, TILESIZE, TILESIZE)

    # Extract the player sprites from the sprite sheet
    player_sprite1 = pygame.transform.scale(sprite_sheet1.subsurface(player_sprite1_rect), (TILESIZE*4, TILESIZE*4))
    player_sprite2 = pygame.transform.scale(sprite_sheet2.subsurface(player_sprite2_rect), (TILESIZE*4, TILESIZE*4))

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
                    return choice1
                # If the player clicks on the right half of the screen, choose player_sprite2
                else:
                    return choice2

        # Draw a grey rectangle with a white border
        pygame.draw.rect(screen, (128, 128, 128), pygame.Rect(0, 0, screen.get_width(), screen.get_height()))
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, 0, screen.get_width(), screen.get_height()), 4)
        
        pygame.draw.rect(screen, (96, 96, 96), pygame.Rect(0, 0, screen.get_width(), 50))
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, 0, screen.get_width(), 50), 2)
        
        pygame.draw.line(screen, (255, 255, 255), (screen.get_width() / 2, 50), (screen.get_width() / 2, screen.get_height()), 2)
        
        screen.blit(player_sprite1, (screen.get_width() / 4 - player_sprite1.get_width() / 2, screen.get_height() / 2 - player_sprite1.get_height() / 2))
        screen.blit(player_sprite2, (screen.get_width() * 3 / 4 - player_sprite2.get_width() / 2, screen.get_height() / 2 - player_sprite2.get_height() / 2))
        
            
        font = pygame.font.Font(None, 32)
        # Create a surface with the "Pick your character" text
        text = font.render("Pick your character", True, (255, 255, 255))

        # Calculate the position of the text
        text_rect = text.get_rect(center=(screen.get_width() / 2, 25))

        # Draw the text
        screen.blit(text, text_rect)

        pygame.display.flip()
            
def draw_bottom_bar(self):
    pygame.draw.rect(self.screen, (64, 64, 64), pygame.Rect(0, self.screen.get_height() - 100, self.screen.get_width(), 100))
    pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(0, self.screen.get_height() - 100, self.screen.get_width(), 100), 2)

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
    # Create a font object
    font = pygame.font.Font(None, 64)
    small_font = pygame.font.Font(None, 32)

    # Create a surface with the "Game Over" text
    game_over_text = font.render("Game Over", True, (255, 255, 255))

    # Create a surface with the "Press R to restart" text
    restart_text = small_font.render("Press R to quit", True, (255, 255, 255))

    # Calculate the position of the "Game Over" text
    game_over_rect = game_over_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))

    # Calculate the position of the "Press R to restart" text
    restart_rect = restart_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 + 70))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                return  # Restart the game when R key is pressed

        # Fill the screen with black color
        self.screen.fill("black")

        # Draw the "Game Over" text
        self.screen.blit(game_over_text, game_over_rect)

        # Draw the "Press R to restart" text
        self.screen.blit(restart_text, restart_rect)

        # Update the display
        pygame.display.update()
        
def shop_menu(self):
    shop = Shop()
    back_button = Button(1110, 625, 150, 50, "white", "#5A5A5A", "Back", 32)
    sword_button = ShopButton(170, 608, 600, 44, "white", "#5A5A5A", "Sword Upgrade", 32)
    health_potion_button = ShopButton(170, 654, 600, 44, "white", "#5A5A5A", "Health Potion", 32)
    shop_background = pygame.transform.scale(pygame.image.load("assets/shop_bg.png"), (WIDTH, HEIGHT))

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
                if self.inventory.get_item('Gold') >= 100:
                    print("Bought a sword")
                    self.inventory.remove_item('Gold',100)
                    self.player.stats.strength += 1
                else:
                    show_popup = True
                    message = "You don't have enough gold to buy a sword"
                    print("Not enough gold")

            if health_potion_button.is_pressed(mouse_pos, mouse_pressed, self.inventory, shop):
                if self.inventory.get_item('Gold') >= 25:
                    print("Bought a health potion")
                    self.inventory.remove_item('Gold',25)
                else: 
                    show_popup = True
                    self.inventory.remove_item('Health Potion')
                    message = "You don't have enough gold to buy a health potion"
                    print("Not enough gold")
        if show_popup:
            popup = Popup(300, 100, message)
            popup_surface = popup.render()
            self.screen.blit(popup_surface, (WIDTH/2-150, HEIGHT/2-50))
            pygame.display.flip()
            time.sleep(0.5)
            show_popup = False
            
        self.screen.blit(shop_background, (0, 0))   
        draw_bottom_bar(self)
        draw_gold(self,100, 100, 620)
        draw_gold(self,25, 100, 665)
        font = pygame.font.Font(None, 32)
        text = font.render("Current:", True, (255, 255, 255))
        self.screen.blit(text, (800, 640))
        draw_gold(self,self.inventory.get_item('Gold'), 900, 640)
        self.screen.blit(back_button.image, back_button.rect)
        self.screen.blit(sword_button.image, sword_button.rect)
        self.screen.blit(health_potion_button.image, health_potion_button.rect)

        self.clock.tick(FPS)
        pygame.display.update()
