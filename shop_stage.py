import pygame
import static_resources as sr
from network import Network
from gui import MinionButton
from gui import ShopVisualiser
from gameElements import Minion, Player, Hero
from gameElements import Tribe
from gameElements import State
from gameElements import Stats
from combat_stage import combat


def shop(players, current_player, n, clock, screen):
    start_time = pygame.time.get_ticks()
    shop = ShopVisualiser(players[current_player])
    shop_timer = sr.shop_time
    sr.redraw_shop(screen, shop)
    running = True
    while running:
        timer = (sr.shop_time - (pygame.time.get_ticks() - start_time) // 1000)
        sr.timer_display(timer, 500, 500, screen, "recruitment")
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
                    if btn.onclick(pos, shop):
                        sr.redraw_shop(screen, shop)
        n.send(players[current_player])
        if timer == 0:
            combat(players, current_player, n, clock, screen)
        #sr.timer_display(shop_timer, 400, 500, screen)
        # redraw_window(screen, p)
        # print(player2.get_hero().get_minions())