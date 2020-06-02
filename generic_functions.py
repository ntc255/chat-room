
HEADER_LENGTH = 10

from security import encrypt, decrypt

def send_msg(s, socket):
    s_body = encrypt(s.encode('utf-8'))
    s_header = f'{len(s_body):<{HEADER_LENGTH}}'.encode('utf-8')
    # print('EM - ',encrypted_message)
    socket.send(s_header + s_body)

def receive_msg(socket):
    s_header = socket.recv(HEADER_LENGTH)
    if not len(s_header):
        return -1
    s_length = int(s_header.decode('utf-8').strip())
    s = socket.recv(s_length)
    decrypted_message = decrypt(s)
    return decrypted_message.decode('utf-8')


def receive_message_server(client_socket):
    try:
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
    except Exception as e:
        print('error found', str(e))
        return False

def message_format(header, message):
    return {'header': header, 'data':message}