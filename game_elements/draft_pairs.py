from game_elements.gameElements import PlayerState
import random


def check_and_draft(players, pairs):
    players_alive = []
    for player in players:
        if player.status == PlayerState.after_combat:
            players_alive.append(player.id)
        if player.status in (PlayerState.in_combat, PlayerState.in_shop, PlayerState.connected,
                             PlayerState.not_connected):
            return

    if len(players_alive) == 2:
        pairs[players_alive[0]] = players_alive[1]
        pairs[players_alive[1]] = players_alive[0]
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

