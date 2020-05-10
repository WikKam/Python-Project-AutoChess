import pygame
from utilities.json_helper import *

from static_resources import create_image_with_size


def is_clicked(pos, x, y, width, height):
    x1 = pos[0]
    y1 = pos[1]
    return x <= x1 <= (x + width) and y <= y1 <= (y + height)


class MinionButton:
    def __init__(self, minion, player, x, y):
        self.minion = minion
        self.player = player
        self.x = x
        self.y = y
        self.width = 65
        self.height = 65
        self.icon = self.create_icon()
        self.font = pygame.font.SysFont('Arial', 25)
        self.is_hovered = False
        self.hover_x = self.calculate_hover_x()

    def calculate_hover_x(self):
        w, h = pygame.display.get_surface().get_size()
        return self.x + self.width + 10 if self.x + self.width + 10 + 200 < w else self.x - 210

    def draw(self, win):
        win.blit(self.icon, (self.x, self.y))
        win.blit(self.font.render(str(self.minion.stats.attack), True, (255, 255, 255)),
                 (self.x, self.y + self.height / 2))
        win.blit(self.font.render(str(self.minion.stats.health), True,
                                  (255, 255, 255)), (self.x + self.width - 10, self.y + self.height / 2))
        win.blit(self.font.render(str(self.minion.stats.tier), True, (255, 255, 255)),
                 (self.x + self.width / 2 - 5, self.y))

    def get_minion(self):
        return self.minion

    def create_icon(self):
        result = pygame.image.load(self.minion.icon_path)
        return pygame.transform.scale(result, (65, 65))

    def onclick(self, pos, shop):
        if is_clicked(pos, self.x, self.y, self.width, self.height):
            if self.minion.get_state() == State.in_shop:  # buying
                if self.player.get_hero().buy_minion(self.minion):
                    shop.remove_from_shop(self.get_minion())
                    shop.make_minion_buttons()
                    return True
            elif self.minion.get_state() == State.in_hand:  # playing
                if self.player.get_hero().play_minion(self.minion):
                    shop.make_minion_buttons()
                    return True
            elif self.minion.get_state() == State.in_play:  # selling
                if self.player.get_hero().sell_minion(self.minion):
                    shop.make_minion_buttons()
                    return True
        else:
            return False

    def update_hover(self, pos, screen):
        if is_clicked(pos, self.x, self.y, self.width, self.height):
            self.is_hovered = True
            img = create_image_with_size(self.minion.card_path, 200, 300)
            screen.blit(img, (self.hover_x, self.y - 50, 100, 100))
        else:
            self.is_hovered = False
        #pygame.display.update((self.hover_x, self.y - 50, 100, 100))

class ShopVisualiser:
    def __init__(self, player):
        self.player = player
        self.minions_in_shop = []
        print(self.minions_in_shop.__len__())
        self.gold = GoldVisualiser(player.hero)
        self.hero = HeroVisualiser(player.hero)
        self.upgradeButton = UpgradeTavernButton(player.hero)
        self.roll = RollMinionsButton(player.hero)
        self.all_minions = get_minions_from_Json()
        self.get_random_minions()
        self.make_minion_buttons()

    def draw(self, screen):
        pygame.draw.line(screen, (0, 255, 255), (0, 150), (800, 150))
        pygame.draw.line(screen, (0, 255, 255), (0, 450), (800, 450))
        pygame.draw.line(screen, (0, 255, 255), (0, 300), (800, 300))
        pygame.draw.line(screen, (0, 255, 255), (150, 0), (150, 150))
        pygame.draw.line(screen, (0, 255, 255), (650, 600), (650, 450))
        self.gold.draw(screen)
        self.upgradeButton.draw(screen)
        self.hero.draw(screen)
        self.roll.draw(screen)
        for mb in self.minion_btns:
            mb.draw(screen)

    def make_minion_buttons(self):
        offset = 50
        minion_btns = []
        for m in self.minions_in_shop:
            if not (m is None):
                mb = MinionButton(m, self.player, 2 * m.position * 50 + offset, 200)
                minion_btns.append(mb)

        for m in self.player.hero.minions:
            if not (m is None):
                mb = MinionButton(m, self.player, 2 * m.position * 50 + offset, 350)
                minion_btns.append(mb)

        for m in self.player.hero.hand:
            if not (m is None):
                mb = MinionButton(m, self.player, 2 * m.position * 50 + offset, 500)
                minion_btns.append(mb)
        self.minion_btns = minion_btns

    def get_random_minions(self):
        self.minions_in_shop = self.roll.get_random_minions(self.all_minions)
        # for m in self.minions_in_shop: pprint(vars(m))

    def get_buttons(self):
        return self.minion_btns

    def remove_from_shop(self, minion):
        self.minions_in_shop.remove(minion)


