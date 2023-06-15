from cryptography.fernet import Fernet
from datetime import datetime
from .various import tokenToDictionary


def generate_salt():
    return Fernet.generate_key()


def crypt(data, salt):
    f = Fernet(salt)
    return f.encrypt(data.encode())


def decrypt(data, salt):
    f = Fernet(salt)
    return f.decrypt(data).decode()


def checkToken(token, users):
    tokenDict = tokenToDictionary(token)
    index = 0
    while index < len(users):
        if int(tokenDict["id"]) == users[index]["id"]:
            username = users[index]["username"] == tokenDict["username"]
            email = users[index]["email"] == tokenDict["email"]
            password = users[index]["password"] == tokenDict["password"]
            created_at = users[index]["created_at"][0:13] == tokenDict["created_at"]
            auth_from = users[index]["auth_from"][0:13] == tokenDict["auth_from"]
            auth_until = users[index]["auth_until"][0:13] == tokenDict["auth_until"]

            if username and email and password and created_at and auth_from and auth_until:
                print("passed")
                if users[index]["auth_from"] < (datetime.now().strftime("%Y/%m/%d %H:%M:%S")).replace(" ", "T").replace("/", "-") and users[index]["auth_until"] > (datetime.now().strftime("%Y/%m/%d %H:%M:%S")).replace(" ", "T").replace("/", "-"):
                    return int(tokenDict["id"])
                else:
                    return 0
            else:
                print("not passed")
                return 0
        else:
            index += 1
    return 0
