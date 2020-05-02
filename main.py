import pygame
from game_stages.waiting_stage import waiting

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("AutoChess")
waiting(screen)
