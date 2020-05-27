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
    if target.stats.health <= 0:
        target.is_dead = True


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
    if attacker_idx >= 0:
        if attacker_minions[attacker_idx].is_dead:
            attacker_idx = find_next_living_minion_index(attacker_idx, attacker_minions)
        if len(attacker_minions) > attacker_idx >= 0:
            if len(victim_minions) > attacker_idx and \
                    not victim_minions[attacker_idx].is_dead:
                return attacker_minions[attacker_idx], victim_minions[attacker_idx]
            else:
                for minion in victim_minions:
                    if not minion.is_dead:
                        return attacker_minions[attacker_idx], minion
    return None, None


def find_next_living_minion_index(index, minions):
    iterations = 0
    if len(minions) > 0:
        while iterations <= len(minions):
            index = (index + 1) % len(minions)
            iterations += 1
            if not minions[index].is_dead:
                return index
    return -1


class Combat:
    def __init__(self, current_player_minions, opponent_minions, curr_player, opponent):
        self.current_player_minions = current_player_minions
        self.opponent_minions = opponent_minions
        self.current_player_index = find_next_living_minion_index(-1, current_player_minions)
        self.opponent_index = find_next_living_minion_index(-1, opponent_minions)
        self.curr_player = curr_player
        self.opponent = opponent
        self.next_attack = self.curr_player if self.curr_player.attack_turn == AttackTurn.attack_first else self.opponent
        resolve_attack_turns(self.curr_player, self.opponent)

    def current_player_attack(self):
        attacker, victim = pick_minion_pair(self.current_player_index, self.current_player_minions,
                                            self.opponent_minions)
        if victim is None or attacker is None: return
        perform_attack(attacker, victim)
        is_minion_dead(victim)
        self.current_player_index = find_next_living_minion_index(self.current_player_index, self.current_player_minions)

    def opponent_attack(self):
        attacker, victim = pick_minion_pair(self.opponent_index, self.opponent_minions,
                                            self.current_player_minions)
        if victim is None or attacker is None: return
        perform_attack(attacker, victim)
        is_minion_dead(victim)
        self.opponent_index = find_next_living_minion_index(self.opponent_index,self.opponent_minions)

    def check_if_all_minions_dead(self):
        cur_res = 0
        op_res = 0
        for minion in self.current_player_minions:
            if not minion.is_dead:
                cur_res += minion.stats.tier
        for minion in self.opponent_minions:
            if not minion.is_dead:
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
        ret1, ret2 = pick_minion_pair(attacker_idx, atacker_minions, victim_minions)
        return ret1, ret2

    def do_attack(self):
        if self.curr_player == self.next_attack:
            self.current_player_attack()
        else:
            self.opponent_attack()
        self.next_attack = self.get_opposing_player(self.next_attack)
