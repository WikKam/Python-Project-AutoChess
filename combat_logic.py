import pygame
import static_resources as sr
from network import Network
from gui import *
from gameElements import Minion, Player, Hero
from gameElements import Tribe
from gameElements import State
from gameElements import Stats


def attack(my_minion, opponen_minion, attacker_index):
    opponen_minion[random.randin(0, len(opponen_minion))].stats.health -= my_minion[attacker_index].stats.attack
    attacker_index += 1
    return attacker_index % len(my_minion)