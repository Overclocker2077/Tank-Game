import pygame
from random import randint
from os import walk
from pytmx.util_pygame import load_pygame

pygame.init()

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

clock = pygame.time.Clock() 

window_width, window_height = screen.get_size()
# Game Values
num_of_images = 17
count = 0
map_scale_factor = 1
game_art = "Game_Art"
menu_art = f"{game_art}\\Menu Screen"
russian_art = f"{game_art}\\Russian"
Ukraine_art = f"{game_art}\\ukraine"
game_music = "Game_Music"
flag_scale = (250, 150)
quit_button_scale = (250, 100)
tank_size = (150,250)
turret_size = (250, 120)

# Custom Events
WALL_PAPER_EVENT = pygame.event.custom_type()

class Color:
    GREY = (128, 128, 128)

class GameState():
    MENU = 0
    GAMEPLAY = 1
    PAUSE = 2
    GAME_OVER = 3

class Direction:
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4



# class Button(pygame.sprite.Group):   # surface, group, x, y, image, image2=None, swap=True
#     def __init__(self, surface, group, x, y, image, image2=None, swap=True):
#         super().__init__(group)   # Add this class to a sprite group
#         self.image = image
#         self.rect = self.image.get_rect()
#         self.rect.topleft = (x, y)
#         self.topleft = (x, y)
#         self.image2 = image2 
#         self.swap = swap
#         self.surface = surface

#     def draw(self):
#         if self.swap:
#             self.surface.blit(self.image, (self.rect.x, self.rect.y))
#         elif self.image2 != None:
#             self.surface.blit(self.image2, (self.rect.x, self.rect.y))

#     def isHovering(self, mouse_x, mouse_y):
#         if self.topleft[0] < mouse_x and self.topleft[0] + self.rect.width > mouse_x and self.topleft[1] < mouse_y and self.topleft[1] + self.rect.height > mouse_y:
#             return True
#         return False
