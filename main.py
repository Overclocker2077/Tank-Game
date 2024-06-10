from settings import *
from loader import init_loader, Tank_Image_Loader

class Button(pygame.sprite.Sprite):   # surface, group, x, y, image, image2=None, swap=True
    def __init__(self, group, x, y, image, image2=None):
        super().__init__(group)   # Add this class to a sprite group
        self.image = image
        self.rect1 = self.image.get_rect()
        self.rect = self.rect1
        self.rect.center = (x, y)
        self.center = (x, y)
        self.topleft = self.rect.topleft
        self.image2 = image2 
        
        if self.image2:
            self.orig_image = self.image
            self.rect2 = self.image2.get_rect()
            self.rect2.center = (x,y)

    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.image2:
            if not self.isHovering(mouse_x, mouse_y):
                self.image = self.orig_image
                self.rect = self.rect1
            else:
                self.image = self.image2
                self.rect = self.rect2

    def isHovering(self, mouse_x, mouse_y):
        return self.topleft[0] < mouse_x and self.topleft[0] + self.rect.width > mouse_x and self.topleft[1] < mouse_y and self.topleft[1] + self.rect.height > mouse_y

class Tile(pygame.sprite.Sprite):   # groups, surf, pos
    def __init__(self, groups, surf, pos):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.orignal_center = self.rect.center
    
    def update(self, offset):
        self.rect.center = (self.orignal_center[0] + offset[0], self.orignal_center[1] + offset[1])

class Text(pygame.sprite.Sprite):     #  group, text, x, y, font, color
    def __init__(self, group, text, x, y, font, color):
        super().__init__(group)
        self.image = font.render(text, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class WallPaperCycle(pygame.sprite.Sprite):  # groupm image_list
    def __init__(self, group, image_list):
        super().__init__(group)
        self.image_list = image_list
        self.image_index = 1
        self.image = self.image_list[f"{self.image_index}.jpg"]
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,0)
        
    def update_img(self):
        self.image_index += 1 
        if self.image_index > num_of_images:
            self.image_index = 1
        self.image = self.image_list[f"{self.image_index}.jpg"]

class M1_Abrem_Tank(pygame.sprite.Sprite):   #  group, name, body_image, turet_image, pos (Tuple)
    def __init__(self, group, name, body_image, turret_image, pos):
        super().__init__(group)
        self.image = body_image
        self.rect = body_image.get_rect()
        self.rect.center = pos
        self.turret_image = turret_image
        self.turret_pos = (pos[0]-100, pos[1]+70)
        self.turret_image_rect = turret_image.get_rect(center = self.turret_pos)
        self.front = -1
        self.vertical = True

    def update2(self, direction):
        n = 90
        if Direction.RIGHT == direction and self.vertical:
            self.vertical = False
            self.image = pygame.transform.rotate(self.image, n*self.front)  # Neg
            self.front = 1

        elif Direction.LEFT == direction and self.vertical:
            self.vertical = False
            self.image = pygame.transform.rotate(self.image, -n*self.front)  # Pos
            self.front = -1

        elif Direction.UP == direction and not self.vertical:
            self.vertical = True
            self.image = pygame.transform.rotate(self.image, n*self.front)   # Neg
            self.front = -1
        
        elif Direction.DOWN == direction and not self.vertical:
            self.vertical = True
            self.image = pygame.transform.rotate(self.image, -n*self.front)   
            self.front = 1
        
        if not self.vertical:
            self.turret_image_rect.center = (self.turret_image_rect.centerx - 30, self.turret_image_rect.centery - 30)

class ExtendedCameraGroup(pygame.sprite.Group):  # Custom update method for sprite groups
    def __init__(self):
        super().__init__()
    def update2(self, offset):
        for sprite in self.sprites():
            sprite.update(offset)

class ExtendedPlayerGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
    
    def custom_draw(self, surface):
        for sprite in self.sprites():
            surface.blit(sprite.image, sprite.rect.center)  # Dispay the body of the Tank
            surface.blit(sprite.turret_image, sprite.turret_image_rect.center)  # Display the turret

    def update2(self, direction):
        for sprite in self.sprites():
            sprite.update2(direction)

class Music_Player:  # Music_Files
    def __init__(self, Music_Files):
        self.Music_Files = Music_Files
        pygame.mixer.music.load(f"{game_music}\\{self.Music_Files[0]}")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play()

class Camera:  # Group
    def __init__(self, groups, player):
        self.groups = groups
        self.player = player
        self.offset = pygame.math.Vector2()
        self.rect = pygame.Rect(0,0, window_width/2, window_height/2)
        self.rect.center = player.rect.center

    def update(self, direction):
        # Update Offset
        self.rect.center = (self.rect.centerx + direction[0], self.rect.centery + direction[1])
        self.offset.x -= direction[0]
        self.offset.y += direction[1]

        # Apply Offset
        self.groups.update2(self.offset)

