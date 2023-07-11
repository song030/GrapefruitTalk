import socket
import datetime
import threading
from PyQt5 import QtWidgets
import sys
import pickle
from Views.UI_MainWidget import Ui_MainWidget
from Views.DialogWarning import Ui_DlgWarning
from Views.TalkBox import TalkBox
from Views.DateLine import DateLine


class Client(Ui_MainWidget):
    """메인 윈도우에서 상속받아 채팅방을 보여준고 기능들을 서버에 연결해 준다.
    사용자에게 메세지를 받고 다른 클라이언트들에게 정보를 받고 보내주는 기능을 한다."""

    __FORMAT = "utf-8"  # utf-8
    __BUFFER = 4000
    __PORT = 1121
    __HOST = '10.10.20.103'  # socket.gethostbyname(socket.gethostname()) #'10.10.20.103' #socket.gethostbyname(socket.gethostname())
    print('호스트: ', __HOST, '포트주소: ', __PORT, '버퍼: ', __BUFFER)
    __SERVER = (__HOST, __PORT)  # 호스트와 포트 주소를 __SEVER 변수에 저장한다.

    def __init__(self, MainWindow, username):
        self.__connected = False
        self.__welcomescreen = None
        self.__receive_thread = threading.Thread(target=self.__receive_message)
        self.__chatroom = MainWindow
        self.__logged_user = username
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__connect_to_server()
        self.__validate_user(self.__logged_user)

    def __connect_to_server(self):
        """서버 소켓에 연결한다."""

        try:
            self.__client.connect(self.__SERVER)

        except ConnectionRefusedError:
            print("서버에 연결할 수 없습니다.")
            sys.exit()

    def __validate_user(self, username):
        """서버로 보내어 username이 유효한지 확인한다. 유효하면 채팅방을 보여준다.
           :param str username: 클라이언트에서 제출한 username
           :raises OSError: 서버가 오프라인 상태이므로 클라이언트가 메시지를 보낼 수 없습니다.
        """

        try:
            self.__client.send(username.encode(self.__FORMAT))
            if self.__client.recv(self.__BUFFER).decode(self.__FORMAT) == "Valid":  # 서버가 username을 유효하게 선언하는 경우.
                self.__connected = True
                self.setupUi(self.__chatroom)
                # self.__chatroom.setWindowTitle("ChatRoom")
                self.__chatroom.btn_send.clicked.connect(self.__send_message)
                # self.disconnect_button.clicked.connect(self.__disconnect)
                # self.__chatroom.show()
                # self.__chatroom.textBrowser.append("채팅방에 참여하였습니다.")
                self.__receive_thread.start()

            else:
                self.__show_welcomescreen()

        except(OSError):  # 서버 파일이 실행되지 않아 클라이언트가 메시지를 보낼 수 없습니다.
            print("서버가 오프라인 상태입니다.")
            sys.exit()

    def __send_message(self):
        """클라이언트에서 서버로 메시지를 보낸다.
           :raises ConnectionResetError: 서버 파일이 중지되었지만 클라이언트가 메시지를 보내려고 시도합니다.
        """
        print('메세지가 타요')
        # message = self.edt_txt.toPlainText().strip()
        message = self.__chatroom.edt_txt.text()
        print('유저가 작성한 메세지', message)
        if len(message) > 0:  # message가 비어 있지 않은 경우
            try:
                message_date = datetime.datetime.now()
                self.__client.send(message.encode(self.__FORMAT))

                # 메세지 추가
                self.add_date_line()
                talkbox = TalkBox('', self.__logged_user, message, message_date)
                self.__chatroom.layout_talk.addLayout(talkbox.layout)

                # self.__chatroom.textBrowser.append(
                #     f"{self.__logged_user}: " + message + " - " + message_date.strftime(" %x %I:%M %p"))
                # self.textBrowser.append(">YOU: " + message + " - " + message_date.strftime(" %x %I:%M %p"))

            except(ConnectionResetError):  # 서버가 실행되지 않았지만 클라이언트가 메시지를 보내려고 시도합니다.
                # self.textBrowser.append("서버가 현재 오프라인 상태입니다.")
                # self.__chatroom.textBrowser.append("서버가 현재 오프라인 상태입니다.")
                pass

    def add_date_line(self):
        """날짜를 생성한다"""
        talkbox = DateLine(datetime.datetime.now())
        self.__chatroom.layout_talk.addLayout(talkbox.layout)

    def __receive_message(self):
        """
        각각 다른 스레드에서 있는 서버에서 메세지를 받기 위한 역할을 한다.
        메세지는 서버에서 받아지고 첫번째로 피클 모듈을 사용하여 리스트 형식으로 변형된다.
        이 리스트는 채팅방에 있는 모든 클라이언트에게 보내진다.
        """

        try:
            while self.__connected:  # 무한 루프를 사용하여 메시지를 계속 수신한다.
                message = self.__client.recv(self.__BUFFER)
                print('메세지는', message)
                if message:
                    try:
                        connected_users = pickle.loads(message)  # 나중에 pickle -> sqlite
                        self.connected_clients.clear()
                        for name in connected_users:
                            self.connected_clients.addItem(name)

                    except:
                        # self.textBrowser.append(message.decode(self.__FORMAT))
                        # self.textBrowser.append(message.decode('ISO-8859-1'))
                        self.add_date_line()
                        talkbox = TalkBox('', self.__logged_user, str(message), datetime.datetime.now())
                        self.__chatroom.layout_talk.addLayout(talkbox.layout)


        except(ConnectionAbortedError, ConnectionResetError):
            pass

    def __disconnect(self):
        """클라이언트가 연결을 종료할 때 실행되는 함수."""

        # self.__client.send("exit".encode(self.__FORMAT))
        try:
            self.__client.send('DISCONNECT'.encode(self.__FORMAT))
        except(ConnectionResetError):
            pass
        self.__client.close()
        self.__show_welcomescreen()

    def __show_welcomescreen(self):
        """Username이 유효하지 않을 때 실행되는 함수."""
        # from Client.welcome import WelcomeScreen
        self.chatroom.destroy()
        dialog = QtWidgets.QDialog()
        self.__welcomescreen = WelcomeScreen(dialog)
        # self.__welcomescreen = LoginScreen.Ui_Welcomescreen()
        # self.__welcomescreen.setupUi(self.__welcomescreen)
        # self.__welcomescreen.setWindowTitle("Welcome!")
        # self.__welcomescreen.show()
