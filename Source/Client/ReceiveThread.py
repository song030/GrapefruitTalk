from PyQt5.QtCore import QThread, pyqtSignal

from Source.Client import Client

class ReceiveThread(QThread):
    res_message = pyqtSignal()

    def __init__(self, client:Client):
        super().__init__()
        self.client = client

    def run(self) -> None:
        while True:
            data = self.client.recevie()

            self.res_message.emit(data)