import pygame
from state.Button import Button_
from state.constant import constant

# Load Font for load screen
font_30 = pygame.font.Font("resources\font\Dragon Slayer.py", 30)
font_40 = pygame.font.Font("resources\font\Dragon Slayer.py", 40)

# Load Image for button
img_btn_Hide = pygame.image.load("resources\img\BTN_Hide.png")
img_btn_Show = pygame.image.load("resources\img\BTN_Show.png")

img_btn_Vol_Off = pygame.image.load("resources\img\BTN_Vol_Off.png")
img_btn_Vol_On = pygame.image.load("resources\img\BTN_Vol_On.png")

# define Button Global
btn_Play = Button_()
btn_Exit = Button_()
btn_Vol = Button_()


def Create_button():
    pass


def Change_Vol():
    pass


def Draw_Text():
    pass


def Load_Screen():
    pass
