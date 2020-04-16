import pygame
from gameElements import Minion
from gameElements import Tribe
from gameElements import State
from gameElements import Stats
from gameElements import Hero
from gameElements import Player


class MinionButton:
    def __init__(self, minion, player, x, y):
        self.minion = minion
        self.player = player
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.icon = self.create_icon()

    def draw(self, win):
        # pygame.draw.rect(win, (0, 200, 0), (self.x, self.y, self.width, self.height))
        win.blit(self.icon, (self.x, self.y))

    def get_minion(self):
        return self.minion

    def create_icon(self):
        result = pygame.image.load(self.minion.icon_path)
        return pygame.transform.scale(result, (50, 50))

    def onclick(self, pos, shop):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= (self.x + self.width) and self.y <= y1 <= (self.y + self.height):
            if self.minion.get_state() == State.in_shop:  # buying
                print("KLIK")
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


class ShopVisualiser:

    def __init__(self, player):
        self.player = player
        self.minions_in_shop = []
        self.get_random_minions(self.player.get_hero().get_current_tier())
        print(self.minions_in_shop.__len__())
        self.make_minion_buttons()
        self.gold = GoldVisualiser(player.hero)
        self.upgradeButton = UpgradeTavernButton(player.hero)
        print(self.minion_btns.__len__())

    def draw(self, screen):
        pygame.display.update()
        pygame.draw.line(screen, (0, 255, 255), (0, 150), (800, 150))
        pygame.draw.line(screen, (0, 255, 255), (0, 450), (800, 450))
        pygame.draw.line(screen, (0, 255, 255), (0, 300), (800, 300))
        pygame.draw.line(screen, (0, 255, 255), (150, 0), (150, 150))
        pygame.draw.line(screen, (0, 255, 255), (650, 600), (650, 450))
        self.gold.draw(screen)
        self.upgradeButton.draw(screen)
        for mb in self.minion_btns:
            mb.draw(screen)
        pygame.display.flip()

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

    def get_random_minions(self, tier):
        index = 0
        while index < 7:
            minion = Minion("test", Tribe.orc, [], State.in_shop, Stats(4, 4, tier), "minions_icons/Axe.png")
            minion.set_position(index)
            self.minions_in_shop.append(minion)
            index += 1

    def get_buttons(self):
        return self.minion_btns

    def remove_from_shop(self, minion):
        self.minions_in_shop.remove(minion)


class GoldVisualiser:

    def __init__(self, hero):
        self.hero = hero

    def draw(self, win):
        counter = 0
        offset = 50
        print(self.hero.current_gold)
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

    def draw(self, screen):
        color = (0, 0, 200) if self.isEnabled else (200, 0, 0)
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))

    def onclick(self, pos, shop):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= (self.x + self.width) and self.y <= y1 <= (self.y + self.height):
            self.isEnabled = False
            self.hero.upgrade_tier()
            print("upgraded")
            return True
