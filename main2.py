import pygame
from settings import *
from loader import init_loader


class Button(pygame.sprite.Sprite):
    def __init__(self, surface, group, x, y, image, image2=None, swap=True):
        super().__init__(group)  # Add this class to a sprite group
        self.orig_image = image
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.topleft = (x, y)
        self.image2 = image2
        self.swap = swap
        self.surface = surface

    def update(self):
        if self.swap:
            self.image = self.orig_image
            self.rect = self.image.get_rect()
        elif self.image2:
            self.image = self.image2
            self.rect = self.image.get_rect()

    def isHovering(self, mouse_x, mouse_y):
        return self.topleft[0] < mouse_x < self.topleft[0] + self.rect.width and self.topleft[1] < mouse_y < self.topleft[1] + self.rect.height


class Tank(pygame.sprite.Sprite):
    def __init__(self, group, name, body_image, turret_image):
        super().__init__(group)
        # Tank initialization code here


class WallPaperCycle(pygame.sprite.Sprite):
    def __init__(self, group, image_list):
        super().__init__(group)
        self.image_list = image_list
        self.image_index = 1
        self.image = self.image_list[f"{self.image_index}.jpg"]
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)

    def update_img(self):
        self.image_index += 1
        if self.image_index > num_of_images:
            self.image_index = 1
        self.image = self.image_list[self.image_index]


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.window_width, self.window_height = self.screen.get_size()
        self.running = True
        self.current_game_state = GameState.MENU
        # Load data
        self.menu_images, self.menu_buttons, self.Fonts, self.Music, self.map_image = init_loader(self.window_width, self.window_height)
        # Groups
        self.camera_group = pygame.sprite.Group()
        self.game_sprites = pygame.sprite.Group()
        self.menu_sprites = pygame.sprite.Group()
        self.menu_list = []

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
            self.update()
            self.render()

            pygame.display.update()

        pygame.quit()

    def event_handler(self, event):
        if self.current_game_state == GameState.MENU:
            self.menu_events(event)

    def update(self):
        if self.current_game_state == GameState.MENU:
            self.menu_sprites.update()

    def render(self):
        if self.current_game_state == GameState.MENU:
            self.render_menu()

    def menu_events(self, event):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.menu_list[0].isHovering(mouse_x, mouse_y):
            self.menu_list[0].swap = False
        else:
            self.menu_list[0].swap = True
        if event.type == WALL_PAPER_EVENT:
            self.wall_paper.update_img()

    def render_menu(self):
        self.screen.fill((0, 0, 0))  # Clear screen with black
        self.menu_sprites.draw(self.screen)
        print("Rendering menu...")

    def init_menu(self):
        self.menu_list.append(Button(self.screen, self.menu_sprites, self.window_width / 2, self.window_height / 2,
                                     self.menu_images[self.menu_buttons[0]], image2=self.menu_images[self.menu_buttons[1]]))  # Quit Button
        self.menu_list.append(Button(self.screen, self.menu_sprites, self.window_width / 2, self.window_height / 2 - 100,
                                     self.menu_images[self.menu_buttons[2]]))  # Ukraine
        self.menu_list.append(Button(self.screen, self.menu_sprites, self.window_width / 2, self.window_height / 2 - 100,
                                     self.menu_images[self.menu_buttons[3]]))  # Russia
        self.wall_paper = WallPaperCycle(self.menu_sprites, self.menu_images)

    def init_game(self):
        pass


if __name__ == "__main__":
    game = Game()
    game.run()
