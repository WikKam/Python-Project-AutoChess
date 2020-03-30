import socket
from _thread import *
import sys

server = "192.168.0.113"  # local host  cmd -> ipconfig -> IPv4 Address 192.168.0.113
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))  # whatever ip to given port
except socket.error as e:
    str(e)

s.listen(2)  # then we can have multiply client connected, 2 people max connected so far
print("Waiting for connection, Server started")


def threaded_client(conn):
    conn.send(str.encode("Connected"))
    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                print("Disconnected")
                break
            else:
                print("Received: ", reply)
                print("Sending : ", reply)

            conn.sendall(str.encode(reply))
        except:
            break

    print("Lost connection")
    conn.close()


while True:
    conn, address = s.accept() # what's connected and ip adress
    print("Connected to: ", address)

    start_new_thread(threaded_client, (conn,))