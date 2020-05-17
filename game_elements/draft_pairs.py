from game_elements.gameElements import PlayerState
import random


def check_and_draft(players, pairs):
    count_deads = []
    for player in players:
        if player.status in (PlayerState.in_combat, PlayerState.in_shop, PlayerState.connected,
                             PlayerState.not_connected):
            return
        if player.status == PlayerState.dead:
            count_deads.append(player.id)

    if len(count_deads) >= 2:
        return #TODO
    else:
        random_opponent = random.randint(1, 3)
        random_opponent = random.randint(1, 3) if random_opponent == pairs[0] else random_opponent

        pairs[0] = random_opponent
        pairs[random_opponent] = 0
        if random_opponent == 1:
            pairs[2] = 3
            pairs[3] = 2
        elif random_opponent == 2:
            pairs[1] = 3
            pairs[3] = 1
        else:
            pairs[1] = 2
            pairs[2] = 1

