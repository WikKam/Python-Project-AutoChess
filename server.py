import socket
from _thread import *
from gameElements import Minion, Player, Hero
from gameElements import Tribe
from gameElements import State
from gameElements import Stats
import static_resources as sr
import pickle

server = "192.168.1.108"  # local host  cmd -> ipconfig -> IPv4 Address   192.168.1.103
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
    conn.send(pickle.dumps(players[current_player])) # send to player
    print(current_player)
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[current_player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if current_player == 1:
                    reply = players[0]
                else:
                    reply = players[1]

                # print("Received: ", data, " ", current_player)
                # print("Sending : ", reply)
                # if players[0].ge_hero() is not None:
                #     print(players[0].get_hero().get_minions())
                # if players[1].ge_hero() is not None:
                #     print(players[1].get_hero().get_minions())
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