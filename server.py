import socket
import select
from generic_functions import receive_message_server, send_msg, message_format


def start(IP, PORT):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # allows to reconnect
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((IP, PORT))

    return server_socket


def broadcast(user, message, left=set()):
    for client_socket in clients:
        if client_socket not in left:
            send_msg(user['data'].decode('utf-8'), client_socket)
            send_msg(message['data'].decode('utf-8'), client_socket)
            # send_server(user['header']+user['data']+message['header']+message['data'], client_socket)


def new_connection():
    client_socket, client_address = server_socket.accept()
    print('NEW Connection enstablishing')
    user = receive_message_server(client_socket)
    if user is False:
        print('IN false')
        return
    try:
        user['data'].decode('utf-8')
    except UnicodeDecodeError as e:
        print("Unauthorized user tried to access")
        return
    socket_list.append(client_socket)
    clients[client_socket] = user
    print('ACCEPTED new connection from {}:{} username {}'.format(client_address[0], client_address[1], user['data'].decode('utf-8')))


def remove_client(notified_socket):
    user = clients[notified_socket]
    message = message_format(''.encode('utf-8'), f'{user["data"].decode("utf-8")} has left. '.encode('utf-8'))
    broadcast(user, message, {notified_socket})
    socket_list.remove(notified_socket)
    del clients[notified_socket]

# ---------------------- main program ---------------------------#


HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234
server_socket = start(IP, PORT)
server_socket.listen()
socket_list = [server_socket]

clients = {}



while True:
    read_sockets, _, exception_sockets = select.select(socket_list, [], socket_list)
    # (read_list, write_list, error_list)
    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            # Someone just connected
            new_connection()
        else:
            # message received
            message = receive_message_server(notified_socket)
            if message is False:
                # connection ended.
                print('Closed connection from {}'.format(clients[notified_socket]['data'].decode('utf-8')))
                remove_client(notified_socket)
                continue
            user = clients[notified_socket]
            print('RECEIVED message from {}: {}'.format(user['data'].decode('utf-8'), message['data'].decode('utf-8')))
            broadcast(user, message, {notified_socket})
    
    # remove non answering clients
    for notified_socket in exception_sockets:
        remove_client(notified_socket)





