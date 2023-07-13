import sys
import socket
import threading
from Source.Views.TalkBox import TalkBox


class Client:

    __BUFFER = 1024
    __FORMAT = "utf-8"
    __PORT = 9000
    __HOST = socket.gethostbyname(socket.gethostname())
    __SERVER = (__HOST, __PORT)

    def __init__(self, username):
        self.__connected = False
        self.__welcomescreen = None
        self.__receive_thread = threading.Thread(target=self.__receive_message)
        self.__chat = TalkBox()
        self.__logged_user = username
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__connect_to_server()
        self.__validate_user(self.__logged_user)

    def __connect_to_server(self):
        try:
            self.__client.connect(self.__SERVER)
        except ConnectionRefusedError:
            print("Unable to connect to the server.")
            sys.exit()

    def __validate_user(self, username):
        try:
            self.__client.send(username.encode(self.__FORMAT))
            if self.__client.recv(self.__BUFFER).decode(self.__FORMAT) == "Valid":
                self.__connected = True
                pass
        except OSError:
            print("Server is offline")
            sys.exit()

    def __send_message(self):
        pass
