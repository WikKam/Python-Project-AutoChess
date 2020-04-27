import pygame
import static_resources as sr
from network import Network
from shop_stage import *
from gui import *


def combat(players, current_player, n, clock, screen):
    players, opponent = n.send(players[current_player])
    print(players[current_player].get_hero().get_minions())
    print(players[opponent].get_hero().get_minions())
    screen.blit(sr.board, (0, 0))
    pygame.display.flip()
    combat_viualiser = CombatVisualiser(players[current_player], players[opponent])
    combat_viualiser.draw(screen)
    running = True
    while running:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
