from PyQt5.QtCore import QThread, pyqtSignal

from Source.Client import Client
from Source.DataClass import *

class ReceiveThread(QThread):

    # 시그널 선언
    res_message = pyqtSignal(ReqChat)

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