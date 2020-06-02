import socket
import select
import errno
import sys
from generic_functions import send_msg, receive_msg

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

my_username = input('Username: ')
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
# received functionality will not be blocking 
client_socket.setblocking(False)



username = my_username.encode('utf-8')
# username_header = f'{len(username):<{HEADER_LENGTH}}'.encode("utf-8")
# client_socket.send(username_header + username)
send_msg(my_username, client_socket)

while True:
    message = input(f"{my_username} > ")
    if message:
        send_msg(message, client_socket)
    
    try:
        while True:
            # receive things
            username = receive_msg(client_socket)
            if username == -1:
                print('connection closed by the server')
                sys.exit()
            message =  receive_msg(client_socket)
            print(f"{username} > {message}")

    except IOError as e:
        # error we might see depending on OS when their are no more messages to receive
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print("Reading Error", str(e))
            sys.exit()
        continue

    except Exception as e:
        print("General Error", str(e))
        sys.exit()