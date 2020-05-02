import pygame
import static_resources as sr
from gui.gui import *
from game_elements.gameElements import Minion, Player, Hero
from game_elements.gameElements import Tribe
from game_elements.gameElements import State
from game_elements.gameElements import Stats


def attack(my_minion, opponent_minion, attacker_index, target):
    if my_minion[attacker_index].isDead:
        return attack(my_minion, opponent_minion, (attacker_index + 1) % len(my_minion), target)
    if opponent_minion[target].isDead:
        return attack(my_minion, opponent_minion, attacker_index, (target+1) % len(opponent_minion))
    # my_minion[attacker_index].attack(opponent_minion[target])
    opponent_minion[target].stats.health -= my_minion[attacker_index].stats.attack
    if opponent_minion[target].stats.health <= 0:
        opponent_minion[target].isDead = True
    return (attacker_index + 1) % len(my_minion), (target + 1) % len(opponent_minion)