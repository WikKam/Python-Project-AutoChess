import pygame
import static_resources as sr
from gui.gui import *
from game_elements.gameElements import Minion, Player, Hero
from game_elements.gameElements import Tribe
from game_elements.gameElements import State
from game_elements.gameElements import Stats
from game_elements.combat_logic import attack
from static_resources import clock
from static_resources import current_player, network


def shopping(screen):
    start_time = pygame.time.get_ticks()
    shop = ShopVisualiser(current_player)
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
                if shop.hero.onclick(pos):
                    sr.redraw_shop(screen,shop)
                for btn in shop.minion_btns:
                    if btn.onclick(pos, shop):
                        sr.redraw_shop(screen, shop)
                network.send(current_player)
        if not timer:
            network.send(current_player)
            shop.player.hero.on_turn_end()
            pygame.time.delay(2500)
            running = False
            combat(screen)


def combat(screen):
    start_time = pygame.time.get_ticks()
    players, opponent = network.send(current_player)
    print(current_player.get_hero().get_minions())
    print(players[opponent].get_hero().get_minions())
    players, opponent = n.send(current_player)
    minions = list(filter(None, copy.deepcopy(current_player.get_hero().get_minions())))
    print(players[opponent])
    minions_opponent = list(filter(None, copy.deepcopy(players[opponent].get_hero().get_minions())))
    screen.blit(sr.board, (0, 0))
    pygame.display.flip()
    combat_visualiser = CombatVisualiser(current_player, players[opponent])
    combat_visualiser.draw(screen)
    running = True
    minion_attacker = 0
    target = 0
    me_target = 0
    enemy_attacker = 0
    attack_time = pygame.time.get_ticks()
    attack_time_enemy = pygame.time.get_ticks()
    if current_player.id % 2:
        attack_time -= 1000
    else:
        attack_time_enemy -= 1000
    print("wchodzę do walki")
    print(minions_opponent)
    print(minions)
    while running:
        timer = (sr.combat_time - (pygame.time.get_ticks() - start_time) // 1000)
        clock.tick(60)
        if current_player.id % 2:
            if pygame.time.get_ticks() - attack_time > 3000:
                minion_attacker, target = attack(minions, minions_opponent, minion_attacker, target)
                attack_time = pygame.time.get_ticks()
                for m in minions:
                    print(m.stats.health)
                for m in minions_opponent:
                    print(m.stats.health)
            if pygame.time.get_ticks() - attack_time_enemy > 3000:
                enemy_attacker, me_target = attack(minions_opponent, minions, enemy_attacker, me_target)
                attack_time_enemy = pygame.time.get_ticks()
        else:
            if pygame.time.get_ticks() - attack_time > 3000:
                minion_attacker, target = attack(minions, minions_opponent, minion_attacker, target)
                attack_time = pygame.time.get_ticks()
                for m in minions:
                    print(m.stats.health)
                for m in minions_opponent:
                    print(m.stats.health)
            if pygame.time.get_ticks() - attack_time_enemy > 3000:
                enemy_attacker, me_target = attack(minions_opponent, minions, enemy_attacker, me_target)
                attack_time_enemy = pygame.time.get_ticks()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
        if minions[len(minions)-1].isDead or minions_opponent[len(minions_opponent)-1].isDead:
            if minions[-1].isDead:
                print("Opponent won round")
            else:
                print("You won round")
            running = False
            current_player.hero.on_new_turn()
            network.send(current_player)
            shopping(screen)
        # if not timer:
        #     running = False
        #     players[current_player].hero.on_new_turn()
        #     shopping(players, current_player, n, clock, screen)

