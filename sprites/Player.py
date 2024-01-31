import pygame
from config import *
from characterstats import CharacterStats
import time

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
        self.invulnerable_until = 0
        
        self.level = 1  # The player's current level
        self.xp = 0  # The player's current xp
        self.xp_to_next_level = 100  # The amount of xp needed to level up
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.animate_speed = 200  # Change the frame every 200 milliseconds
        
        self.x_change = 0
        self.y_change = 0

        self.facing = "down"

        self.image = self.game.character_spritesheet.getSprite(0, 64, self.width, self.height)

        self.stats = CharacterStats(self.level*15,self.game.inventory.get_item('Sword'),self.level)  # Add this line to create a PlayerStats object for the player   

        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        
    def take_damage(self, amount):
        if time.time() > self.invulnerable_until:
            self.stats.health -= amount
            self.invulnerable_until = time.time() + 1  # 1 second of invulnerability

    def update(self):
        self.movement()
        self.animate()
        self.rect.x += self.x_change
        self.collision_handler("x")
        self.rect.y += self.y_change
        self.collision_handler("y")

        self.x_change = 0
        self.y_change = 0

    def gain_xp(self, amount):
        self.xp += amount
        while self.xp >= self.xp_to_next_level:  # Level up as many times as possible
            self.level_up()
            
    def level_up(self):
        self.level += 1
        self.xp -= self.xp_to_next_level  # Subtract the XP needed for the last level
        self.xp_to_next_level *= 2  # Double the XP needed for the next level
        self.stats.max_health += 10 # Increase max health by 10
        self.stats.health = self.stats.max_health
        self.stats.strength += 1  # Increase attack by 1
    
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

    def collision_handler(self, direction):
        hits_blocks = pygame.sprite.spritecollide(self, self.game.blocks, False)
        hits_enemies = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if direction == "x":
            if hits_blocks:
                if self.x_change > 0:
                    self.rect.x = hits_blocks[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits_blocks[0].rect.right
                self.x_change = 0
            if hits_enemies:
                if self.x_change > 0:
                    self.rect.x = hits_enemies[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits_enemies[0].rect.right
                self.x_change = 0
        if direction == "y":
            if hits_blocks:
                if self.y_change > 0:
                    self.rect.y = hits_blocks[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits_blocks[0].rect.bottom
                self.y_change = 0
            if hits_enemies:
                if self.y_change > 0:
                    self.rect.y = hits_enemies[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits_enemies[0].rect.bottom
                self.y_change = 0
        self.y = self.rect.y

        
        
    def animate(self):
        now = pygame.time.get_ticks()
        down_animations = [self.game.character_spritesheet.getSprite(0, 0, self.width, self.height),
                           self.game.character_spritesheet.getSprite(32, 0, self.width, self.height),
                           self.game.character_spritesheet.getSprite(64, 0, self.width, self.height)]
        up_animations = [self.game.character_spritesheet.getSprite(0, 96, self.width, self.height),
                            self.game.character_spritesheet.getSprite(32, 96, self.width, self.height),
                            self.game.character_spritesheet.getSprite(64, 96, self.width, self.height)]
        left_animations = [self.game.character_spritesheet.getSprite(0, 32, self.width, self.height),
                            self.game.character_spritesheet.getSprite(32, 32, self.width, self.height),
                            self.game.character_spritesheet.getSprite(64, 32, self.width, self.height)]
        right_animations = [self.game.character_spritesheet.getSprite(0, 64, self.width, self.height),
                            self.game.character_spritesheet.getSprite(32, 64, self.width, self.height),
                            self.game.character_spritesheet.getSprite(64, 64, self.width, self.height)]
        
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
                