class GoldVisualiser:

    def __init__(self, hero):
        self.hero = hero

    def draw(self, win):
        counter = 0
        offset = 25
        while counter < self.hero.current_gold:
            pygame.draw.rect(win, (255, 255, 10), (500 + counter * offset, 100, 20, 20))
            counter += 1


class UpgradeTavernButton:

    def __init__(self, hero):
        self.hero = hero
        self.x = 200
        self.y = 25
        self.width = 100
        self.height = 100
        self.isEnabled = True
        self.font = pygame.font.SysFont('Arial', 25)

    def draw(self, screen):
        color = (0, 0, 200) if self.isEnabled and self.hero.can_upgrade_tier() else (220, 220, 220)
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
        screen.blit(self.font.render(str(self.hero.current_upgrade_cost), True, (0, 0, 0)),
                    (self.x + self.width / 2 - 5, self.y))

    def onclick(self, pos, shop):
        if is_clicked(pos, self.x, self.y, self.width, self.height):
            self.isEnabled = False
            success = self.hero.upgrade_tier()
            return True
        return False


class RollMinionsButton:

    def __init__(self, hero):
        self.hero = hero
        self.x = 320
        self.y = 50
        self.width = 50
        self.height = 50
        self.font = pygame.font.SysFont('Arial', 25)

    def get_random_minions(self, all_minions):
        ret = []
        correct_tier_minions = [m for m in all_minions if m.stats.tier <= self.hero.current_tier]
        for x in range(self.hero.hero_stats.max_minion_no):
            index = random.randint(0, len(correct_tier_minions) - 1)
            m = copy.deepcopy(correct_tier_minions[index])
            m.set_position(x)
            ret.append(m)
        return ret

    def draw(self, screen):
        color = (100, 100, 100) if self.hero.can_reroll_tavern() else (220, 220, 220)
        img = pygame.image.load("images/Buttons/roll.png")
        #pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
        screen.blit(img,(self.x, self.y))
        screen.blit(self.font.render(str(self.hero.reroll_cost), True, color),
                    (self.x + self.width / 2 + 8, self.y))

    def onclick(self, pos, shop):
        if is_clicked(pos, self.x, self.y, self.width, self.height):
            if self.hero.can_reroll_tavern():
                shop.get_random_minions()
                self.hero.on_tavern_reroll()
                shop.make_minion_buttons()
                return True
        return False


class CombatVisualiser:
    def __init__(self, current_player, opponent):
        self.current_player = current_player
        self.opponent = opponent
        self.minions_buttons = []

    def draw(self, screen):
        for i, m in enumerate(self.current_player.get_hero().get_minions()):
            if m is None:
                break
            mb = MinionButton(m, self.current_player, 150 +
                              80 * i, 340)
            self.minions_buttons.append(mb)
        for i, m in enumerate(self.opponent.get_hero().get_minions()):
            if m is None:
                break
            mb = MinionButton(m, self.opponent, 150 +
                              80 * i, 170)
            self.minions_buttons.append(mb)
        for mb in self.minions_buttons:
            mb.draw(screen)


class HeroVisualiser:
    def __init__(self, hero):
        self.hero = hero
        self.x = 285
        self.y = 430
        self.width = 150
        self.height = 200
        self.hero_icon = create_image_with_size(hero.icon, self.width, self.height)
        self.hero_power_radius = 50
        self.is_hero_power_enabled = True

    def draw(self, screen):
        color = (255, 255, 255) if self.is_hero_power_enabled and self.hero.can_use_hero_power() else (0, 0, 0)
        screen.blit(self.hero_icon, (self.x, self.y))
        pygame.draw.circle(screen, color, (self.x + self.width + 50, 450 + round(self.height / 2)),
                           self.hero_power_radius, 5)

    def onclick(self, pos):
        distance = ((pos[0] - (self.x + self.width + 50)) ** 2 + (pos[1] - (450 + round(self.height / 2))) ** 2) ** (
                    1 / 2)
        if distance < self.hero_power_radius and self.is_hero_power_enabled:
            print("click")
            self.hero.activate_hero_power()
            self.is_hero_power_enabled = False
            return True
        return False
