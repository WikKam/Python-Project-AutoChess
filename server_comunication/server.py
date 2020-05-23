import socket
from _thread import *
from game_elements.gameElements import Player
import pickle
from game_elements.game_enums import PlayerState
from game_elements.draft_pairs import check_and_draft

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
server = s.getsockname()[0]
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))  # whatever ip to given port
except socket.error as e:
     str(e)

s.listen(4)  # then we can have multiply client connected, 2 people max connected so far
print("Waiting for connection, Server started")
players = [Player(None, 0), Player(None, 1), Player(None, 2), Player(None, 3)]

combat_pair = {
    0: 1,
    1: 0,
    2: 3,
    3: 2
}


def threaded_client(conn, current_player):
    players[current_player].status = PlayerState.connected
    info = players, current_player
    conn.sendall(pickle.dumps(info))
    print(current_player)
    while True:
        try:
            data = pickle.loads(conn.recv(2048 * 8))

            players[current_player] = data
            players_game = players
            check_and_draft(players_game, combat_pair)
            if not data:
                print("Disconnected")
                break
            else:
                if current_player == 1:
                    reply = players_game, combat_pair[1]
                elif current_player == 0:
                    reply = players_game, combat_pair[0]
                elif current_player == 2:
                    reply = players_game, combat_pair[2]
                else:
                    reply = players_game, combat_pair[3]
            conn.sendall(pickle.dumps(reply))
        except:
            break
    print("Lost connection")
    conn.close()

# keep track of connected players
current_player = 0
while True:
    conn, address = s.accept() # what's connected and ip adress
    print("Connected to: ", address)
    start_new_thread(threaded_client, (conn, current_player))
    current_player += 1