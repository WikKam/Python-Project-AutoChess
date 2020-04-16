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

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("AutoChess")


def redraw_window(win, shop): # need separate func for shop and combat
    win.fill((255, 255, 255))
    win.blit(sr.board, (0, 0))
    shop.draw(win)
    pygame.display.flip()
    # player.draw(win)
    #pygame.display.update()


# minion = Minion("first", Tribe.orc, [], State.in_play, Stats(4, 4, 1))
# minion1 = Minion("first", Tribe.orc, [], State.in_play, Stats(4, 4, 1))
# minion2 = Minion("first", Tribe.orc, [], State.in_play, Stats(4, 4, 1))
# minion3 = Minion("first", Tribe.orc, [], State.in_play, Stats(4, 4, 1))
#
# hminion1 = Minion("first", Tribe.orc, [], State.in_hand, Stats(4, 4, 1))
# hminion2 = Minion("first", Tribe.orc, [], State.in_hand, Stats(4, 4, 1))
# hminion3 = Minion("first", Tribe.orc, [], State.in_hand, Stats(4, 4, 1))

#p.get_hero().add_minion(minion)
#p.get_hero().add_minion(minion1)
#p.get_hero().add_minion(minion2)
#p.get_hero().add_minion(minion3)
#p.get_hero().add_minion_in_hand(hminion1)
#p.get_hero().add_minion_in_hand(hminion2)
#p.get_hero().add_minion_in_hand(hminion3)

n = Network()
clock = pygame.time.Clock()


def shop(current_player):
    shop = ShopVisualiser(current_player)
    shop_timer = 40
    redraw_window(screen, shop)
    running = True
    while running:
        palyer2 = n.send(current_player)
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if shop.upgradeButton.onclick(pos,shop):
                    redraw_window(screen,shop)
                for btn in shop.minion_btns:
                    #pos = pygame.mouse.get_pos()
                    if btn.onclick(pos, shop):
                        redraw_window(screen, shop)
        n.send(current_player)
        #sr.timer_display(shop_timer, 400, 500, screen)
        # redraw_window(screen, p)


def combat():
    pass


def recruitment(current_player):
    screen.fill((255, 255, 255))
    screen.blit(sr.board, (0, 0))
    pygame.display.flip()
    screen.blit(sr.recruitment_background, (0, 0))
    pygame.display.flip()
    running = True
    while running:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
        #click event to pick hero and redirect to shop
        current_player.recruit_hero()
        n.send(current_player)
        running = False
        shop(current_player)

def waiting():
    current_player = n.getP()  # actual player
    current_player.get_hero().add_minion(Minion("first", Tribe.orc, [], State.in_play, Stats(4, 4, 1), "minions_icons/Axe.png"))
    screen.fill((255, 255, 255))
    screen.blit(sr.waiting_background, (0, 0))
    pygame.display.flip()
    running = True
    while running:
        clock.tick(60)
        player2 = n.send(current_player)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
        if player2.ready:
            running = False
            recruitment(current_player)


# waiting()
recruitment(n.getP())
