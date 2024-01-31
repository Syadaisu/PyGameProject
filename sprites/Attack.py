import pygame
from config import *

class Attack(pygame.sprite.Sprite):
    def __init__(self,game,x,y, damage):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites, game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.damage = self.game.player.stats.strength
        self.x = x
        self.y = y
        self. width = TILESIZE
        self.height = TILESIZE
        
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.animate_speed = 30
        
        self.image = self.game.attack_spritesheet.getSprite(0, 0, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def update(self):
        self.animate()
        self.collide()
        
    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        for enemy in hits:
            enemy.health -= self.damage
            if enemy.health <= 0:
                self.game.player.gold += enemy.gold  # Increase the player's gold
                self.game.player.xp += enemy.xp  # Increase the player's xp
                enemy.kill()
        
    def animate(self):
        now = pygame.time.get_ticks()
        direction = self.game.player.facing
        
        right_animations = [self.game.attack_spritesheet.getSprite(0, 64, self.width, self.height),
                           self.game.attack_spritesheet.getSprite(32, 64, self.width, self.height),
                           self.game.attack_spritesheet.getSprite(64, 64, self.width, self.height),
                           self.game.attack_spritesheet.getSprite(96, 64, self.width, self.height),
                           self.game.attack_spritesheet.getSprite(128, 64, self.width, self.height)]

        down_animations = [self.game.attack_spritesheet.getSprite(0, 32, self.width, self.height),
                           self.game.attack_spritesheet.getSprite(32, 32, self.width, self.height),
                           self.game.attack_spritesheet.getSprite(64, 32, self.width, self.height),
                           self.game.attack_spritesheet.getSprite(96, 32, self.width, self.height),
                           self.game.attack_spritesheet.getSprite(128, 32, self.width, self.height)]

        left_animations = [self.game.attack_spritesheet.getSprite(0, 96, self.width, self.height),
                           self.game.attack_spritesheet.getSprite(32, 96, self.width, self.height),
                           self.game.attack_spritesheet.getSprite(64, 96, self.width, self.height),
                           self.game.attack_spritesheet.getSprite(96, 96, self.width, self.height),
                           self.game.attack_spritesheet.getSprite(128, 96, self.width, self.height)]

        up_animations = [self.game.attack_spritesheet.getSprite(0, 0, self.width, self.height),
                         self.game.attack_spritesheet.getSprite(32, 0, self.width, self.height),
                         self.game.attack_spritesheet.getSprite(64, 0, self.width, self.height),
                         self.game.attack_spritesheet.getSprite(96, 0, self.width, self.height),
                         self.game.attack_spritesheet.getSprite(128, 0, self.width, self.height)]
        
        if now - self.last_update > self.animate_speed:  # Time to update the frame
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % 5  # Assuming you have 5 frames for each direction

            if direction == 'up':  # Moving up
                self.image = up_animations[self.current_frame]
                if self.current_frame == 4:
                    self.kill()
            elif direction == 'down':  # Moving down
                self.image = down_animations[self.current_frame]
                if self.current_frame == 4:
                    self.kill()
            elif direction == 'left':  # Moving left
                self.image = left_animations[self.current_frame]
                if self.current_frame == 4:
                    self.kill()
            elif direction == 'right':  # Moving right
                self.image = right_animations[self.current_frame]
                if self.current_frame == 4:
                    self.kill()
