import pygame
from gui.base_minion import MinionVisualiser
from game_elements.combat_logic import pick_minion_pair


class CombatVisualiser:
    def __init__(self, current_player_minions, opponent_minions, combat_manager):
        self.current_player_minions = current_player_minions
        self.opponent_minions = opponent_minions
        self.minions_buttons = []
        self.combat_manager = combat_manager
        self.is_attack_in_progress = False
        self.is_attack_done = False
        self.create_buttons()

    def draw(self, screen):
        if not self.is_attack_in_progress:
            att, vic = self.combat_manager.get_next_pair()
            if not (vic is None or att is None):
                self.set_animation_pair(att, vic)
                print("CURRENT ATTACKER: " + att.name)
                self.attacker_btn, self.victim_btn = self.get_minion_visualisers_pair()
                self.attacker_btn.set_target(self.victim_btn)
                self.is_attack_in_progress = True
        for mb in self.minions_buttons:
            if mb is self.attacker_btn:
                if mb.has_already_hit and not self.is_attack_done:
                    print('HAS ALREADY HIT')
                    self.combat_manager.do_attack()
                    self.is_attack_done = True
                if mb.has_already_returned:
                    self.is_attack_in_progress = False
                    self.is_attack_done = False
            mb.draw(screen)


    def create_buttons(self):
        shift = 0
        for i, m in enumerate(self.current_player_minions):
            shift = 200 - (len(self.current_player_minions) * 25) if len(self.current_player_minions) > 1 else 200
            mb = MinionVisualiser(m, 150 + 80 * i + shift, 270)
            self.minions_buttons.append(mb)
        for i, m in enumerate(self.opponent_minions):
            shift = 200 - (len(self.opponent_minions) * 25) if len(self.opponent_minions) > 1 else 200
            mb = MinionVisualiser(m, 150 + 80 * i + shift, 155)
            self.minions_buttons.append(mb)


    def get_button_with_minion(self, minion):
        return [x for x in self.minions_buttons if x.minion is minion].pop(0)

    def set_animation_pair(self, attacker, victim):
        self.attacker = attacker
        self.victim = victim
        self.is_attack_in_progress = True
        self.is_attack_done = False

    def get_minion_visualisers_pair(self):
        return self.get_button_with_minion(self.attacker), self.get_button_with_minion(self.victim)



