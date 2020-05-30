import pygame

from game_stages.recruitment_stage import recruitment
from game_stages.shop_and_combat_stage import shopping, combat
from game_stages.waiting_stage import waiting
from server_comunication.network import Network

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("AutoChess")
network = Network()
players, current_player = network.get_player()
is_game_ended = False
is_game_ended = waiting(players[current_player], network, screen)
is_game_ended = recruitment(players[current_player],network,screen)
while not is_game_ended:
    is_game_ended = shopping(players[current_player],network,screen)
    is_game_ended = combat(players[current_player],network,screen)
