import pygame
import static_resources as sr
from network import Network
from gui import *
from gameElements import Minion, Player, Hero
from gameElements import Tribe
from gameElements import State
from gameElements import Stats


def attack(my_minion, opponent_minion, attacker_index, target):
    if my_minion[attacker_index].isDead:
        return attack(my_minion, opponent_minion, (attacker_index + 1) % len(my_minion), target)
    if opponent_minion[target].isDead:
        return attack(my_minion, opponent_minion, attacker_index, (target+1) % len(opponent_minion))
    my_minion[attacker_index].attack(opponent_minion[target])
    return (attacker_index + 1) % len(my_minion), (target + 1) % len(opponent_minion)