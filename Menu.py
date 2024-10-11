import pygame

Dark_blue = (30, 30, 65)
grey = (30, 30, 30)
black = (0, 0, 0)
white = (230, 230, 230)

Button_width = 400
Button_height = 100


class Button:
    def __init__(self, surface, width, height, x, y, col, font, font_col, button_name):
        self.surface = surface
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.col = col
        self.font = font
        self.font_col = font_col
        self.button_name = button_name
        self.Pressed = False

    def draw(self):
        pygame.draw.rect(self.surface, self.col, (self.x, self.y, self.width, self.height))
        Render_BText = self.font.render(self.button_name, True, self.font_col)
        Button_rect = Render_BText.get_rect()
        Button_rect.center = ((self.x + (self.width // 2)), (self.y + (self.height // 2)))
        self.surface.blit(Render_BText, Button_rect)

    def Hit_Button(self, mouse):
        self.Pressed = False
        if self.x <= mouse[0] <= self.x + self.width:
            if self.y <= mouse[1] <= self.y + self.height:
                self.Pressed = True


class Slider:
    def __init__(self, surface, R1width, height, R2width, x, y, col, col_slid, font, font_col, slider_name):
        self.surface = surface
        self.R1width = R1width
        self.height = height
        self.R2width = R2width
        self.x = x
        self.y = y
        self.col = col
        self.col_slid = col_slid
        self.font = font
        self.font_col = font_col
        self.slider_name = slider_name
        self.sliding = False

    def draw(self):
        pygame.draw.rect(self.surface, self.col, (self.x, self.y, self.R1width, self.height))
        pygame.draw.rect(self.surface, self.col_slid, (self.x, self.y, self.R2width, self.height))
        Render_SText = self.font.render(self.slider_name, True, self.font_col)
        Slider_rect = Render_SText.get_rect()
        Slider_rect.center = ((self.x + (self.R1width // 2)), (self.y - (self.height // 2)))
        self.surface.blit(Render_SText, Slider_rect)

    def slide(self, mouse):
        self.sliding = False
        if self.x <= mouse[0] <= self.x + self.R1width:
            if self.y <= mouse[1] <= self.y + self.height:
                self.sliding = True
