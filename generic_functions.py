# standard library
import time
from threading import Thread
# Thread(target=client_thread, args=(...,..)).start()

# user defined library
from security import encrypt, decrypt
from constant_val import HEADER_LENGTH, NAME_LENGTH, TYPE_LENGTH


# Function begin

def isACK(message):
    msg = message.decode('utf-8')
    if msg == 'ACK':
        return True
    return False


def isNAK(message):
    msg = message.decode('utf-8')
    if msg == 'NAK':
        return True
    return False


def sendACK(socket):
    send_msg('ACK', socket, ack = 1)


"""
@params
s: String
socket: Socket
typeof: String
"""
def send_msg(s, socket, typeof='txt', ack=0):
    if typeof in ['txt', 'cmd']:
        s1 = typeof + s
        s_body = encrypt(s1.encode('utf-8'))
        s_header = f'{len(s_body):<{HEADER_LENGTH}}'.encode('utf-8')
        # print('EM - ',encrypted_message)
        socket.send(s_header + s_body)
        # if ack==0:
        #     # wait for acknowledgement
        #     print('waiting for ack')
        #     Thread(target=waitACK, args=(socket,)).start()
    else:
        raise ValueError('Invalid type input')


"""
@params
client_socket: Socket
"""
def receive_message(client_socket, ack=1):
    message_header = client_socket.recv(HEADER_LENGTH)
    # print('header - ', message_header)
    if not len(message_header):
        # client closed the connection
        return False
    message_length = int(message_header.decode('utf-8').strip())
    d1 = client_socket.recv(message_length)
    d2 = decrypt(d1)
    # print('received_server- ', d2)
    msg = message_format(message_header, d2)
    if ack:
        # send an acknowlegement
        # print('send ack')
        sendACK(client_socket)
        
    return msg
    # return {"header": message_header, "data": d2}


"""
@params
header: String
message: String
"""
def message_format(header, message):
    # type - txt, cmd
    return {'header': header, "type":message[:TYPE_LENGTH] ,'data':message[TYPE_LENGTH:]}