import pygame
import static_resources as sr
from network import Network
from gui import MinionButton
from gui import ShopVisualiser
from gameElements import Minion, Player, Hero
from gameElements import Tribe
from gameElements import State
from gameElements import Stats


def shop(current_player, n, clock, screen):
    print(current_player.get_hero().name)
    shop = ShopVisualiser(current_player)
    shop_timer = 40
    sr.redraw_shop(screen, shop)
    running = True
    while running:
        player2 = n.send(current_player)
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if shop.upgradeButton.onclick(pos,shop):
                    sr.redraw_shop(screen, shop)
                if shop.roll.onclick(pos, shop):
                    sr.redraw_shop(screen, shop)
                for btn in shop.minion_btns:
                    #pos = pygame.mouse.get_pos()
                    if btn.onclick(pos, shop):
                        sr.redraw_shop(screen, shop)
        n.send(current_player)
        #sr.timer_display(shop_timer, 400, 500, screen)
        # redraw_window(screen, p)
        # print(player2.get_hero().get_minions())