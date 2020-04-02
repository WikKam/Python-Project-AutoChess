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

    def draw(self, win):
        pygame.draw.rect(win, (0, 200, 0), (self.x, self.y, self.width, self.height))

    def get_minion(self):
        return self.minion

    def onclick(self, pos, shop):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= (self.x + self.width) and self.y <= y1 <= (self.y + self.height):
            if self.minion.get_state() == State.in_shop:
                print("KLIK")
                if self.player.get_hero().buy_minion(self.minion):
                    shop.remove_from_shop(self.get_minion())
                    shop.make_minion_buttons()
                    return True
            elif self.minion.get_state() == State.in_hand:
                if self.player.get_hero().play_minion(self.minion):
                    shop.make_minion_buttons()
                    return True
            elif self.minion.get_state() == State.in_play:
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
        print(self.minion_btns.__len__())

    def draw(self, screen):
        pygame.display.update()
        pygame.draw.line(screen, (0, 255, 255), (0, 150), (800, 150))
        pygame.draw.line(screen, (0, 255, 255), (0, 450), (800, 450))
        pygame.draw.line(screen, (0, 255, 255), (0, 300), (800, 300))
        pygame.draw.line(screen, (0, 255, 255), (150, 0), (150, 150))
        pygame.draw.line(screen, (0, 255, 255), (650, 600), (650, 450))
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
                mb = MinionButton(m, self.player, 2*m.position*50 + offset, 500)
                minion_btns.append(mb)
        self.minion_btns = minion_btns

    def get_random_minions(self, tier):
        index = 0
        while index < 7:
            minion = Minion("test", Tribe.orc, [], State.in_shop, Stats(4, 4, tier))
            minion.set_position(index)
            self.minions_in_shop.append(minion)
            index += 1

    def get_buttons(self):
        return self.minion_btns

    def remove_from_shop(self, minion):
        self.minions_in_shop.remove(minion)

