import pygame
import static_resources as sr
from network import Network
from shop_stage import *


def combat(players, current_player, n, clock, screen):
    players, opponent = n.send(players[current_player])
    print(players[current_player].get_hero().get_minions())
    print(players[opponent].get_hero().get_minions())