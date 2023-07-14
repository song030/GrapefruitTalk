from PyQt5.QtCore import QThread, pyqtSignal

from Source.Client import Client
from Source.Main.DataClass import *

class ReceiveThread(QThread):

    # 시그널 선언
    res_message = pyqtSignal(ReqChat)
    res_duplicate_id_check = pyqtSignal(PerDuplicateCheck)
    res_emailcheck_1 = pyqtSignal(PerEmailSend)
    res_emailcheck_2 = pyqtSignal(PerEmailNumber)
    res_regist = pyqtSignal(PerRegist)
    res_login = pyqtSignal(PerLogin)

    def __init__(self, client:Client):
        super().__init__()
        self.client = client

    def run(self) -> None:
        while True:
            data = self.client.recevie()

            print("[ 데이터 수신 ]")
            print(f"수신 데이터 타입 : {type(data)}")

            # 수신된 데이터 타입에 따른 시그널 방향 제시 : 클라이언트가 받을 결과를 전송하는 것임

            # 채팅 수신
            if type(data) == ReqChat:
                self.res_message.emit(data)

            # 아이디 중복 확인
            elif type(data) == PerDuplicateCheck:
                self.res_duplicate_id_check.emit(data)

            # 인증번호 발송
            elif type(data) == PerEmailSend:
                self.res_emailcheck_1.emit(data)

            # 인증번호 확인
            elif type(data) == PerEmailNumber:
                self.res_emailcheck_2.emit(data)

            # 회원가입 요청 결과
            elif type(data) == PerRegist:
                self.res_regist.emit(data)

            # 로그인 결과
            elif type(data) == PerLogin:
                self.res_login.emit(data)