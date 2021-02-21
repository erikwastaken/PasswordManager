from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Encoder():
    @staticmethod
    def generate_key():
        key = Fernet.generate_key()
        return key

    @staticmethod
    def get_key_for_input(ip):
        encoded_input = ip.encode() #convert to type bytes
        salt = b'salt_' #for testing
        kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(encoded_input))
        return key

    def __init__(self,key):
        self.key = key

    def encrypt(self,message):
        f = Fernet(self.key)
        encrypted = f.encrypt(message.encode())
        return encrypted.decode('utf-8')

    def decrypt(self,message):
        f = Fernet(self.key)
        decrypted = f.decrypt(message.encode())
        return decrypted.decode('utf-8')

if __name__ == '__main__':
    key = Encoder.get_key_for_input('test')
    print(key)
    encryptor = Encoder(key)
    print(encryptor.encrypt('blablablablabla'))
    print(len(encryptor.encrypt('blablablablabla')))
    
