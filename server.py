import socket, select


from generic_functions import receive_message, send_msg, message_format
from constant_val import HEADER_LENGTH, NAME_LENGTH


# ------------ server functions ----------------------------------#

"""
@params
IP: String
PORT: String
@return
server_socket: Socket 
"""
def start(IP, PORT):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # allows to reconnect
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((IP, PORT))

    return server_socket


"""
@params
user: Dict{key: b'String}
message: Dict{key: b'String}
"""
def broadcast(user, message, left=set()):
    for client_socket in clients:
        if client_socket not in left:
            send_msg(user['data'].decode('utf-8'), client_socket, 'txt')
            send_msg(message['data'].decode('utf-8'), client_socket, 'txt')
            # send_server(user['header']+user['data']+message['header']+message['data'], client_socket)


"""
@params
"""
def new_connection():
    client_socket, client_address = server_socket.accept()
    # print('NEW Connection enstablishing')
    user = receive_message(client_socket)
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


"""
@params
notified_socket: Socket
"""
def remove_client(notified_socket):
    user = clients[notified_socket]
    message = message_format(''.encode('utf-8'), f'txt{user["data"].decode("utf-8")} has left. '.encode('utf-8'))
    broadcast(user, message, {notified_socket})
    socket_list.remove(notified_socket)
    del clients[notified_socket]


"""
@params
username: String
@return
client: Socket
"""
def find_user(username):
    for client in clients:
        if username == clients[client]['data']:
            return client
    return False


"""
@params
notified_socket: Socket

"""
def message_received(notified_socket):
    message = receive_message(notified_socket)
    if message is False:
        # connection ended.
        print('Closed connection from {}'.format(clients[notified_socket]['data'].decode('utf-8')))
        remove_client(notified_socket)
        return

    user = clients[notified_socket]
    print('RECEIVED message from {}: {}'.format(user['data'].decode('utf-8'), message['data'].decode('utf-8')))
    typeof = message['type'].decode('utf-8')
    if typeof=='txt':    
        broadcast(user, message, {notified_socket})
    elif typeof=='cmd':
        username = message['data'][:NAME_LENGTH].strip()
        command = message['data'][NAME_LENGTH:]
        sendto = find_user(username)
        # print(f'command - {username}, with {command}')
        if sendto == False:
            print(f'No such user: {username.decode("utf-8")} found')
        else:
            # print('send to ', sendto)
            send_msg(command.decode('utf-8'), sendto, 'cmd')
    else:
        print(f'INVALID INPUT by {user["data"]} message - {message}')





# ---------------------- main program ---------------------------#



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
            message_received(notified_socket)
    # remove non answering clients
    for notified_socket in exception_sockets:
        remove_client(notified_socket)





