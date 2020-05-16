import pygame
import static_resources as sr
from gui.gui import *
from static_resources import clock
from utilities.timer_helper import shop_time, combat_time, timer_display
from gui.stages_visualiser import redraw_shop
from game_elements.combat_logic import Combat, check_if_players_have_minions, resolve_attack_turns
from game_elements.gameElements import PlayerState, AttackTurn
from game_stages.end_of_game_stage import game_over_lost


def shopping(current_player, network, screen):
    current_player.status = PlayerState.in_shop
    start_time = pygame.time.get_ticks()
    shop = ShopVisualiser(current_player)
    redraw_shop(screen, shop,[0,0],shop_time)
    running = True
    while running:
        clock.tick(60)
        timer = (shop_time - (pygame.time.get_ticks() - start_time) // 1000)
        pos = pygame.mouse.get_pos()
        for e in pygame.event.get():
            needs_update = False
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                if shop.upgradeButton.onclick(pos, shop):
                    needs_update = True
                if shop.roll.onclick(pos, shop):
                    needs_update = True
                if shop.hero.onclick(pos):
                    needs_update = True
                for btn in shop.minion_btns:
                    if btn.onclick(pos, shop):
                        needs_update = True
                network.send(current_player)
        redraw_shop(screen, shop, pos, timer)
        if not timer:
            network.send(current_player)
            shop.player.hero.on_turn_end()
            pygame.time.delay(2500)
            running = False
            combat(current_player, network, screen)


def combat(current_player, network, screen):
    current_player.status = PlayerState.in_combat
    players, opponent = network.send(current_player)
    print("My HP", current_player.hero.current_hp, current_player.status, current_player.attack_turn)
    print("Opponend Hp", players[opponent].hero.current_hp, players[opponent].attack_turn)
    resolve_attack_turns(current_player, players[opponent])
    print("My HP", current_player.hero.current_hp, current_player.status, current_player.attack_turn)
    print("Opponend Hp", players[opponent].hero.current_hp, players[opponent].attack_turn)
    minions = list(filter(None, copy.deepcopy(current_player.get_hero().get_minions())))
    minions_opponent = list(filter(None, copy.deepcopy(players[opponent].get_hero().get_minions())))
    can_play, status_code = check_if_players_have_minions(minions, minions_opponent)
    combat = Combat(minions, minions_opponent)
    screen.blit(sr.board, (0, 0))
    pygame.display.flip()
    combat_visualiser = CombatVisualiser(current_player, players[opponent])
    combat_visualiser.draw(screen)
    running = True
    attack_time = pygame.time.get_ticks()
    attack_time_enemy = pygame.time.get_ticks()
    if current_player.attack_turn == AttackTurn.attack_first:
        attack_time -= 1000
    else:
        attack_time_enemy -= 1000
    if not can_play:
        current_player.status = PlayerState.after_combat
        if status_code < 0:
            current_player.get_hero().current_hp += status_code
    while running:
        clock.tick(60)
        players, opponent = network.send(current_player)
        if current_player.status == PlayerState.after_combat:
            all_players_finished_combat = True
            for player in players:
                if player.status != PlayerState.after_combat:
                    all_players_finished_combat = False
                    break
            if all_players_finished_combat:
                running = False
        else:
            end_round, hp = combat.check_if_all_minions_dead()
            if end_round:
                if hp < 0:
                    current_player.get_hero().current_hp += hp
                current_player.status = PlayerState.after_combat
            else:
                if current_player.attack_turn == AttackTurn.attack_first:
                    if pygame.time.get_ticks() - attack_time > 3000:
                        combat.current_player_attack()
                        attack_time = pygame.time.get_ticks()
                    if pygame.time.get_ticks() - attack_time_enemy > 3000:
                        combat.opponent_attack()
                        attack_time_enemy = pygame.time.get_ticks()
                else:
                    if pygame.time.get_ticks() - attack_time > 3000:
                        combat.current_player_attack()
                        attack_time = pygame.time.get_ticks()
                    if pygame.time.get_ticks() - attack_time_enemy > 3000:
                        combat.opponent_attack()
                        attack_time_enemy = pygame.time.get_ticks()
        for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
    if current_player.get_hero().current_hp <= 0:
        current_player.status = PlayerState.dead
    print("My HP", current_player.hero.current_hp, current_player.status)
    if current_player.status == PlayerState.dead:
        game_over_lost(screen)
    else:
        current_player.hero.on_new_turn()
        network.send(current_player)
        shopping(current_player, network, screen)
