import client
import time
import generic_functions

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

max_user = 10

clients = []
for idx in range(max_user):
    username = f'user{idx}'
    clients.append([client.start(IP, PORT, username), username])
    time.sleep(2)

while True:
    time.sleep(1)
    for socket, username in clients:
        generic_functions.send_msg(str(time.time_ns()), socket)
        time.sleep(2)
    
    for socket, username in clients:
        socket.close()
    break



