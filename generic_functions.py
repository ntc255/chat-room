
HEADER_LENGTH = 10
TYPE_LENGTH = 3

from security import encrypt, decrypt

"""
@params
s: String
socket: Socket
typeof: String
"""
def send_msg(s, socket, typeof='txt'):
    if typeof in ['txt', 'cmd']:
        s1 = typeof + s
        s_body = encrypt(s1.encode('utf-8'))
        s_header = f'{len(s_body):<{HEADER_LENGTH}}'.encode('utf-8')
        # print('EM - ',encrypted_message)
        socket.send(s_header + s_body)
    else:
        raise ValueError('Invalid type input')


"""
@params
client_socket: Socket
"""
def receive_message(client_socket):
    message_header = client_socket.recv(HEADER_LENGTH)
    # print('header - ', message_header)
    if not len(message_header):
        # client closed the connection
        return False
    message_length = int(message_header.decode('utf-8').strip())
    d1 = client_socket.recv(message_length)
    d2 = decrypt(d1)
    # print('received_server- ', d2)
    return message_format(message_header, d2)
    # return {"header": message_header, "data": d2}


"""
@params
header: String
message: String
"""
def message_format(header, message):
    # type - txt, cmd
    return {'header': header, "type":message[:TYPE_LENGTH] ,'data':message[TYPE_LENGTH:]}