import pygame
from config import *
import random
from sprites.Attack import Attack
import math
from characterstats import CharacterStats

class Enemy(pygame.sprite.Sprite):
    
    def __init__(self, game,x,y,health):
        self.groups = game.all_sprites, game.enemies
        self._layer = ENEMY_LAYER
        self.game = game
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE                                                                                                                                                                                                   
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.stats = CharacterStats(20,1,1)
        
        self.change_direction_delay = 0
        
        self.x_change = 0
        self.y_change = 0
        
        self.gold = random.randint(5, 15)
        self.xp = random.randint(1, 15)
        
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.animate_speed = 200
        
        self.movement_loop = 0
        self.max_travel = random.randint(10, 50)
        
        self.last_attack_time = pygame.time.get_ticks()  # Initialize to current time
        self.attack_cooldown = 2000  # Cooldown period in milliseconds
        
        
        self.image = self.game.skeleton_spritesheet.getSprite(0, 0, self.width, self.height)
        self.image.set_colorkey("black")
        
        self.facing = random.choice(["up", "down", "left", "right"])
        
        self.rect=self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def update(self):
        self.movement()
        self.animate()
        
        self.rect.x += self.x_change
        self.collision_handler("x")
        self.rect.y += self.y_change
        self.collision_handler("y")

       
        
        self.x_change = 0
        self.y_change = 0


        
    def movement(self):
        if self.facing == "up":
            self.y_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = random.choice(["up", "down", "left", "right"])
        if self.facing == "down":
            self.y_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = random.choice(["up", "down", "left", "right"])
        if self.facing == "left":
            self.x_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = random.choice(["up", "down", "left", "right"])
        if self.facing == "right":
            self.x_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = random.choice(["up", "down", "left", "right"])
    
    
    
    def animate(self):
        now = pygame.time.get_ticks()
        down_animations = [self.game.skeleton_spritesheet.getSprite(0, 0, self.width, self.height),
                           self.game.skeleton_spritesheet.getSprite(32, 0, self.width, self.height),
                           self.game.skeleton_spritesheet.getSprite(64, 0, self.width, self.height)]
        up_animations = [self.game.skeleton_spritesheet.getSprite(0, 96, self.width, self.height),
                            self.game.skeleton_spritesheet.getSprite(32, 96, self.width, self.height),
                            self.game.skeleton_spritesheet.getSprite(64, 96, self.width, self.height)]
        left_animations = [self.game.skeleton_spritesheet.getSprite(0, 32, self.width, self.height),
                            self.game.skeleton_spritesheet.getSprite(32, 32, self.width, self.height),
                            self.game.skeleton_spritesheet.getSprite(64, 32, self.width, self.height)]
        right_animations = [self.game.skeleton_spritesheet.getSprite(0, 64, self.width, self.height),
                            self.game.skeleton_spritesheet.getSprite(32, 64, self.width, self.height),
                            self.game.skeleton_spritesheet.getSprite(64, 64, self.width, self.height)]
        
        if now - self.last_update > self.animate_speed:  # Time to update the frame
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % 3  # Assuming you have 3 frames for each direction

            if self.y_change < 0:  # Moving up
                self.image = up_animations[self.current_frame]
            elif self.y_change > 0:  # Moving down
                self.image = down_animations[self.current_frame]
            elif self.x_change < 0:  # Moving left
                self.image = left_animations[self.current_frame]
            elif self.x_change > 0:  # Moving right
                self.image = right_animations[self.current_frame]
                
    def collision_handler(self, direction):
       
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.facing = random.choice(["up", "down", "left", "right"])
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.facing = random.choice(["up", "down", "left", "right"])
                    self.rect.x = hits[0].rect.right
                self.x_change = 0
                

            # Check for collisions with other enemies
            enemies = self.game.enemies.copy()
            enemies.remove(self)
            if pygame.sprite.spritecollide(self, enemies, False):
                self.facing = random.choice(["up", "down", "left", "right"])
                self.x_change = 0

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.facing = random.choice(["up", "down", "left", "right"])
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.facing = random.choice(["up", "down", "left", "right"])
                    self.rect.y = hits[0].rect.bottom
                self.y_change = 0

            # Check for collisions with other enemies
            enemies = self.game.enemies.copy()
            enemies.remove(self)
            if pygame.sprite.spritecollide(self, enemies, False):
                self.facing = random.choice(["up", "down", "left", "right"])
                self.y_change = 0
            
    def is_player_in_range(self, player):
        dx = self.rect.x - player.rect.x
        dy = self.rect.y - player.rect.y
        distance = math.sqrt(dx**2 + dy**2)
        current_time = pygame.time.get_ticks()
        if distance <= TILESIZE*2 and current_time - self.last_attack_time > self.attack_cooldown:
            if self.facing =='up':
                attack = Attack(self.game, self.rect.x, self.rect.y - TILESIZE, self.stats.strength, ENEMY_LAYER, self.game.enemy_attacks)
                attack.attacker = self  # Set the attacker
            if self.facing =='down':
                attack = Attack(self.game, self.rect.x, self.rect.y + TILESIZE, self.stats.strength, ENEMY_LAYER, self.game.enemy_attacks)
                attack.attacker = self  # Set the attacker
            if self.facing =='left':
                attack = Attack(self.game, self.rect.x - TILESIZE, self.rect.y , self.stats.strength, ENEMY_LAYER, self.game.enemy_attacks)
                attack.attacker = self  # Set the attacker
            if self.facing =='right':
                attack = Attack(self.game, self.rect.x + TILESIZE, self.rect.y , self.stats.strength, ENEMY_LAYER, self.game.enemy_attacks)
                attack.attacker = self  # Set the attacker
            self.last_attack_time = current_time  # Update the last attack time
        else:
            return False
        