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


def perform_attac(attacker, target):
    target.stats.health -= attacker.stats.attack


class Combat:
    def __init__(self, current_player_minions, opponent_minions):
        self.current_player_minions = current_player_minions
        self.opponent_minions = opponent_minions
        self.current_player_index = 0
        self.opponent_index = 0

    def current_player_attack(self):
        if len(self.opponent_minions) > self.current_player_index and \
                not self.opponent_minions[self.current_player_index].isDead:
            perform_attac(self.current_player_minions[self.current_player_index],
                               self.opponent_minions[self.current_player_index])
            is_minion_dead(self.opponent_minions[self.current_player_index])
        else:
            for minion in self.opponent_minions:
                if not minion.isDead:
                    perform_attac(self.current_player_minions[self.current_player_index], minion)
                    is_minion_dead(minion)
                    break
        self.current_player_index = (self.current_player_index + 1) % len(self.current_player_minions)

    def opponent_attack(self):
        if len(self.current_player_minions) > self.opponent_index and \
                not self.current_player_minions[self.opponent_index].isDead:
            perform_attac(self.opponent_minions[self.opponent_index],
                               self.current_player_minions[self.opponent_index])
            is_minion_dead(self.current_player_minions[self.opponent_index])
        else:
            for minion in self.current_player_minions:
                if not minion.isDead:
                    perform_attac(self.opponent_minions[self.opponent_index], minion)
                    is_minion_dead(minion)
                    break
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
