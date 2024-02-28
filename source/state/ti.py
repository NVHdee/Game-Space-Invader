# Space Invaders
import pygame, time
from pygame import mixer
from pygame.locals import *
import random
import sys

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()
# Fps
clock = pygame.time.Clock()
fps = 60

screen_width = 600
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invanders!")

# Fonts
font30 = pygame.font.Font("font\\Fussion-3zgAz.ttf", 30)
font40 = pygame.font.Font("font\\Dragon Slayer.ttf", 40)
font20 = pygame.font.Font("font\\Fussion-3zgAz.ttf", 20)
# Load Font
font_btn = pygame.font.Font("font\\Fussion-3zgAz.ttf", 30)
font_title = pygame.font.Font("font\\Dragon Slayer.ttf", 75)

# Load Sound and SFX
explosion_fx = pygame.mixer.Sound("mus\\explosion.wav")
explosion_fx.set_volume(0.25)

explosion2_fx = pygame.mixer.Sound("mus\\explosion2.wav")
explosion2_fx.set_volume(0.25)

laser_fx = pygame.mixer.Sound("mus\\laser.wav")
laser_fx.set_volume(0.25)

main_fx = pygame.mixer.Sound("mus\\SoundTrack_Main.mp3")
main_fx.set_volume(0.75)

play_fx = pygame.mixer.Sound("mus\\SoundTrack_Play.mp3")
play_fx.set_volume(0.75)

button_click_fx = pygame.mixer.Sound("mus\\btn_click.mp3")
button_click_fx.set_volume(0.5)
vol_status = True

# Define game variables
rows = 5
cols = 5

# bullet countdown
alien_countdown = 1000
last_alien_shot = pygame.time.get_ticks()

# screen countdown
countdown = 3
last_count = pygame.time.get_ticks()

# Status Game
game_over = 0  # 0: no game over, 1: player has won, -1: player has lost

# Define Colors
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)

# Load Image
bg = pygame.image.load("img/bg.png").convert_alpha()
show_img = pygame.image.load("img/BTN_Show.png").convert_alpha()
hide_img = pygame.image.load("img/BTN_Hide.png").convert_alpha()
vol_on_img = pygame.image.load("img/BTN_Vol_On.png").convert_alpha()
vol_off_img = pygame.image.load("img/BTN_Vol_Off.png").convert_alpha()

# Construc Obj
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()


def draw_bg():
    screen.blit(bg, (0, 0))


# Def_func for create_Text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# Class SpaceShip
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_remaining = health
        self.last_shot = pygame.time.get_ticks()

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
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += speed

        # record current time
        time_now = pygame.time.get_ticks()
        # shoot
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            laser_fx.play()
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_shot = time_now

        # update mask
        self.mask = pygame.mask.from_surface(self.image)

        # draw health bar
        pygame.draw.rect(
            screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15)
        )
        if self.health_remaining > 0:
            pygame.draw.rect(
                screen,
                green,
                (
                    self.rect.x,
                    (self.rect.bottom + 10),
                    int(self.rect.width * (self.health_remaining / self.health_start)),
                    15,
                ),
            )
        elif self.health_remaining <= 0:
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            explosion_group.add(explosion)
            self.kill()
            game_over = -1
        return game_over


# Class Bullets
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, alien_group, True):
            self.kill()
            explosion_fx.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_group.add(explosion)


# Class Aliens
class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/alien" + str(random.randint(1, 5)) + ".png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_direction = 1

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 75:
            self.move_direction *= -1
            self.move_counter *= self.move_direction


# Class Alien_Bullets
class Alien_Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/alien_bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self, spaceship):
        self.rect.y += 2
        if self.rect.top > screen_height:
            self.kill()
        if pygame.sprite.spritecollide(
            self, spaceship_group, False, pygame.sprite.collide_mask
        ):
            self.kill()
            explosion2_fx.play()
            # reduce spaceship health
            spaceship.health_remaining -= 1
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            explosion_group.add(explosion)


# Class Explosion
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f"img/exp{num}.png")
            if size == 1:
                img = pygame.transform.scale(img, (20, 20))
            if size == 2:
                img = pygame.transform.scale(img, (40, 40))
            if size == 3:
                img = pygame.transform.scale(img, (160, 160))
            # add the image to the list
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 3
        # update explosion animation
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        # if the animation is complete, delete explosion
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()


