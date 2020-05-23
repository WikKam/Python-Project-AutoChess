import pygame
from gui.base_minion import Minion


class CombatVisualiser:
    def __init__(self, current_player_minions, opponent_minions):
        self.current_player_minions = current_player_minions
        self.opponent_minions = opponent_minions
        self.minions_buttons = []

    def draw(self, screen):
        shift = 0
        for i, m in enumerate(self.current_player_minions):
            shift = 200 - (len(self.current_player_minions) * 25) if len(self.current_player_minions) > 1 else 200
            mb = Minion(m, 150 + 80 * i + shift, 340)
            self.minions_buttons.append(mb)
        for i, m in enumerate(self.opponent_minions):
            shift = 200 - (len(self.opponent_minions) * 50) if len(self.opponent_minions) > 1 else 200
            mb = Minion(m, 150 + 80 * i + shift, 170)
            self.minions_buttons.append(mb)
        for mb in self.minions_buttons:
            mb.draw(screen)
            pygame.display.flip()



