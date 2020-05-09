import pygame
import static_resources as sr
from gui.gui import *
from game_elements.combat_logic import attack
from static_resources import clock
from utilities.timer_helper import shop_time, combat_time, timer_display
from gui.stages_visualiser import redraw_shop


def shopping(current_player, network, screen):
    start_time = pygame.time.get_ticks()
    shop = ShopVisualiser(current_player)
    redraw_shop(screen, shop)
    running = True
    while running:
        clock.tick(60)
        #redraw_shop(screen,shop)
        timer = (shop_time - (pygame.time.get_ticks() - start_time) // 1000)
        timer_display(timer, 665, 500, screen, "shop")
        for e in pygame.event.get():
            needs_update = False
            pos = pygame.mouse.get_pos()
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                if shop.upgradeButton.onclick(pos,shop):
                    needs_update = True
                if shop.roll.onclick(pos, shop):
                    needs_update = True
                if shop.hero.onclick(pos):
                    needs_update = True
                for btn in shop.minion_btns:
                    if btn.onclick(pos, shop):
                        needs_update = True
                network.send(current_player)
            if e.type == pygame.MOUSEMOTION:
                for btn in shop.minion_btns:
                     if btn.update_hover(pos,screen):
                         needs_update = True
            if needs_update:
                redraw_shop(screen,shop)
        if not timer:
            network.send(current_player)
            shop.player.hero.on_turn_end()
            pygame.time.delay(2500)
            running = False
            combat(current_player, network, screen)
        #redraw_shop(screen, shop)

def combat(current_player, network, screen):
    start_time = pygame.time.get_ticks()
    players, opponent = network.send(current_player)
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
    while running:
        timer = (combat_time - (pygame.time.get_ticks() - start_time) // 1000)
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
            shopping(current_player, network, screen)
        # if not timer:
        #     running = False
        #     players[current_player].hero.on_new_turn()
        #     shopping(players, current_player, n, clock, screen)

