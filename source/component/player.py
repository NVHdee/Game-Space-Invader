import pygame
from ..constant import c
from .bullets import Bullets
from .explosion import Explosion

# Class SpaceShip
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, health,scr):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("resources/img/alien_spaceship/spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_remaining = health
        self.last_shot = pygame.time.get_ticks()
        self.screen = scr
    def update(self):
        # set movement speed
        speed = 8
        # set a cooldown variable
        cooldown = 500  # milliseconds
        game_over = 0

        # get key press
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < c.screen_width:
            self.rect.x += speed

        # record current time
        time_now = pygame.time.get_ticks()
        # shoot
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            c.laser_fx.play()
            bullet = Bullets(self.rect.centerx, self.rect.top)
            c.bullet_group.add(bullet)
            self.last_shot = time_now

        # update mask
        self.mask = pygame.mask.from_surface(self.image)

        # draw health bar
        pygame.draw.rect(
            self.screen, c.red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15)
        )
        if self.health_remaining > 0:
            pygame.draw.rect(
                self.screen,
                c.green,
                (
                    self.rect.x,
                    (self.rect.bottom + 10),
                    int(self.rect.width * (self.health_remaining / self.health_start)),
                    15,
                ),
            )
        elif self.health_remaining <= 0:
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            c.explosion_group.add(explosion)
            self.kill()
            game_over = -1
        return game_over