# Load Image
def Load_Image(image, size, scr, pos):
    image = pygame.transform.scale(image, (int(size[0]), int(size[1])))
    scr.blit(image, (int(pos[0]), int(pos[1])))


# Class Button
class Button_:
    def __init__(
        self,
        image_hide,
        image_show,
        pos,
        text_input,
        font,
        base_color,
        hovering_color,
        scale,
    ):
        self.image_hide = pygame.transform.scale(
            image_hide,
            (int(image_hide.get_width() * scale), int(image_hide.get_height() * scale)),
        )
        self.image_show = pygame.transform.scale(
            image_show,
            (int(image_show.get_width() * scale), int(image_show.get_height() * scale)),
        )
        self.scale = scale
        self.image = self.image_hide
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text

        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    # Draw Button
    def draw_btn(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_Colision(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[
            1
        ] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def change_Statue(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[
            1
        ] in range(self.rect.top, self.rect.bottom):
            # Change Size, Pos and Color Text
            self.text = self.font.render(self.text_input, True, self.hovering_color)
            self.text_rect = self.text.get_rect(center=(self.x_pos + 2, self.y_pos - 5))
            # Change size and Pos Image
            image = self.image_show
            image = pygame.transform.scale(
                image,
                (
                    int(self.image_show.get_width() * (self.scale - 0.025)),
                    int(self.image_show.get_height() * (self.scale - 0.025)),
                ),
            )
            self.image = image
            self.rect = self.image.get_rect(center=(self.x_pos + 2, self.y_pos - 5))
        else:
            # Set Default Text
            self.text = self.font.render(self.text_input, True, self.base_color)
            self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
            # Set Default Image
            self.image = self.image_hide
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    # Change Image
    def change_img(self, status):
        if status:
            self.image = self.image_hide
        else:
            self.image = self.image_show


# Initialize Button Use
btn_vol = Button_(
    image_hide=vol_on_img,
    image_show=vol_off_img,
    pos=(550, 30),
    text_input="",
    font=font20,
    base_color="#F5F5DC",
    hovering_color="white",
    scale=0.2,
)
btn_start = Button_(
    image_hide=hide_img,
    image_show=show_img,
    pos=(300, 380),
    text_input="START",
    font=font20,
    base_color="#F5F5DC",
    hovering_color="#00FF7F",
    scale=0.9,
)
btn_Exit = Button_(
    image_hide=hide_img,
    image_show=show_img,
    pos=(300, 520),
    text_input="EXIT",
    font=font20,
    base_color="#F5F5DC",
    hovering_color="#00FF7F",
    scale=0.9,
)


# Create The Aliens
def create_aliens():
    for row in range(rows):
        for item in range(cols):
            alien = Aliens(100 + item * 100, 100 + row * 70)
            alien_group.add(alien)


# Craete Button Screen Menu
def create_btn_menu(status):
    draw_bg()
    title = font40.render("Space Invader", True, "#FF7F50")
    draw_text(
        "Space Invader",
        font40,
        "#FF7F50",
        int(screen_width / 2 - title.get_width() / 2),
        120,
    )
    btn_vol.draw_btn(screen)
    btn_start.draw_btn(screen)
    btn_Exit.draw_btn(screen)
    btn_vol.change_img(status)
    pygame.display.update()


# Set Volume Status
def set_vol(vol_status):
    if vol_status:
        # Volume Status On
        explosion_fx.set_volume(0.25)
        explosion2_fx.set_volume(0.25)
        laser_fx.set_volume(0.25)
        button_click_fx.set_volume(0.5)
        play_fx.set_volume(0.75)
        main_fx.set_volume(0.75)
    else:
        # Volume Status Off
        explosion_fx.set_volume(0)
        explosion2_fx.set_volume(0)
        laser_fx.set_volume(0)
        button_click_fx.set_volume(0)
        play_fx.set_volume(0)
        main_fx.set_volume(0)


# Screen Play Game
def play_game(countdown, last_count, alien_countdown, last_alien_shot, game_over):
    spaceship = Spaceship(int(screen_width / 2), screen_height - 100, 3)
    spaceship_group.add(spaceship)
    create_aliens()
    run = True
    life_hearth = 3
    while run:
        clock.tick(fps)
        # draw background
        draw_bg()
        draw_text("Heart: ", font20, white, 10, 20)
        draw_text(str(life_hearth), font20, white, 150, 20)
        if countdown == 0:
            # create random alien bullets
            # record current time
            time_now = pygame.time.get_ticks()
            # shoot
            if (
                time_now - last_alien_shot > alien_countdown
                and len(alien_bullet_group) < 5
                and len(alien_group) > 0
            ):
                attacking_alien = random.choice(alien_group.sprites())
                alien_bullet = Alien_Bullets(
                    attacking_alien.rect.centerx, attacking_alien.rect.bottom
                )
                alien_bullet_group.add(alien_bullet)
                last_alien_shot = time_now

            # check if all the aliens have been killed
            if len(alien_group) == 0:
                game_over = 1

            if game_over == 0:
                # update spaceship
                game_over = spaceship.update()

                # update sprite groups
                bullet_group.update()
                alien_group.update()
                alien_bullet_group.update(spaceship)
            else:
                if game_over == -1:
                    if life_hearth > 1:
                        life_hearth -= 1
                        spaceship = Spaceship(
                            int(screen_width / 2), screen_height - 100, 3
                        )
                        spaceship_group.add(spaceship)
                        game_over = 0
                    else:
                        draw_text(
                            "GAME OVER!",
                            font40,
                            white,
                            int(screen_width / 2 - 100),
                            int(screen_height / 2 + 50),
                        )
                if game_over == 1:
                    draw_text(
                        "YOU WIN!",
                        font40,
                        white,
                        int(screen_width / 2 - 100),
                        int(screen_height / 2 + 50),
                    )
        # Start Count Down Screen Before Play Game
        if countdown > 0:
            draw_text(
                "GET READY!",
                font40,
                white,
                int(screen_width / 2 - 110),
                int(screen_height / 2 + 50),
            )
            draw_text(
                str(countdown),
                font40,
                white,
                int(screen_width / 2 - 10),
                int(screen_height / 2 + 100),
            )
            count_timer = pygame.time.get_ticks()

            if count_timer - last_count > 1000:
                countdown -= 1
                last_count = count_timer

        # update explosion group
        explosion_group.update()

        # draw sprite groups
        spaceship_group.draw(screen)
        bullet_group.draw(screen)
        alien_group.draw(screen)
        alien_bullet_group.draw(screen)
        explosion_group.draw(screen)

        # event handlers
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                main_fx.stop()
                play_fx.play()
        pygame.display.update()


# Screen Menu
def main_menu(
    vol_status, countdown, last_count, alien_countdown, last_alien_shot, game_over
):
    if vol_status:
        main_fx.play(-1)
    while True:
        Mouse_Pos = pygame.mouse.get_pos()
        create_btn_menu(vol_status)

        for button in [btn_Exit, btn_start]:
            button.change_Statue(Mouse_Pos)
            button.draw_btn(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check Colision Button Start
                if btn_start.check_Colision(Mouse_Pos):
                    button_click_fx.play()
                    main_fx.stop()
                    play_fx.play()
                    time.sleep(0.5)
                    # Screen Play Game
                    play_game(
                        countdown,
                        last_count,
                        alien_countdown,
                        last_alien_shot,
                        game_over,
                    )
                # Check Colision Button Exit
                if btn_Exit.check_Colision(Mouse_Pos):
                    button_click_fx.play()
                    time.sleep(0.5)
                    main_fx.stop()
                    pygame.quit()
                    sys.quit()
                # Check Colision Button Volume
                if btn_vol.check_Colision(Mouse_Pos):
                    if vol_status:h
                        vol_status = False
                    else:
                        vol_status = True
                    set_vol(vol_status)
                    btn_vol.change_img(vol_status)
                    btn_vol.draw_btn(screen)
                    button_click_fx.play()


if __name__ == "__main__":
    main_menu(
        vol_status, countdown, last_count, alien_countdown, last_alien_shot, game_over
    )
    pygame.quit()
