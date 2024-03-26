import os.path
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


def pad(data):
    while len(data) % 16 != 0:
        data += '\0'
    return data


class ServerCryptOperator:
    def __init__(self, key_dir):
        # The path to the server's public, private and symmetric key
        self.pub_key_dir = key_dir + "key_pub.txt"
        self.pri_key_dir = key_dir + "key_pri.txt"
        # If the files of asymmetric keys do not exist, create a new key pair
        self.create_asy_keys_for_server()
        # Load public and private keys
        self.pub_key = self.load_asy_key(pub=True)
        self.pri_key = self.load_asy_key(pub=False)

    def create_asy_keys_for_server(self):
        """
        Create asymmetric keys for the server
        :return: A RSA key object
        """
        if os.path.exists(self.pub_key_dir) and os.path.exists(self.pri_key_dir):
            return
        self.create_asy_key(1024)

    def asy_encrypt_data_list(self, data_list, pub_key):
        """
        Encrypt a list of data using an external public key
        :param data_list: The input data list
        :param pub_key: External public key
        :return: A list of ciphers
        """
        cipher_list = []

        for data in data_list:
            cipher_byte = self.asy_data_encryption(data, pub_key)
            cipher_list.append(cipher_byte)

        return cipher_list

    def asy_decrypt_cipher_list(self, cipher_list):
        """
        Decrypt a list of data using the server's private key
        :param cipher_list: The input cipher list
        :return: A list of original data
        """
        plain_list = []

        for cipher_byte in cipher_list:
            plain_text = self.asy_data_decryption(cipher_byte)
            plain_list.append(plain_text)

        return plain_list

    def sym_encrypt_data_list(self, data_list, sym_key):
        """
        Encrypt a list of data using a symmetric key
        :param data_list: The input data list
        :param sym_key: The symmetric key used
        :return: A list of ciphers
        """
        cipher_list = []

        for data in data_list:
            cipher_byte = self.sym_data_encryption(data, sym_key)
            cipher_list.append(cipher_byte)

        return cipher_list

    def sym_decrypt_cipher_list(self, cipher_list, sym_key):
        """
        Decrypt a list of data using a symmetric key
        :param cipher_list: The list of cipher
        :param sym_key: The symmetric key used
        :return: A list of original data
        """
        plain_list = []

        for cipher_byte in cipher_list:
            plain_text = self.sym_data_decryption(cipher_byte, sym_key)
            plain_list.append(plain_text)

        return plain_list

    def create_asy_key(self, length):
        """
        Create a pair of asymmetric keys and store them in txt files
        :param length: The key length
        :return: None
        """
        key = RSA.generate(length)
        pub_key = key.public_key().export_key("PEM")
        pri_key = key.export_key("PEM")
        with open(self.pub_key_dir, "w") as f:
            f.write(pub_key.decode())
        f.close()

        with open(self.pri_key_dir, "w") as f:
            f.write(pri_key.decode())
        f.close()

    def load_asy_key(self, pub=False):
        """
        Load asymmetric keys of the server
        :param pub: Load public key or private key
        :return: The key loaded
        """
        try:
            with open(self.pub_key_dir if pub else self.pri_key_dir, "rb") as f:
                content = f.read()
            key = RSA.importKey(content)
            f.close()
            return key
        except FileNotFoundError:
            print("User keys not founded")
            return None


    @staticmethod
    def asy_data_encryption(plain_text, pub_key):
        """
        Encrypt a single piece of data using an external public key
        :param plain_text: The input data
        :param pub_key: The external public key
        :return: The cipher bytes
        """
        cipher = PKCS1_v1_5.new(pub_key)
        cipher_byte = cipher.encrypt(plain_text.encode() if type(plain_text) == str else plain_text)
        return cipher_byte

    def asy_data_decryption(self, cipher_byte, decode=True):
        """
        Decrypt a single piece of data using server's private key
        :param cipher_byte: The input cipher bytes
        :param decode: Whether decode the decrypted data into str or not
        :return: The decrypted data
        """
        cipher = PKCS1_v1_5.new(self.pri_key)
        plain_byte = cipher.decrypt(cipher_byte, sentinel=None)
        return plain_byte.decode() if decode else plain_byte

    @staticmethod
    def sym_data_encryption(plain_text, sym_key):
        """
        Encrypt a single piece of data using a symmetric key
        :param plain_text: The input data
        :param sym_key: The symmetric key used
        :return: The cipher bytes
        """
        cipher = AES.new(sym_key, AES.MODE_ECB)
        cipher_byte = cipher.encrypt(pad(plain_text).encode() if type(plain_text) == str else plain_text)
        return cipher_byte

    @staticmethod
    def sym_data_decryption(cipher_byte, sym_key):
        """
        Decrypt a single piece of data using a symmetric key
        :param cipher_byte: The input cipher bytes
        :param sym_key: Whe symmetric key used
        :return: The plain text
        """
        cipher = AES.new(sym_key, AES.MODE_ECB)
        plain_byte = cipher.decrypt(cipher_byte)
        return plain_byte.decode().strip("\0")

    @staticmethod
    def create_sym_key(length):
        """
        Generate a symmetric key
        :param length: The key length
        :return: The symmetric key
        """
        sym_key = get_random_bytes(length)
        return sym_key

    def get_pub_key(self):
        """
        Get the public key of the server
        :return: The public key
        """
        return self.pub_key

    def get_pri_key(self):
        """
        Get the private key of the server
        :return: The public key
        """
        return self.pri_key


