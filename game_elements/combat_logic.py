from game_elements.game_enums import AttackTurn


def check_if_players_have_minions(current_player_minions, opponent_minions):
    if len(current_player_minions) == 0 and len(opponent_minions) == 0:
        return False, 0
    res = 0
    if len(current_player_minions) == 0:
        for minion in opponent_minions:
            res += minion.stats.tier
        return False, -res
    if len(opponent_minions) == 0:
        return False, 1
    return True, 0


def is_minion_dead(minion):
    if minion.stats.health <= 0:
        minion.isDead = True


def perform_attack(attacker, target):
    target.stats.health -= attacker.stats.attack


def resolve_attack_turns(player1, player2):
    if player1.attack_turn != player2.attack_turn:
        player2.attack_turn = AttackTurn(player2.attack_turn * -1)
        player1.attack_turn = AttackTurn(player1.attack_turn * -1)
    else:
        if player1.get_hero().current_hp == player2.get_hero().current_hp:
            player1.attack_turn = AttackTurn.attack_first if player1.id < player2.id else \
                AttackTurn.attack_second
            player2.attack_turn = AttackTurn(player1.attack_turn * -1)
        else:
            player1.attack_turn = AttackTurn.attack_first if player1.get_hero().current_hp < \
                                                             player2.get_hero().current_hp else AttackTurn.attack_second
            player2.attack_turn = AttackTurn(player1.attack_turn * -1)


def pick_minion_pair(attacker_idx, attacker_minions, victim_minions):
    if len(victim_minions) > attacker_idx and \
            not victim_minions[attacker_idx].isDead:
        return attacker_minions[attacker_idx], victim_minions[attacker_idx]
    else:
        for minion in victim_minions:
            if not minion.isDead:
                return attacker_minions[attacker_idx], minion


class Combat:
    def __init__(self, current_player_minions, opponent_minions, curr_player, opponent):
        self.current_player_minions = current_player_minions
        self.opponent_minions = opponent_minions
        self.current_player_index = 0
        self.opponent_index = 0
        self.curr_player = curr_player
        self.opponent = opponent
        self.next_attack = self.curr_player if self.curr_player.attack_turn == AttackTurn.attack_first else self.opponent
        resolve_attack_turns(self.curr_player, self.opponent)

    def current_player_attack(self):
        attacker, victim = pick_minion_pair(self.current_player_index, self.current_player_minions,
                                            self.opponent_minions)
        perform_attack(attacker, victim)
        is_minion_dead(victim)
        self.current_player_index = (self.current_player_index + 1) % len(self.current_player_minions)

    def opponent_attack(self):
        attacker, victim = pick_minion_pair(self.opponent_index, self.opponent_minions,
                                            self.current_player_minions)
        perform_attack(attacker, victim)
        is_minion_dead(victim)
        self.opponent_index = (self.opponent_index + 1) % len(self.opponent_minions)

    def check_if_all_minions_dead(self):
        cur_res = 0
        op_res = 0
        for minion in self.current_player_minions:
            if not minion.isDead:
                cur_res += minion.stats.tier
        for minion in self.opponent_minions:
            if not minion.isDead:
                op_res += minion.stats.tier
        if op_res > 0 and cur_res > 0:
            return False, 0
        else:
            if cur_res > 0:
                return True, cur_res
            else:
                return True, -op_res

    def get_opposing_player(self, player):
        return self.curr_player if self.opponent == player else self.opponent

    def get_next_pair(self):
        attacker_idx = self.current_player_index if self.next_attack == self.curr_player else self.opponent_index
        atacker_minions = self.current_player_minions if self.next_attack == self.curr_player else self.opponent_minions
        victim_minions = self.opponent_minions if self.next_attack == self.curr_player else self.current_player_minions
        return pick_minion_pair(attacker_idx, atacker_minions, victim_minions)
