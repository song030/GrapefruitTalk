import socket
import datetime
import threading
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLayout
import sys
import pickle
from Views.UI_MainWidget import Ui_MainWidget
from Views.DialogWarning import Ui_DlgWarning
from Views.TalkBox import TalkBox
from Views.DateLine import DateLine


class Client(Ui_MainWidget):
    """메인 윈도우에서 상속받아 채팅방을 보여준고 기능들을 서버에 연결해 준다.
    사용자에게 메세지를 받고 다른 클라이언트들에게 정보를 받고 보내주는 기능을 한다."""

    format_type = "utf-8"  # utf-8
    buffer_num = 4000
    port_num = 1121
    host_num = '10.10.20.103'  # socket.gethostbyname(socket.gethostname()) #'10.10.20.103' #socket.gethostbyname(socket.gethostname())
    print('호스트: ', host_num, '포트주소: ', port_num, '버퍼: ', buffer_num)
    server_num = (host_num, port_num)  # 호스트와 포트 주소를 server_num 변수에 저장한다.

    def __init__(self, MainWindow, username):
        self.connected_state = False
        # self.__welcomescreen = None
        self.receive_thread = threading.Thread(target=self.receive_message)
        self.talk_page = MainWindow
        self.username = username
        self.socket_for_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server()
        self.check_validate_user(self.username)

    def connect_to_server(self):
        """서버 소켓에 연결한다."""

        try:
            self.socket_for_client.connect(self.server_num)

        except ConnectionRefusedError:
            print("서버에 연결할 수 없습니다.")
            sys.exit()

    def check_validate_user(self, username):
        """서버로 보내어 username이 유효한지 확인한다. 유효하면 채팅방을 보여준다.
           :param str username: 클라이언트에서 제출한 username
           :raises OSError: 서버가 오프라인 상태이므로 클라이언트가 메시지를 보낼 수 없습니다.
        """

        try:
            self.socket_for_client.send(username.encode(self.format_type))
            if self.socket_for_client.recv(self.buffer_num).decode(self.format_type) == "Valid":  # 서버가 username을 유효하게 선언하는 경우.
                self.connected_state = True
                self.setupUi(self.talk_page)

                # 버튼 시그널 연결
                self.talk_page.btn_send.clicked.connect(self.send_message)
                self.talk_page.edt_txt.returnPressed.connect(self.send_message)

                # self.disconnect_button.clicked.connect(self.disconnect_func)
                # self.talk_page.show()

                # 채팅방 참여 메세지
                talkbox = TalkBox('', self.username, f"{username}님이 채팅방에 참여하였습니다." , datetime.datetime.now())
                self.talk_page.layout_talk.addLayout(talkbox.layout)

                # 스레드 시작
                self.receive_thread.start()

            else:
                self.__show_welcomescreen()

        except(OSError):  # 서버 파일이 실행되지 않아 클라이언트가 메시지를 보낼 수 없습니다.
            print("서버가 오프라인 상태입니다.")
            sys.exit()

    def send_message(self):
        """클라이언트에서 서버로 메시지를 보낸다.
           :raises ConnectionResetError: 서버 파일이 중지되었지만 클라이언트가 메시지를 보내려고 시도합니다.
        """
        print('메세지가 타요')
        # message = self.edt_txt.toPlainText().strip()
        message = self.talk_page.edt_txt.text()
        print('유저가 작성한 메세지', message)
        if len(message) > 0:  # message가 비어 있지 않은 경우
            try:
                message_date = datetime.datetime.now()
                self.socket_for_client.send(message.encode(self.format_type))

                # 메세지 추가
                self.add_date_line()
                talkbox = TalkBox('', self.username, message, message_date)
                self.talk_page.layout_talk.addLayout(talkbox.layout)

                # self.talk_page.textBrowser.append(
                #     f"{self.username}: " + message + " - " + message_date.strftime(" %x %I:%M %p"))
                # self.textBrowser.append(">YOU: " + message + " - " + message_date.strftime(" %x %I:%M %p"))

            except(ConnectionResetError):  # 서버가 실행되지 않았지만 클라이언트가 메시지를 보내려고 시도합니다.
                # self.textBrowser.append("서버가 현재 오프라인 상태입니다.")
                # self.talk_page.textBrowser.append("서버가 현재 오프라인 상태입니다.")
                pass
        self.talk_page.edt_txt.clear()

    def add_date_line(self):
        """날짜를 생성한다"""
        talkbox = DateLine(datetime.datetime.now())
        self.talk_page.layout_talk.addLayout(talkbox.layout)

    def receive_message(self, client_message):
        """
        각각 다른 스레드에서 있는 서버에서 메세지를 받기 위한 역할을 한다.
        메세지는 서버에서 받아지고 첫번째로 피클 모듈을 사용하여 리스트 형식으로 변형된다.
        이 리스트는 채팅방에 있는 모든 클라이언트에게 보내진다.
        """

        try:
            while self.connected_state:  # 무한 루프를 사용하여 메시지를 계속 수신한다.
                message = self.socket_for_client.recv(self.buffer_num)
                if message:
                    try:
                        connected_users = pickle.loads(message)
                        print('이건머져', connected_users)
                        print('혹시 여길 타나요?')
                        # self.connected_clients.clear()
                        # for name in connected_users:
                        #     self.connected_clients.addItem(name)
                    except:
                        print('서버에서 받은 메세지 출력: ', message.decode(self.format_type))
                        self.add_date_line()
                        talkbox = TalkBox("", "test_user", message.decode(self.format_type), datetime.datetime.now())
                        talkbox.message_signal.connect(self.add_talkbox)
                        # QtCore.QMetaObject.invokeMethod(self.talk_page.layout_talk, 'addLayout',
                        #                                 QtCore.Qt.QueuedConnection,
                        #                                 QtCore.Q_ARG(QLayout, talkbox.layout))

                        # self.talk_page.layout_talk.addLayout(talkbox.layout)

        except(ConnectionAbortedError, ConnectionResetError):
            pass
    def add_talkbox(self, img_path, name, msg, time):
        talkbox = TalkBox(img_path, name, msg, time)
        talkbox_layout = talkbox.layout()
        self.talk_page.layout_talk.addLayout(talkbox_layout)




    def disconnect_func(self):
        """클라이언트가 연결을 종료할 때 실행되는 함수. 만약 x버튼이 있다면"""
        self.connected_state = False
        # self.socket_for_client.send("exit".encode(self.format_type))
        try:
            self.socket_for_client.send('DISCONNECT'.encode(self.format_type))
        except(ConnectionResetError):
            pass
        self.socket_for_client.close()
        self.__show_welcomescreen()

    def __show_welcomescreen(self):
        """Username이 유효하지 않을 때 실행되는 함수."""
        # from Client.welcome import WelcomeScreen
        self.chatroom.destroy()
        # dialog = QtWidgets.QDialog()
        # self.__welcomescreen = WelcomeScreen(dialog)
        # self.__welcomescreen = LoginScreen.Ui_Welcomescreen()
        # self.__welcomescreen.setupUi(self.__welcomescreen)
        # self.__welcomescreen.setWindowTitle("Welcome!")
        # self.__welcomescreen.show()
