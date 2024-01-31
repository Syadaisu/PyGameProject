import pygame
from config import *

class Attack(pygame.sprite.Sprite):
    def __init__(self,game,x,y, damage, layer, group):
        self.game = game
        self._layer = layer
        self.groups = game.all_sprites, group
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.damage = damage
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
        # For enemies
        self.collide_with_group(self.game.enemies)

        # For players
        self.collide_with_sprite(self.game.player)
        
    def collide_with_group(self, target_group):
        hits = pygame.sprite.spritecollide(self, target_group, False)
        for target in hits:
            self.handle_collision(target)
            
    def collide_with_sprite(self, target):
        if pygame.sprite.collide_rect(self, target):
            self.handle_collision(target)
            
    def handle_collision(self, target):
        from sprites.Enemy import Enemy  # Import inside function

        # If the target is the same as the attacker, don't apply any damage
        if target == self.attacker:
            return

        target.stats.health -= self.damage
        if target.stats.health <= 0:
            if isinstance(target, Enemy):
                self.game.inventory.add_item('Gold', target.gold)  # Increase the player's gold
                self.game.player.gain_xp(target.xp)  # Increase the player's xp
            target.kill()
        
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
