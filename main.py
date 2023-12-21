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
        self.intro = True
        self.options=False
        self.font = pygame.font.Font("assets/font.ttf", 32)
        self.character_spritesheet = Spritesheet("assets/character.png")
        self.terrain_spritesheet = Spritesheet("assets/terrain.png")
        self.intro_background = pygame.transform.scale(pygame.image.load("assets/background.png"), (WIDTH, HEIGHT))

    def createTilemap(self):
        for i,row in enumerate(tilemap):
            for j,column in enumerate(row):
                Ground(self, j, i)
                if column == 'B':
                    Block(self, j, i)
                if column == 'P':
                    Player(self, j, i)

    def new(self):
        self.playing = True
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
        print(self.intro)
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

            print (mouse_pos)
            print (mouse_pressed)
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

    def main_menu(self):
        while self.playing:
            self.events()
            self.draw()
            self.update()
        self.running = False




g = Game()
while g.intro:
    g.intro_screen()
    if g.options:
        g.options_screen()
g.new()
while g.running:
    g.main_menu()
    g.game_over()

pygame.quit()
sys.exit()
