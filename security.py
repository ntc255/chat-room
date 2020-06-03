from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


"""
@note
It generate keys and save in the folder name keys/
"""
def generate():
    import os
    files = [name for name in os.listdir(".") if os.path.isdir(name)]
    if 'keys' in files:
        pass
    else:
        os.system('mkdir keys')
    key = RSA.generate(2048)
    f = open('keys/rsa_public.pem', 'wb')
    f.write(key.publickey().exportKey('PEM'))
    f.close()
    f = open('keys/rsa_private.pem', 'wb')
    f.write(key.exportKey('PEM'))
    f.close()


"""
@params
message: b'String
@return
crypt_message: b'String 
"""
def encrypt(message):
    # send encoded data
    with open('keys/rsa_public.pem') as f:
        public_key = RSA.importKey(f.read())
        cipher = PKCS1_OAEP.new(public_key)
        crypt_message = cipher.encrypt(message)
        # print(crypt_message)
        return crypt_message


"""
@params
crypt_message: b'String
@return
message: b'String 
"""
def decrypt(crypt_message):
    # return byte data need to be decoded
    with open('keys/rsa_private.pem') as f:
        private_key = RSA.importKey(f.read())
        cipher = PKCS1_OAEP.new(private_key)
        # cipher = private_key
        message = cipher.decrypt(crypt_message)
        return message

# generate()
def main():
    while 1:
        s = input()
        print('MESSAGE - ', s)
        es = encrypt(s.encode('utf-8'))
        print('ENCRYPTION - ', es)
        ds = decrypt(es).decode('utf-8')
        print("DECRYPTION - ", ds)
# main()