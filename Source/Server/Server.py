import socket
import pickle
# from db import DB
from Source.DataClass import *

from threading import Thread

class Server:
    def __init__(self, port=1234, listener=1):
        # db 초기화 내용 넣기

        # 접속한 클라이언트 정보 key :(ip,포트번호), value : [소켓정보, 아이디]
        # {('10.10.20.117', 57817): [<socket.socket fd=384, family=2, type=1, proto=0, laddr=('10.10.20.117', 1234), raddr=('10.10.20.117', 57817)>, '']}
        self.client : dict[tuple, list[socket.socket, str]] = {}

        # 서버 소켓 생성
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('', port))  # 서버의 주소, 포트번호 저장
        self.sock.listen(listener)  # 서버 소켓 연결 요청 대시 상태로 설정

        self.count = 0

        print("[ 서버 시작 ]")

    # 접속한 클라이언트가 있는지 확인 (있으면 True, 없으면 False)
    def connected(self):
        if len(self.client):
            return True
        else:
            return False

    # 클라이언트 연결
    def accept(self):
        # 클라이언트 연결시 소켓과 어드레스 반환
        sock, addr = self.sock.accept()

        print("[ 클라이언트 접속 ]")
        self.client[addr] = [sock, f"test{self.count}"]

        return sock, addr

    # 클라이언트 연결 종료
    def disconnect(self, addr):
        # 접속 종료한 클라이언트의 정보가 존재한다면
        if addr in self.client:

            # 클라이언트 정보 삭제
            del self.client[addr]

    # 데이터 전송
    def send(self, sock:socket.socket, data):

        # 데이터 타입에따른 데이터 전송
        if type(data) in [ReqChat]:
            self.send_message(data)

    # 접속한 모든 클라이언트에게 전송
    def send_all_client(self, data):
        if self.connected():
            for client in self.client.values():
                client[0].sendall(pickle.dumps(data))
            return True
        else:
            return False

    # 발송자를 제외한 나머지 접속자에세 메시지 발송
    def send_message(self, data:ReqChat):
        if self.connected():
            # {('10.10.20.117', 57817): [<socket.socket fd=384, family=2, type=1, proto=0, laddr=('10.10.20.117', 1234), raddr=('10.10.20.117', 57817)>, '']}
            # 연결된 모든 클라이언트에 데이터 발송
            for client in self.client.values():
                print(data.user_id, client[1])
                if data.user_id != client[1]:
                    client[0].sendall(pickle.dumps(data))
            return True
        else:
            return False

    # 데이터 수신
    def recevie(self, sock:socket.socket):
        # 데이터를 발송한 클라이언트의 어드레스 얻기
        addr = sock.getpeername()

        try:
            receive_bytes = sock.recv(4096)

            # 데이터 수신 실패시 오류 발생
            if not receive_bytes:
                raise

            # 수신 받은 데이터 변환 하여 반환
            data = pickle.loads(receive_bytes)
            return data

        except:
            sock.close()
            self.disconnect(addr)
            return None

    # 받은 데이터에 대한 처리 결과 반환 내용 넣기
    def process_data(self, sock, data):
        print(type(data))
        if type(data) == ReqChat:
            return data

    def handler(self, sock,):
        while True:
            data = self.recevie(sock)

            if not data:
                break

            print("[ 데이터 수신 ]")
            # 수신된 데이터에 따른 결과 반환값을 클라이언트로 보내주기
            print(data)
            process_data = self.process_data(sock, data)

            print("[ 결과 발송 ]")
            self.send(sock, process_data)
            print("발송 완료")


if __name__ == "__main__":
    server = Server()

    while True:
        print("대기중...")

        c_sock, c_addr = server.accept()
        c_thread = Thread(target=server.handler, args=(c_sock,), daemon=True)
        c_thread.start()
