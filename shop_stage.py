import pygame
import static_resources as sr
from network import Network
from gui import *
from gameElements import Minion, Player, Hero
from gameElements import Tribe
from gameElements import State
from gameElements import Stats


def shopping(players, current_player, n, clock, screen):
    start_time = pygame.time.get_ticks()
    shop = ShopVisualiser(players[current_player])
    sr.redraw_shop(screen, shop)
    running = True
    while running:
        timer = (sr.shop_time - (pygame.time.get_ticks() - start_time) // 1000)
        sr.timer_display(timer, 665, 500, screen, "shop")
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
        if not timer:
            n.send(players[current_player])
            shop.player.hero.on_turn_end()
            pygame.time.delay(2500)
            running = False
            combat(players, current_player, n, clock, screen)


def combat(players, current_player, n, clock, screen):
    start_time = pygame.time.get_ticks()
    players, opponent = n.send(players[current_player])
    screen.blit(sr.board, (0, 0))
    pygame.display.flip()
    combat_viualiser = CombatVisualiser(players[current_player], players[opponent])
    combat_viualiser.draw(screen)
    running = True
    minions = list(filter(None, copy.deepcopy(players[current_player].get_hero().get_minions())))
    minions_opponent = list(filter(None, copy.deepcopy(players[opponent].get_hero().get_minions())))
    minion_attacker = 0
    attack_time = pygame.time.get_ticks()
    if not current_player % 2:
        attack_time -= 3000
    print("wchodzę do pentli XDD")
    while running:
        timer = (sr.combat_time - (pygame.time.get_ticks() - start_time) // 1000)
        clock.tick(60)
        if current_player % 2:
            if pygame.time.get_ticks() - attack_time > 3000:
                print("atakuje XD I am current player 1?")
                attack_time = pygame.time.get_ticks()
        else:
            if pygame.time.get_ticks() - attack_time > 3000:
                print("atakuje XD I am current player 2?")
                attack_time = pygame.time.get_ticks()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
        if not timer:
            running = False
            shopping(players, current_player, n, clock, screen)
