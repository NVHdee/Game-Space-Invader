author= "NVHA"
import pygame

__name__ = "__main__"

# Fps
clock = pygame.time.Clock()
fps = 60

#Size Screem
screen_width = 600
screen_height = 800

# Fonts
font30 = pygame.font.Font("font\\Fussion-3zgAz.ttf", 30)
font40 = pygame.font.Font("font\\Dragon Slayer.ttf", 40)
font20 = pygame.font.Font("font\\Fussion-3zgAz.ttf", 20)
# Load Font
font_btn = pygame.font.Font("font\\Fussion-3zgAz.ttf", 30)
font_title = pygame.font.Font("font\\Dragon Slayer.ttf", 75)

# Load Sound and SFX
#Explosion
explosion_fx = pygame.mixer.Sound("mus\\explosion.wav")
explosion_fx.set_volume(0.25)

explosion2_fx = pygame.mixer.Sound("mus\\explosion2.wav")
explosion2_fx.set_volume(0.25)

#Laser
laser_fx = pygame.mixer.Sound("mus\\laser.wav")
laser_fx.set_volume(0.25)

#Load_screen
main_fx = pygame.mixer.Sound("mus\\SoundTrack_Main.mp3")
main_fx.set_volume(0.75)

#Main menu
play_fx = pygame.mixer.Sound("mus\\SoundTrack_Play.mp3")
play_fx.set_volume(0.75)

#Button
button_click_fx = pygame.mixer.Sound("mus\\btn_click.mp3")
button_click_fx.set_volume(0.5)
vol_status = True

# Define amount aliens create 
rows = 5
cols = 5

# screen countdown
countdown = 3
last_count = pygame.time.get_ticks()

# bullet countdown
alien_countdown = 1000
last_alien_shot = pygame.time.get_ticks()

# Status Game
game_over = 0  # 0: no game over, 1: player has won, -1: player has lost

# Define Colors
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)

# Load Image
#Background
bg = pygame.image.load("img/bg.png").convert_alpha()
#Button
btn_show_img = pygame.image.load("img/BTN_Show.png").convert_alpha()
btn_hide_img = pygame.image.load("img/BTN_Hide.png").convert_alpha()
btn_vol_on_img = pygame.image.load("img/BTN_Vol_On.png").convert_alpha()
btn_vol_off_img = pygame.image.load("img/BTN_Vol_Off.png").convert_alpha()

# Construct Object
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()