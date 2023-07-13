from PyQt5.QtCore import QThread, pyqtSignal

from Source.Client import Client
from Source.Main.DataClass import *

class ReceiveThread(QThread):

    # 시그널 선언
    res_message = pyqtSignal(ReqChat)
    res_login = pyqtSignal(PerLogin)

    def __init__(self, client:Client):
        super().__init__()
        self.client = client

    def run(self) -> None:
        while True:
            data = self.client.recevie()

            print("[ 데이터 수신 ]")

            # 수신된 데이터 타입에 따른 시그널 방향 제시
            if type(data) == ReqChat:
                self.res_message.emit(data)

            # 클라이언트가 받을 결과
            elif type(data) == PerLogin:
                self.res_login.emit(data)