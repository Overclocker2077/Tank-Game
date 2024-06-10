import pygame
from pytmx.util_pygame import load_pygame

pygame.init()
screen = pygame.display.set_mode((1000,800))
tmx_data = load_pygame("Game_Art\\Maps\\Map1.tmx")

# print(tmx_data.layers)
# layer = tmx_data.get_layer_by_name("Tile Layer 1")

# for x,y, surf in layer.tiles():
#     print(x * 88, y * 88 , surf)

# print(layer.data)

# print(layer.id)

# Get Objects
object_Layer = tmx_data.get_layer_by_name("Object Layer 1")
# print(object_Layer)
for obj in object_Layer:
    print(obj)

# for obj in tmx_data.objectgroups:
#     print(obj)

# Get tiles 
layer = tmx_data.get_layer_by_name("Tile Layer 1")
 
# for tile in layer.tiles():
#     print(tile)

class Tile(pygame.sprite.Sprite):
    def __init__(self, groups, surf, pos):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)

sprite_group = pygame.sprite.Group()

# Cycle through all layers
for layer in tmx_data.layers:
    if hasattr(layer, "data"):
        for x,y, surf in layer.tiles():
            pos = (x * 88, y * 88)
            Tile(sprite_group, surf, pos)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    screen.fill("Dark Green")
    sprite_group.draw(screen)
    pygame.display.update()
pygame.quit()
