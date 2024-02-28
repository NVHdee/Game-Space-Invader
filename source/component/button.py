import pygame


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
