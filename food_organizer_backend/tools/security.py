from cryptography.fernet import Fernet


def generate_salt():
    return Fernet.generate_key()


def crypt(data, salt):
    f = Fernet(salt)
    return f.encrypt(data.encode())


def decrypt(data, salt):
    f = Fernet(salt)
    return f.decrypt(data).decode()

