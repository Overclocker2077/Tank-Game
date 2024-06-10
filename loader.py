from settings import *

im_im = pygame.image.load

# Load art Fonts and Music
def init_loader(window_width, window_height):
    
    # import image 
    
    # Load Menu images
    menu_images = {}
    # menu_buttons = [im_im(f"{menu_art}\\quit_button_black.png").convert(), im_im(f"{menu_art}\\quit_button_yellow.png").convert(),
    #                 im_im(f"{menu_art}\\UkrainianButton.png").convert(), im_im(f"{menu_art}\\RussianButton.png").convert()]
    menu_buttons = ["quit_button_black.png", "quit_button_yellow.png", "UkrainianButton.png", "RussianButton.png"]
    # Variables to load other stuff, Font, Music, Map etc
    Music_Files = []
    map_image =  im_im("Game_Art\\map.jpg")
    pygame.mixer.init()
    Fonts = {}

    # Load two fonts
    Fonts["turok"] = pygame.font.Font('turok.ttf', 130, bold = True)
    Fonts["SysFont"] = pygame.font.SysFont(None, 150, bold=True)

    # Load Menu images
    for dirpath, dirnames, filenames in walk(menu_art):
        for filename in filenames:
            img = pygame.image.load(f"{dirpath}\\{filename}").convert()
            if "quit" in filename:
                menu_images[filename] = pygame.transform.scale(img, quit_button_scale)
            elif "RussianButton.png" == filename or "UkrainianButton.png" == filename:
                menu_images[filename] = pygame.transform.scale(img, flag_scale)
            else:
                menu_images[filename] = pygame.transform.scale(img, (window_width, window_height))
       
    # Load music
    for dirpath, dirnames, filenames in walk(game_music):
        for filename in filenames:    
            Music_Files.append(filename)
    
    tmx_data = load_pygame("Game_Art\\Maps\\Map1\\Map1.tmx")

    return menu_images, menu_buttons, Fonts, Music_Files, tmx_data


def Tank_Image_Loader():
    tank_dict = {}   # Key: List[0] = Body, List[1] = Turret
    for dirpath, dirnames, filenames in walk("Game_Art\\Tanks"):
        for filename in filenames:
            if "Turret" in filename:
                tank_dict[filename] = pygame.transform.scale(im_im(f"{dirpath}\\{filename}"), turret_size)
            else:
                tank_dict[filename] = pygame.transform.scale(im_im(f"{dirpath}\\{filename}"), tank_size)
    return tank_dict
