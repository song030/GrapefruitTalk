from PyQt5.QtCore import QThread, pyqtSignal

from Source.Client import Client

class ReceiveThread(QThread):

    res_message = pyqtSignal(str)

    def __init__(self, client:Client):
        super().__init__()
        self.client = client

    def run(self) -> None:
        while True:
            data = self.client.recevie()
            print("[ 데이터 수신 ]")
            print(data)

            self.res_message.emit(data)