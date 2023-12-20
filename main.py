import pygame
from sprites import *
from config import *
import sys


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Game")
        self.clock = pygame.time.Clock()
        self.running = True

    def createTilemap(self):
        for i,row in enumerate(tilemap):
            for j,column in enumerate(row):
                if column == 'B':
                    Block(self, j, i)
                if column == 'P':
                    Player(self, j, i)
                    print(j,i)

    def new(self):
        self.playing=True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.buildings = pygame.sprite.LayeredUpdates()
        self.createTilemap()

    def update(self):
        self.all_sprites.update()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def draw(self):
        self.screen.fill("black")
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def intro_screen(self):
        pass

    def game_over(self):
        pass

    def main_menu(self):
        while self.playing:
            self.events()
            self.draw()
            self.update()
        self.running = False




g=Game()
g.intro_screen()
g.new()
while g.running:
    g.main_menu()
    g.game_over()

pygame.quit()
sys.exit()