class UserCryptOperator:
    def __init__(self, key_dir, username):
        # The path to a user's public, private and symmetric key
        self.pub_key_dir = key_dir + username + "_pub.txt"
        self.pri_key_dir = key_dir + username + "_pri.txt"
        self.sym_key_dir = key_dir + username + "_sym.txt"
        # If the files of asymmetric keys do not exist, create a new key pair
        self.create_asy_keys_for_user()
        # Load public and private keys
        self.pub_key = self.load_asy_key(pub=True)
        self.pri_key = self.load_asy_key(pub=False)
        # Only load symmetric key when the file exists
        self.sym_key = None
        if os.path.exists(self.sym_key_dir):
            self.sym_key = self.load_sym_key()

    def create_asy_keys_for_user(self):
        """
        Create asymmetric keys for a user
        :return: A RSA key object
        """
        if os.path.exists(self.pub_key_dir) and os.path.exists(self.pri_key_dir):
            return
        self.create_asy_key(1024)

    def asy_encrypt_data_list(self, data_list, pub_key):
        """
        Encrypt a list of data using an external public key
        :param data_list: The input data list
        :param pub_key: External public key
        :return: A list of ciphers
        """
        cipher_list = []

        for data in data_list:
            cipher_byte = self.asy_data_encryption(data, pub_key)
            cipher_list.append(cipher_byte)

        return cipher_list

    def asy_decrypt_cipher_list(self, cipher_list):
        """
        Decrypt a list of data using the user's private key
        :param cipher_list: The input cipher list
        :return: A list of original data
        """
        plain_list = []

        for cipher_byte in cipher_list:
            plain_text = self.asy_data_decryption(cipher_byte)
            plain_list.append(plain_text)

        return plain_list

    def sym_encrypt_data_list(self, data_list, sym_key):
        """
        Encrypt a list of data using a symmetric key
        :param data_list: The input data list
        :param sym_key: The symmetric key used
        :return: A list of ciphers
        """
        cipher_list = []

        for data in data_list:
            cipher_byte = self.sym_data_encryption(data, sym_key)
            cipher_list.append(cipher_byte)

        return cipher_list

    def sym_decrypt_cipher_list(self, cipher_list, sym_key):
        """
        Decrypt a list of data using a symmetric key
        :param cipher_list: The list of cipher
        :param sym_key: The symmetric key used
        :return: A list of original data
        """
        plain_list = []

        for cipher_byte in cipher_list:
            plain_text = self.sym_data_decryption(cipher_byte, sym_key)
            plain_list.append(plain_text)

        return plain_list

    def create_asy_key(self, length):
        """
        Create a pair of asymmetric keys and store them in txt files
        :param length: The key length
        :return: None
        """
        key = RSA.generate(length)
        pub_key = key.public_key().export_key("PEM")
        pri_key = key.export_key("PEM")
        with open(self.pub_key_dir, "wb") as f:
            f.write(pub_key)
        f.close()

        with open(self.pri_key_dir, "wb") as f:
            f.write(pri_key)
        f.close()

    def store_sym_key(self, sym_key):
        """
        Store the input symmetric key in a txt file
        :param sym_key: The symmetric key
        :return: None
        """
        self.sym_key = sym_key
        with open(self.sym_key_dir, "wb") as f:
            f.write(sym_key)
        f.close()

    def load_asy_key(self, pub=False):
        """
        Load asymmetric keys of the user
        :param pub: Load public key or private key
        :return: The key loaded
        """
        try:
            with open(self.pub_key_dir if pub else self.pri_key_dir, "rb") as f:
                content = f.read()
            key = RSA.importKey(content)
            f.close()
            return key
        except FileNotFoundError:
            print("User keys not founded")
            return None

    def load_sym_key(self):
        """
        Load asymmetric keys of the user
        :return: The key loaded
        """
        try:
            with open(self.sym_key_dir, "rb") as f:
                key = f.read()
            f.close()
            return key
        except FileNotFoundError:
            print("User keys not founded")
            return None

    @staticmethod
    def asy_data_encryption(plain_text, pub_key):
        """
        Encrypt a single piece of data using an external public key
        :param plain_text: The input data
        :param pub_key: The external public key
        :return: The cipher bytes
        """
        cipher = PKCS1_v1_5.new(pub_key)
        cipher_byte = cipher.encrypt(plain_text.encode() if type(plain_text) == str else plain_text)
        return cipher_byte

    def asy_data_decryption(self, cipher_byte, decode=True):
        """
        Decrypt a single piece of data using user's private key
        :param cipher_byte: The input cipher bytes
        :param decode: Whether decode the decrypted data into str or not
        :return: The decrypted data
        """
        cipher = PKCS1_v1_5.new(self.pri_key)
        plain_byte = cipher.decrypt(cipher_byte, sentinel=None)
        return plain_byte.decode() if decode else plain_byte

    @staticmethod
    def sym_data_encryption(plain_text, sym_key):
        """
        Encrypt a single piece of data using a symmetric key
        :param plain_text: The input data
        :param sym_key: The symmetric key used
        :return: The cipher bytes
        """
        cipher = AES.new(sym_key, AES.MODE_ECB)
        cipher_byte = cipher.encrypt(pad(plain_text).encode() if type(plain_text) == str else plain_text)
        return cipher_byte

    @staticmethod
    def sym_data_decryption(cipher_byte, sym_key):
        """
        Decrypt a single piece of data using a symmetric key
        :param cipher_byte: The input cipher bytes
        :param sym_key: Whe symmetric key used
        :return: The plain text
        """
        cipher = AES.new(sym_key, AES.MODE_ECB)
        plain_byte = cipher.decrypt(cipher_byte)
        return plain_byte.decode().strip("\0")

    @staticmethod
    def create_sym_key(length):
        """
        Generate a symmetric key
        :param length: The key length
        :return: The symmetric key
        """
        sym_key = get_random_bytes(length)
        return sym_key

    def get_pub_key(self):
        """
        Get the public key of the user
        :return: The public key
        """
        return self.pub_key

    def get_pri_key(self):
        """
        Get the private key of the user
        :return: The private key
        """
        return self.pri_key
