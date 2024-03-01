__author__= "NVHA"

import pygame 
from ..constant import c
from .explosion import Explosion
# Class Bullets
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("resources/img/bullet/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, c.alien_group, True):
            self.kill()
            c.explosion_fx.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            c.explosion_group.add(explosion)
