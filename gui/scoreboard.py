def draw_scoreboard(players, curren_player):
    scoreboard = []
    for player in players:
        if player.get_hero() is None:
            return
        scoreboard.append((player.id, player.get_hero().current_hp, player.get_hero().icon))
    scoreboard.sort(key=lambda x: x[1], reverse = True)
    print("SCOREBOARD: ", scoreboard)
