from time import sleep

import pygame
from gameElements import Minion, Player, Hero
from gameElements import Tribe
from gameElements import State
from gameElements import Stats
from gui import MinionButton
from gui import ShopVisualiser
from network import Network
import static_resources as sr
from waiting_stage import waiting

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("AutoChess")


def redraw_shop(win, shop): # need separate func for shop and combat
    win.fill((255, 255, 255))
    win.blit(sr.board, (0, 0))
    shop.draw(win)
    pygame.display.flip()
    # player.draw(win)
    #pygame.display.update()

net = Network()
clock = pygame.time.Clock()


def shop(current_player, n):
    shop = ShopVisualiser(current_player)
    shop_timer = 40
    redraw_shop(screen, shop)
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
                    redraw_shop(screen, shop)
                if shop.roll.onclick(pos, shop):
                    redraw_shop(screen, shop)
                for btn in shop.minion_btns:
                    #pos = pygame.mouse.get_pos()
                    if btn.onclick(pos, shop):
                        redraw_shop(screen, shop)
        n.send(current_player)
        #sr.timer_display(shop_timer, 400, 500, screen)
        # redraw_window(screen, p)
        print(player2.get_hero().get_minions())


def combat():
    pass


def recruitment(current_player, n):
    start_time = pygame.time.get_ticks()
    screen.fill((255, 255, 255))
    # screen.blit(sr.board, (0, 0))
    # pygame.display.flip()
    screen.blit(sr.recruitment_background, (0, 0))
    pygame.display.flip()
    sr.timer_display((20 - (pygame.time.get_ticks()-start_time)//1000), 350, 400, screen, "recruitment")
    running = True
    while running:
        timer = (4 - (pygame.time.get_ticks() - start_time) // 1000)
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        screen.blit(sr.recruitment_background, (0, 0))
        pygame.display.flip()
        sr.timer_display(timer, 350, 400, screen, "recruitment")
        #click event to pick hero and redirect to shop
        current_player.recruit_hero()
        n.send(current_player)
        if timer == 0:
            running = False
            shop(current_player)



waiting(net, screen, clock)
# recruitment(n.getP())
