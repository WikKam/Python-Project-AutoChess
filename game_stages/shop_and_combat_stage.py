import pygame
import static_resources as sr
from gui.combat_visualiser import *
from gui.gui import *
from static_resources import clock, victory, lost, check_end_of_game
from utilities.timer_helper import shop_time, combat_time, timer_display
from gui.stages_visualiser import redraw_shop
from game_elements.combat_logic import Combat, check_if_players_have_minions, resolve_attack_turns
from game_elements.game_enums import PlayerState, AttackTurn
from game_stages.end_of_game_stage import game_over
from gui.scoreboard import draw_scoreboard


def shopping(current_player, network, screen):
    players, opponent = network.send(current_player)
    start_time = pygame.time.get_ticks()
    shop = ShopVisualiser(current_player)
    redraw_shop(screen, shop, [0, 0], shop_time, current_player, players)
    running = True
    while running:
        if check_end_of_game(players, current_player.id):
            game_over(screen, victory)
            return False
        clock.tick(60)
        timer = (shop_time - (pygame.time.get_ticks() - start_time) // 1000)
        pos = pygame.mouse.get_pos()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                current_player.get_hero().current_hp = 0
                current_player.status = PlayerState.dead
                network.send(current_player)
                running = False
                return True
            if e.type == pygame.MOUSEBUTTONDOWN:
                shop.upgradeButton.onclick(pos, shop)
                shop.roll.onclick(pos, shop)
                shop.hero.onclick(pos)
                for btn in shop.minion_btns:
                    btn.onclick(pos, shop)
                network.send(current_player)
        players, opponent = network.send(current_player)
        redraw_shop(screen, shop, pos, timer, current_player, players)
        if not timer:
            shop.player.hero.on_turn_end()
            network.send(current_player)
            #pygame.time.delay(2500)
            running = False
            return False
            #combat(current_player, network, screen)


def redraw_combat(win, combat_vis):
    win.blit(sr.board, (0, 0))
    combat_vis.draw(win)
    pygame.display.flip()


def combat(current_player, network, screen):
    current_player.status = PlayerState.in_combat
    players, opponent = network.send(current_player)
    resolve_attack_turns(current_player, players[opponent])
    minions = list(filter(None, copy.deepcopy(current_player.get_hero().get_minions())))
    minions_opponent = list(filter(None, copy.deepcopy(players[opponent].get_hero().get_minions())))
    can_play, status_code = check_if_players_have_minions(minions, minions_opponent)
    combat = Combat(minions, minions_opponent, current_player, players[opponent])
    screen.blit(sr.board, (0, 0))
    combat_visualiser = CombatVisualiser(minions, minions_opponent, combat)
    #    combat_visualiser.draw(screen)
    draw_scoreboard(players, current_player, screen)
    pygame.display.flip()
    running = True
    attack_time = pygame.time.get_ticks()
    attack_time_enemy = pygame.time.get_ticks()
    if current_player.attack_turn == AttackTurn.attack_first:
        attack_time -= 1000
    else:
        attack_time_enemy -= 1000
    if not can_play:
        if status_code < 0:
            current_player.get_hero().current_hp += status_code
        current_player.status = PlayerState.dead if current_player.get_hero().current_hp <= 0 else \
            PlayerState.after_combat
    while running:
        clock.tick(60)
        players, opponent = network.send(current_player)
        if current_player.status not in (PlayerState.after_combat, PlayerState.dead):
            end_round, hp = combat.check_if_all_minions_dead()
            if end_round and not combat_visualiser.is_attack_in_progress:
                if hp < 0:
                    current_player.get_hero().current_hp += hp
                current_player.status = PlayerState.dead if current_player.get_hero().current_hp <= 0 else \
                    PlayerState.after_combat
        if current_player.status in (PlayerState.after_combat, PlayerState.dead):
            all_players_finished_combat = True
            for player in players:
                if player.status not in (PlayerState.after_combat, PlayerState.dead):
                    all_players_finished_combat = False
                    break
            if all_players_finished_combat:
                running = False
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                current_player.get_hero().current_hp = 0
                current_player.status = PlayerState.dead
                network.send(current_player)
                return True
        redraw_combat(screen, combat_visualiser)
    print("My HP: ", current_player.hero.current_hp, current_player.hero.name)
    if current_player.status == PlayerState.dead:
        game_over(screen, lost)
    elif check_end_of_game(players, current_player.id):
        game_over(screen, victory)
    else:
        current_player.hero.on_new_turn()
        network.send(current_player)
        return False
        #shopping(current_player, network, screen)
