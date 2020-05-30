import pygame
from game_stages.recruitment_stage import recruitment
from game_elements.game_enums import PlayerState
from static_resources import waiting_background
from static_resources import clock, heroes


def waiting(current_player, network, screen):
    screen.blit(waiting_background, (0, 0))
    pygame.display.flip()
    running = True
    while running:
        clock.tick(60)
        players, opponent = network.send(current_player)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                current_player.recruit_hero(heroes[0])
                current_player.get_hero().current_hp = 0
                current_player.status = PlayerState.dead
                network.send(current_player)
                return True
        if players[3].status == PlayerState.connected:
            running = False
            return False
            #recruitment(current_player, network, screen)
