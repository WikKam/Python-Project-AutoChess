import pygame
from game_stages.waiting_stage import waiting
from server_communication.network import Network

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("AutoChess")
network = Network()
current_player = network.get_player()
waiting(current_player, network, screen)
