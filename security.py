from Crypto.PublicKey import RSA

def generate():
    import os
    files = [name for name in os.listdir(".") if os.path.isdir(name)]
    if 'keys' in files:
        pass
    else:
        os.system('mkdir keys')
    key = RSA.generate(4096)
    f = open('keys/rsa_public.pem', 'wb')
    f.write(key.publickey().exportKey('PEM'))
    f.close()
    f = open('keys/rsa_private.pem', 'wb')
    f.write(key.exportKey('PEM'))
    f.close()

def encrypt(message):
    # send encoded data
    with open('keys/rsa_public.pem', 'rb') as f:
        public_key = RSA.importKey(f.read())
        crypt_message = public_key.encrypt(message,32)
        return crypt_message[0]

def decrypt(crypt_message):
    # return byte data need to be decoded
    with open('keys/rsa_private.pem', 'rb') as f:
        private_key = RSA.importKey(f.read())
        message = private_key.decrypt(crypt_message)
        return message

# generate()
def main():
    while 1:
        s = input()
        print('MESSAGE - ', s)
        es = encrypt(s)
        print('ENCRYPTION - ', es)
        ds = decrypt(es)
        print("DECRYPTION - ", ds)
# main()