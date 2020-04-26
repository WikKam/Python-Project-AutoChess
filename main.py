from time import sleep

import pygame
from gameElements import Minion, Player, Hero
from gameElements import Tribe
from gameElements import State
from gameElements import Stats
from network import Network
import static_resources as sr
from waiting_stage import waiting
from recruitment_stage import recruitment # temporary

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("AutoChess")
net = Network()
clock = pygame.time.Clock()


waiting(net, screen, clock)
# recruitment(net.getP(), net, clock, screen)
