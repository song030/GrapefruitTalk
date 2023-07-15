import socket
import pickle
import queue

from Source.Server.DBConnector import DBConnector
from Source.Main.DataClass import *

from threading import Thread

class Server:
    def __init__(self, port=1989, listener=10):
        self.db = DBConnector()

        # 접속한 클라이언트 정보 key :(ip,포트번호), value : [소켓정보, 아이디]
        # {('10.10.20.117', 57817): [<socket.socket fd=384, family=2, type=1, proto=0, laddr=('10.10.20.117', 1234), raddr=('10.10.20.117', 57817)>, '']}
        self.client : dict[tuple, list[socket.socket, str]] = {}

        # 서버 소켓 생성
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 서버 소켓 닫을 때 포트 닫아주는 설정
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("", port))  # 서버의 주소, 포트번호 저장
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
        self.client[addr] = [sock, ""]
        print()

        return sock, addr

    # 클라이언트 연결 종료
    def disconnect(self, sock):
        # 접속 종료한 클라이언트의 정보가 존재한다면
        addr = sock.getpeername()
        if addr in self.client:
            # 로그아웃 정보 발송
            self.send_exclude_sender(sock, LoginInfo([self.client[addr][1]], False))

            # 클라이언트 정보 삭제
            del self.client[addr]

    # 데이터 타입에따른 데이터 전송
    def send(self, sock:socket.socket, data):
        # 접속중인 방 멤버에게만 메시지 발송
        if type(data) in [ReqChat]:
            self.send_message(data)

        # 요청 클라이언트를 제외한 모든 클라이언트에게 발송
        if type(data) in [LoginInfo]:
            self.send_exclude_sender(sock, data)

        # 요청한 클라이언트에게 회신
        elif type(data) in [PerDuplicateCheck, PerEmailSend, PerEmailNumber, PerRegist]:
            self.send_client(sock, data)

        elif type(data) in [PerAcceptFriend]:
            self.send_friend(sock, data)

        # 클라이언트 로그인 요청 → 두 방식으로 발송해야해서 따로 나눔
        elif type(data) in [PerLogin]:
            # 요청자에게 로그인 결과 발송
            self.send_client(sock, data)
            self.db_log_inout_state_save(data.rescode)

            # 로그인 성공시
            # 서버에 로그인 정보 저장, 접속자 제외한 클라이언트에게 접속 정보 발송
            if data.rescode == 2:
                self.client[sock.getpeername()][1] = data.user_id_
                self.send_exclude_sender(sock, LoginInfo(data.user_id_))
        # elif type(data) in [ReqMembership]:

    def send_friend(self, sock:socket.socket, data:PerAcceptFriend):
        if self.connected():
            user_id = self.client[sock.getpeername()][1]

            # 친구 요청
            if user_id == data.user_id_:
                send_id = data.user_id_

            # 요청 답변
            else:
                send_id = data.frd_id_

            for client in self.client.values():
                if client[1] == send_id:
                    client[0].sendall(pickle.dumps(data))
                    break

    # 요청한 클라이언트에게만 전송
    def send_client(self, sock: socket.socket, data):
        if self.connected():
            sock.sendall(pickle.dumps(data))
            return True
        else:
            return False

    # 접속한 모든 클라이언트에게 전송
    def send_all_client(self, data):
        if self.connected():
            for client in self.client.values():
                client[0].sendall(pickle.dumps(data))
            return True
        else:
            return False

    # 발송자를 제외한 나머지 접속자에게 메시지 발송
    def send_message(self, data: ReqChat):
        if self.connected():
            member = self.db.find_user_chatroom(data.cr_id_)
            print("sende message")
            print("member :", member)

            for idx, client in enumerate(self.client.values()):
                print("-", client[1])
                if data.user_id_ != client[1] and client[1] in member:
                    client[0].sendall(pickle.dumps(data))
                    # self.db.insert_content(data)

                # 메시지 발송내역은 한번만 저장
                if idx == 0:
                    self.db.insert_content(data)
            return True
        else:
            return False

    # 발송자를 제외한 나머지 접속자에게 발송
    def send_exclude_sender(self, sock: socket.socket, data: LoginInfo):
        print("send_exclude_sender")
        if self.connected():
            for idx, client in enumerate(self.client.values()):
                if self.client[sock.getpeername()][1] != client[1]:
                    client[0].sendall(pickle.dumps(data))
            return True
        else:
            return False

    # 데이터 수신
    def recevie(self, sock:socket.socket):
        # 데이터를 발송한 클라이언트의 어드레스 얻기
        try:
            receive_bytes = sock.recv(4096)

            # 데이터 수신 실패시 오류 발생
            if not receive_bytes:
                raise

            # 수신 받은 데이터 변환 하여 반환
            data = pickle.loads(receive_bytes)
            return data

        except:
            self.disconnect(sock)
            sock.close()
            return None

    # 받은 데이터에 대한 처리 결과 반환 내용 넣기
    def process_data(self, sock, data):
        print(f"process_data : {type(data)}")
        print("data", get_data_tuple(data))
        print()

        # 채팅 발송
        if type(data) == ReqChat:
            return data

        # 아이디 중복 확인 요청
        elif type(data) == ReqDuplicateCheck:
            perdata: PerDuplicateCheck = self.db.membership_id_check(data)

        # 인증메일 발송 요청
        elif type(data) == ReqEmailSend:
            perdata: PerEmailSend = self.db.email_check_1(data)

        # 인증번호 확인 요청
        elif type(data) == ReqEmailNumber:
            perdata: PerEmailNumber = self.db.email_check_2(data)

        # 회원가입 요청
        elif type(data) == ReqMembership:
            perdata: PerRegist = self.db.regist(data)

        # 로그인 요청
        elif type(data) == ReqLogin:
            perdata: PerLogin = self.db.login(data)
            if perdata.rescode == 2:
                self.client[sock.getpeername()][1] = perdata.user_id_
                perdata.login_info = self.get_login_list()

        # 로그 아웃
        elif type(data) == ReqLoout:
            user_id = self.client[sock.getpeername()][1]
            self.client[sock.getpeername()][1] = ""
            perdata: LoginInfo([user_id], False)

        # 중간 과정 없이 바로 진행 하는 data
        # 친구 요청, 친구 수락/거절
        elif type(data) == ReqSuggetsFriend:
            # 요청 유저 아이디
            req_user_id = self.client[sock.getpeername()][1]
            login_list = self.get_login_list()
            perdata = data

            # 친구 요청
            if req_user_id == data.user_id_:
                self.db.insert_friend(data)

                # 요청 받은 친구가 접속중인 경우
                if data.frd_id_ in login_list:
                    perdata:PerAcceptFriend(data.user_id_, data.frd_id_)

            # 친구 요청 결과 발송
            elif req_user_id == data.frd_id_:
                # 수락
                if data.result == 1:
                    self.db.update_friend(data)

                    if data.user_id_ in login_list:
                        perdata:PerAcceptFriend(data.user_id_, data.frd_id_, 1)

                # 거절
                else:
                    self.db.delete_friend(data)

                    if data.user_id_ in login_list:
                        perdata:PerAcceptFriend(data.user_id_, data.frd_id_, 0)

        else:
            return data

        print(f"process_data : {type(perdata)}")
        print("perdata", get_data_tuple(data))
        print()
        return perdata

    def get_login_list(self):
        login_list = list()
        for client in self.client.values():
            if client[1] != "":
                login_list.append(client[1])

        print("login info")
        print(login_list)

        return login_list

    def db_log_inout_state_save(self, rescode):
        """로그인 / 로그아웃 내역(시간) USER_LOG에 저장"""
        sql_ = ''
        time_ = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        print(time_)
        print(rescode)
        if rescode == 2:
            sql_ = f"UPDATE TB_LOG SET LOGIN_TIME = '{time_}' WHERE USER_ID = '{id}'"
            self.db.conn.execute(sql_)
            self.db.conn.commit()
        All_TB_LOG = self.db.conn.execute("SELECT * FROM TB_LOG").fetchall()
        if not All_TB_LOG:
            print("예외처리 : TB_LOG에 아무것도 없습니다.")

    def handler(self, sock, queue_: queue.Queue):
        while True:
            data = self.recevie(sock)

            if not data:
                break

            print("[ 데이터 수신 ]")
            # 수신된 데이터에 따른 결과 반환값을 클라이언트로 보내주기
            print(data)
            # 클라이언트에게 받은 데이터를 Queue에 추가
            queue_.put(data)

            while True:
                try:
                    # Queue에서 데이터 얻기
                    get_data = queue_.get(block=False)
                    process_data = self.process_data(sock, get_data)
                    print("[ 데이터 처리 ]")
                    self.send(sock, process_data)
                    print("처리 완료")
                    queue_.task_done()
                except:
                    break


if __name__ == "__main__":
    server = Server()
    # 데이터를 받을 Queue 추가
    data_queue = queue.Queue()

    while True:
        print("대기중...")

        c_sock, c_addr = server.accept()
        c_thread = Thread(target=server.handler, args=(c_sock, data_queue), daemon=True)
        c_thread.start()