class Game:
    def __init__(self):
        self.screen = screen 
        self.clock =  clock
        self.window_width = window_width
        self.window_height = window_height
        self.running = True
        self.current_game_state = GameState.MENU
        self.player_team = False  # False -> Ukraine, True -> Russia
        # Load data
        self.menu_images, self.menu_buttons, self.Fonts, self.Music_Files, self.tmx_data = init_loader(self.window_width, self.window_height)  
        
        # Play Music
        self.music_class = Music_Player(self.Music_Files)
        
        # Groups
        self.camera_group = pygame.sprite.Group()
        self.game_sprites = ExtendedCameraGroup()
        self.menu_sprites = pygame.sprite.Group()
        self.player_group = ExtendedPlayerGroup()

        # Initialize Menu Sprites
        self.init_menu()

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False
                self.event_handler(event)
            # Update 
            #self.all_sprites.update(dt)
                
            self.update()
            self.render()
            
            # Draw to the surface
            #self.all_sprites.draw(self.display_surface)
            pygame.display.update()

        self.clock.tick(60)
        pygame.quit()
    
    ### Game State and events ###
    def event_handler(self, event):  # Run the input functions for a given event
        if self.current_game_state == GameState.MENU:
            self.menu_events(event)
        if self.current_game_state == GameState.GAMEPLAY:
            self.game_events(event)
    
    def update(self):
        if self.current_game_state == GameState.MENU:
            self.menu_sprites.update()
        if self.current_game_state == GameState.GAMEPLAY:
            moveBy = 2
            direction = 0
            if self.keyHold[0]:
                if self.keyHold[1] == pygame.K_w:
                    self.camera.update((0,moveBy))
                    direction = Direction.UP
                elif self.keyHold[1] == pygame.K_d:
                    self.camera.update((moveBy, 0))
                    direction = Direction.RIGHT
                elif self.keyHold[1] == pygame.K_a:
                    self.camera.update((-moveBy, 0))
                    direction = Direction.LEFT
                elif self.keyHold[1] == pygame.K_s:
                    self.camera.update((0, -moveBy)) 
                    direction = Direction.DOWN
                self.player_group.update2(direction)
            self.game_sprites.update2(self.camera.offset)

    def render(self):
        if self.current_game_state == GameState.MENU:
            self.render_menu()
        if self.current_game_state == GameState.GAMEPLAY:
            self.render_game()
    
    def game_events(self, event):
        if event.type == pygame.KEYUP:
            self.keyHold[0] = False
            self.keyHold[1] = None

        elif event.type == pygame.KEYDOWN:
            self.keyHold[0] = True
            self.keyHold[1] = event.key 

    def render_game(self):
        self.screen.fill("Dark Green")
        self.game_sprites.draw(self.screen)
        self.player_group.custom_draw(self.screen)

    def init_game(self):
        self.keyHold = [False, None]
        for layer in self.tmx_data.layers:
            if hasattr(layer, "data"):
                for x,y, surf in layer.tiles():
                    pos = (x * 88, y * 88)
                    Tile(self.game_sprites, surf, pos)
        tank_dict = Tank_Image_Loader()
        if self.player_team:
            self.Player = M1_Abrem_Tank(self.player_group, "M1 Abrem", tank_dict["M1 Tank Body.png"], tank_dict["M1 Tank Turret.png"],
                                        (window_width/2-(tank_size[0]/2),window_height/2-(tank_size[1]/2)))
        else:
            self.Player = M1_Abrem_Tank(self.player_group, "T-62AG Tank", tank_dict["T-62AG Tank Body.png"], tank_dict["T-62AG Tank Turret.png"],
                            (window_width/2-(tank_size[0]/2),window_height/2-(tank_size[1]/2)))
            
        self.camera = Camera(self.game_sprites, self.Player)

    def menu_events(self, event):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.type == WALL_PAPER_EVENT:
            self.wall_paper.update_img()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.quit_button.isHovering(mouse_x, mouse_y):
                self.running = False 
            elif self.ukraine_button.isHovering(mouse_x, mouse_y):
                self.current_game_state = GameState.GAMEPLAY
                pygame.event.clear()
                self.player_team = True
                self.init_game()
            elif self.russian_button.isHovering(mouse_x, mouse_y):
                self.current_game_state = GameState.GAMEPLAY
                pygame.event.clear()
                self.init_game()

    def render_menu(self):
        self.screen.fill((0, 0, 0))
        self.menu_sprites.draw(self.screen)
    
    #############################

    # Set up and initialize all the classes needed for the main menu screen
    def init_menu(self):
        pygame.time.set_timer(WALL_PAPER_EVENT, 12000)
        self.wall_paper = WallPaperCycle(self.menu_sprites, self.menu_images)
        self.Menu_text = Text(self.menu_sprites, "Russo-Ukrainian War", self.window_width/2, self.window_height/2-300, self.Fonts["turok"], (0,0,0))
        self.quit_button = Button(self.menu_sprites, self.window_width / 2, self.window_height / 2 + 300,
                                     self.menu_images[self.menu_buttons[0]], image2=self.menu_images[self.menu_buttons[1]])  # Quit Button
        self.ukraine_button = Button(self.menu_sprites, self.window_width / 2, self.window_height / 2 - 100,
                                     self.menu_images[self.menu_buttons[2]])  # Ukraine
        self.russian_button = Button(self.menu_sprites, self.window_width / 2, self.window_height / 2 + 100,
                                     self.menu_images[self.menu_buttons[3]])  # Russia


if __name__ == "__main__":
    game = Game()
    game.run()
