# standard library
import socket, select, errno, sys, os
from threading import Thread
# Thread(target=client_thread, args=(...,..)).start()

# userdefined library
from generic_functions import send_msg, receive_message, isACK, isNAK
from constant_val import HEADER_LENGTH, NAME_LENGTH


# ----------------- client functions ------------------------#
# WAIT act a  lock for ack or nak
WAIT = False


"""
@params
IP: String
PORT: String
username: String
@return
client_socket: Socket 
"""
def start(IP, PORT, username):
    global WAIT
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(5)
    client_socket.connect((IP, PORT))
    # received functionality will not be blocking 
    client_socket.setblocking(0)
    ch = send_msg(username, client_socket, 'txt')
    if ch==False:
        print('Unable to connect')
        sys.exit()
    WAIT = True
    # everything is setup now 
    return client_socket


"""
@params
username: String
client_socket: Socket
@return
type: Int
1 means need to ask for acknowledgement.
0 means no ack needed. 
"""
def sending_messages(username, client_socket):
    global WAIT
    if not WAIT:
        message = input(f"{username} > ")
        if message:
            if message == 'cmd()':
                username = input("Enter user to send: ")
                command = input("\t>> ")
                msg = f'{username:<{NAME_LENGTH}}' + command
                print(f'Sending command - {command} to {username}')
                ch = send_msg(msg, client_socket, 'cmd')
                if ch== False:return 0 
            elif message == 'quit()':
                client_socket.close()
                sys.exit()
            else:
                ch = send_msg(message, client_socket, 'txt')
                if ch==False:
                    return 0
            WAIT = True
            return 1
    return 0


"""
@params
command: String
"""
def run_command(command):
    print(f'You have received a command - {command}')
    choose = input('y(accept)/any key (decline): ')
    if choose == 'y':
        os.system(command)
    else:
        pass
    

"""
@params
client_socket: Socket
@return
type: Int
1 ack received
2 nak received
0 no ack received 
"""
def receiving_messages(client_socket):
    global WAIT
    # no ack=0 means no need to send ack by client to server
    username = receive_message(client_socket, 0)
    if username == False :
        print('connection closed by the server')
        sys.exit()
    if WAIT:
        if username['type'].decode('utf-8') == 'txt':
            if isACK(username['data']):
                return 1
            if isNAK(username['data']):
                return 2
        else:
            raise ValueError('Expecting a ACK')
    else:
        if username['type'].decode('utf-8')=='txt':
            message =  receive_message(client_socket, 0)
            print(f"{username['data'].decode('utf-8')} > {message['data'].decode('utf-8')}")
            sys.stdout.flush()
        elif username['type'].decode('utf-8')=='cmd':
            command = username['data'].decode('utf-8')
            run_command(command)
        else:
            print('INVALID INPUT')
    return 0


"""
@params
client_socket: Socket
"""
def receive_client(client_socket):
    global WAIT
    # if ack=1 : expecting an acknowledgement
    # print('Client ack - ', + WAIT)
    try:
        while True:
            # receive things
            chk = receiving_messages(client_socket)
            # print('Client 2 - ', chk)
            if WAIT:
                if chk :
                    if chk==1:
                        pass
                        # print('ack received')
                    else:
                        print('nak received')
                        sys.exit()
                        
                    WAIT = False
                else:
                    raise ValueError('NO acknowlegement received')
    except IOError as e:
        # error we might see depending on OS when their are no more messages to receive
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print("Reading Error", str(e))
            sys.exit()
        return

    except Exception as e:
        print("General Error", str(e))
        sys.exit()


def header(username):
    print(f'{"*"*70}\n {"welcome "+username:^70} \n{"*"*70}\n')
    print('Operations-:')
    print('- write any things as a text')
    print('- write cmd() than in next two lines user and command\n')


# ----------------- main program --------------#

def main():
    
    IP = "127.0.0.1"
    PORT = 1234

    username = input('Username: ')
    client_socket = start(IP, PORT, username)
    
    header(username)
    while True:
        receive_client(client_socket)
        # Thread(target=sending_messages, args=(username, client_socket)).start()
        sending_messages(username, client_socket)
        # Thread(target=receive_client, args=(client_socket, )).start()
        


if __name__ == "__main__":
    main()