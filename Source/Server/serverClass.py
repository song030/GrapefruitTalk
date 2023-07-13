import datetime
import socket
import threading
import pickle


class Group:
    """채팅방 객체 : 전체 멤버 정보 """
    def __init__(self, t_user: str, t_sock: socket.socket):
        self.all_client = {}
        self.all_member = set()
        self.online_member = set()

        self.admin = t_user
        self.all_client[t_user] = t_sock
        self.all_member.add(t_user)
        self.online_member.add(t_user)

    def connect(self, t_user: str, t_sock: socket.socket):
        """온라인"""
        # self.online_member.add(t_user)
        # self.all_client[t_user] = t_sock
        pass

    def disconnect(self, t_user):
        """오프라인"""
        # self.online_member.remove(t_user)
        # del self.all_client[t_user]
        pass


class MainServer:
    def __init__(self, t_ip: str = '', t_port: int = 9000):
        self.clients = {}   # 현재 서버에 접속 중인 클라이언트 정보를 담는 딕셔너리
        self.group_bundle = {}   # 현재 활성화된 채팅방 dict("그룹 아이디": 그룹 객체)
        try:
            self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_sock.bind((t_ip, t_port))
        except socket.error as ex:
            print("Error in creating the server.")
            self.server_sock.close()

    def start(self, t_listener: int = 100):
        """서버 실행 이후 연결 대기 상태, 클라이언트 연결(프로그램 실행)"""
        try:
            print("[server start]")
            self.server_sock.listen(t_listener)
            while True:
                client, addr = self.server_sock.accept()
                _handler = threading.Thread(target='handler', args=(client,))
                _handler.daemon = True
                _handler.start()
                print(f"{addr} thread start")
        except socket.error as ex:
            print("Error while listening for client connections.")

    def send(self):
        """송신용 스레드 함수"""
        while True:
            pass

    def recv(self):
        """수신용 스레드 함수"""
        while True:
            message = self.server_sock.recv(1024)
            if not message:
                break
            # message = pickle.loads(message)   # 명령어를 클래스 객체로 받겠다?
            self.process(message)

    def process(self, message):
        """바이트 시퀀스에 대한 처리"""
        print(f"{message.decode('utf-8')}")
        pass

    # def __validate_username(self, username):
    #     if self.__connected_clients.get(username) is None:
    #         return True
    #     else:
    #         return False
    #
    # def __list_of_users(self):
    #     pass
    # def __broadcast(self, username, message):
    #     for k, v in self.__connected_clients.items():
    #         if k == username:
    #             continue
    #         else:
    #             v['client'].send(message.encode(self.__FORMAT))
    #
    # def handler(self, username, address, client):
    #     connected = True
    #     while connected:
    #         try:
    #             message = client.recv(self.__BUFFER).decode(self.__FORMAT)
    #             if message == "DISCONNECT":
    #                 connected = False
    #                 continue
    #             else:
    #                 message_date = datetime.datetime.now()
    #                 self.__broadcast(username, f">{username}: {message} - {message_date.strftime(' %x %I:%M %p')}")
    #         except ConnectionResetError:
    #             break
    #
    #     client.close()
    #     self.__remove_user(username)
    #
    # def __remove_user(self, username):
    #     del self.__connected_clients[username]
    #     self.__connected_usernames.remove(username)
    #
    #     if len(self.__connected_usernames) != 0:
    #         self.__list_of_users()
    #         self.__broadcast(username, f"[*] {username} has disconnected from the server")


def handler(t_server: MainServer, t_client: socket.socket):
    """ server.recv > server.prcs > server.send(처리 결과를 클라이언트에 전송)"""
    pass


def run_server():
    listen_server = MainServer()
    listen_server.start()


if __name__ == "__main__":
    run_server()
