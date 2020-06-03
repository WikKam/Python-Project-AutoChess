import pygame

from game_elements.game_enums import State
from static_resources import create_image_with_size, is_clicked


class MinionVisualiser:
    hovered_minion = None

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
        self.animation_speed = 10
        self.current_x = self.x
        self.is_attacking = False
        self.current_y = self.y
        self.has_already_hit = False
        self.has_already_returned = False
        self.hover_img = create_image_with_size(self.minion.card_path, 200, 300)
        self.in_hand_img = create_image_with_size(self.minion.card_path, 150, 250)

    def calculate_hover_x(self):
        w, h = pygame.display.get_surface().get_size()
        return self.x + self.width + 10 if self.x + self.width + 10 + 200 < w else self.x - 210

    def create_icon(self):
        result = pygame.image.load(self.minion.icon_path)
        return pygame.transform.scale(result, (100, 120))

    def update_hover(self, pos, screen):
        if not is_clicked(pos, self.x, self.y, self.width, self.height):
            if MinionVisualiser.hovered_minion is self:
                MinionVisualiser.hovered_minion = None
            self.is_hovered = False
        else:
            MinionVisualiser.hovered_minion = self
            self.is_hovered = True


    def draw(self, win):
        if self.minion.state == State.in_hand:
            win.blit(self.in_hand_img, (self.current_x, self.current_y))
        else:
            self.animate_attack()
            win.blit(self.icon, (self.current_x, self.current_y))
            win.blit(self.outline_font.render(str(self.minion.stats.attack), True, (0, 0, 0)),
                     (self.current_x + 20, self.current_y - 2 + self.height / 1.5))
            win.blit(self.outline_font.render(str(self.minion.stats.health), True,
                                              (0, 0, 0)), (self.current_x + self.width - 30, self.current_y - 2 + self.height / 1.5))
            win.blit(self.font.render(str(self.minion.stats.attack), True, (255, 255, 255)),
                     (self.current_x + 20, self.current_y - 2 + self.height / 1.5))
            win.blit(self.font.render(str(self.minion.stats.health), True,
                                      (255, 255, 255)), (self.current_x + self.width - 30, self.current_y - 2 + self.height / 1.5))

    def set_target(self, target):
        self.target = target
        self.is_attacking = True
        self.dx = (self.target.x - self.x)/self.animation_speed
        self.dy = (self.target.y - self.y)/self.animation_speed
        self.has_already_hit = False
        self.has_already_returned = False

    def animate_attack(self):
        if self.is_attacking:
            print("attacking...")
            if not self.has_already_hit:
                self.current_x += self.dx
                self.current_y += self.dy
                if abs(self.current_x - self.target.x) < abs(self.dx*5)\
                        or abs(self.current_y - self.target.y) < abs(self.dy*5):
                    self.has_already_hit = True
            else:
                if self.current_y != self.y or self.current_x != self.x:
                    self.current_x -= self.dx
                    self.current_y -= self.dy
                else:
                    self.has_already_returned = True
                    self.is_attacking = False
                    self.has_already_hit = False
                    print("FINISHED ATTACK")

