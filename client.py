import socket
import select
import errno
import sys


HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

my_username = input('Username: ')
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
# received functionality will not be blocking 
client_socket.setblocking(False)

def send_msg(s):
    s_body = s.encode('utf-8')
    s_header = f'{len(s_body):<{HEADER_LENGTH}}'.encode("utf-8")
    client_socket.send(s_header + s_body)

def receive_msg():
    s_header = client_socket.recv(HEADER_LENGTH)
    if not len(s_header):
        return -1
    s_length = int(s_header.decode('utf-8').strip())
    s = client_socket.recv(s_length).decode('utf-8')
    return s

username = my_username.encode('utf-8')
# username_header = f'{len(username):<{HEADER_LENGTH}}'.encode("utf-8")
# client_socket.send(username_header + username)
send_msg(my_username)

while True:
    message = input(f"{my_username} > ")
    if message:
        send_msg(message)
    
    try:
        while True:
            # receive things
            username = receive_msg()
            if username == -1:
                print('connection closed by the server')
                sys.exit()
            message =  receive_msg()
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