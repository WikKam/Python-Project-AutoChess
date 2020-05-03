import socket
from _thread import *
from game_elements.gameElements import Player
import pickle

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
server = s.getsockname()[0]
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))  # whatever ip to given port
except socket.error as e:
     str(e)

s.listen(2)  # then we can have multiply client connected, 2 people max connected so far
print("Waiting for connection, Server started")
players = [Player(None, 0), Player(None, 1)]


def threaded_client(conn, current_player):
    players[current_player].ready = True
    info = players, current_player
    conn.sendall(pickle.dumps(info))
    print(current_player)
    while True:
        try:
            data = pickle.loads(conn.recv(2048 * 16))

            players[current_player] = data
            players_game = players

            if not data:
                print("Disconnected")
                break
            else:
                if current_player == 1:
                    reply = players_game, 0
                else:
                    reply = players_game, 1
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