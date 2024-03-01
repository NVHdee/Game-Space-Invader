__author__= "NVHA"

import pygame
import random

alien_group = pygame.sprite.Group()

# Create Random Address image Aliens
def random_add_img(val_start,val_end):
    return "resources/img/alien_spaceship/"+str(random.randint(val_start,val_end))+".png"

# Class Aliens
class Aliens(pygame.sprite.Sprite):
    def __init__(self, rect_x, rect_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(random_add_img(1,4))
        self.rect = self.image.get_rect()
        self.rect.center = [rect_x, rect_y]
        self.move_counter = 0
        self.move_direction = 1
    # Update Location of Object
    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 75:
            self.move_direction *= -1
            self.move_counter *= self.move_direction