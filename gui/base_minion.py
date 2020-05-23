import pygame
from static_resources import create_image_with_size, is_clicked


class Minion:
    def __init__(self, minion, x, y):
        self.minion = minion
        self.x = x
        self.y = y
        self.width = 100
        self.height = 120
        self.icon = self.create_icon()
        self.font = pygame.font.Font('Fonts/Belwe Medium.otf', 22)
        self.outline_font = pygame.font.Font('Fonts/Belwe Medium.otf', 24)
        self.is_hovered = False
        self.hover_x = self.calculate_hover_x()

    def calculate_hover_x(self):
        w, h = pygame.display.get_surface().get_size()
        return self.x + self.width + 10 if self.x + self.width + 10 + 200 < w else self.x - 210

    def create_icon(self):
        result = pygame.image.load(self.minion.icon_path)
        return pygame.transform.scale(result, (100, 120))

    def update_hover(self, pos, screen):
        if is_clicked(pos, self.x, self.y, self.width, self.height):
            self.is_hovered = True
            img = create_image_with_size(self.minion.card_path, 200, 300)
            screen.blit(img, (self.hover_x, self.y - 50, 100, 100))
        else:
            self.is_hovered = False

    def draw(self, win):
        win.blit(self.icon, (self.x, self.y))
        win.blit(self.outline_font.render(str(self.minion.stats.attack), True, (0, 0, 0)),
                 (self.x + 20, self.y - 2 + self.height / 1.5))
        win.blit(self.outline_font.render(str(self.minion.stats.health), True,
                                          (0, 0, 0)), (self.x + self.width - 30, self.y - 2 + self.height / 1.5))
        win.blit(self.font.render(str(self.minion.stats.attack), True, (255, 255, 255)),
                 (self.x + 20, self.y - 2 + self.height / 1.5))
        win.blit(self.font.render(str(self.minion.stats.health), True,
                                  (255, 255, 255)), (self.x + self.width - 30, self.y - 2 + self.height / 1.5))