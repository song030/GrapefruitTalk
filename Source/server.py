# 모듈 import
import threading
import socket
import pickle
import datetime


class Server(object):
    """클라이언트 연결을 처리하는 서버 객체를 만듭니다. Server 클래스는
       누가 연결되어 있는지 추적하고 클라이언트로부터 메시지를 받아서 다시 클라이언트에게 보내는 역할을 합니다.
    """
    print('헐랭')
    # 변수
    buffer_num = 4000 # 버퍼
    port_num = 1121  # 포트
    host_num = '10.10.20.103' # socket.gethostbyname(socket.gethostname()) #호스트 ip
    host_and_port_nums = (host_num, port_num) # 호스트 ip와 port 주소를 튜플로 저장
    format_type = "utf-8" # 포메팅은 utf-8로
    connected_clients_dict = {} # 연결된 클라이언트의 key/value 쌍을 매핑하는 딕셔너리입니다.
    connected_usernames_list = [] # 모든 클라이언트에게 표시하기 위해 사용자 이름을 저장하는 리스트입니다.



    def __init__(self):
        try:
            # 서버 소켓 생성(AF_INET: ipv4, 버전으로 사용, SOCK_STREAM: tcp 패킷을 받는다는 의미)
            self.socket_for_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # 소켓 옵션 조작
            # (SOL_SOCKET: 옵션이 정의된 소켓 옵션 레벨을 나타내는 상수,
            # SO_REUSEADDR: 로컬 주소를 재활용할 수 있는 소켓 옵션. 이 옵션을 설정하면 TIME_WAIT 상태가 만료될 때 까지 기다리지 않고 로컬 주소를 재사용할 것임을 나타낸다. )
            self.socket_for_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # bind(): 생성된 서버 소켓에 주소를 부여한다. 이때 ip와 port주소를 전달한다.
            self.socket_for_server.bind(self.host_and_port_nums)

        # socket.error가 생성되면 오류문을 출력하고 소켓을 닫는다.
        except socket.error as ex:
            print("서버 생성 중 오류 발생.")
            self.socket_for_server.close()



    def start(self):
        """서버 소켓이 다른 소켓으로부터 들어오는 연결을 수신하기 시작합니다.
           연결이 이루어지면 먼저 클라이언트의 사용자 이름이 유효한지 확인합니다.
           유효하면 딕셔너리와 리스트에 추가됩니다.
           연결된 각 클라이언트마다 별도의 스레드가 시작되어 서버로 메시지를 보냅니다.
        """

        print("[서버 시작]") # 서버시작 확인용 print

        try:
            self.socket_for_server.listen() # 연결 요청 대기

            while True:
                # accept(): 서버의 연결 요청 대기. 클라이언트가 연결 요청 할 때까지 대기한다.
                sock, addr = self.socket_for_server.accept() # 소켓 객체, 주소를 튜플 형식으로 반환받는다.
                print(f"[연결 성공] {addr}가 서버에 연결되었습니다.") # 확인용

                # recv(): 소켓 객체에서 데이터를 전달받는다. 첫번째 매개변수로 표시되는 소켓을 통해 데이터를 수신하고, 수신한 데이터를 BUFFER에 보관한다.
                # 아래 코드에서는 utf-8 형식으로 메세지를 클라이언트가 보낸 메세지를 포메팅하고, 버퍼 크기만큼 저장한다.
                username = sock.recv(self.buffer_num).decode(self.format_type)

                # 서버에 연결한 클라이언트의 사용자 이름이 유효한지 확인
                if self.check_validate_username(username): # True값 리턴되면
                    sock.send("Valid".encode(self.format_type)) # utf-8값으로 인코딩해서 값을 보내줌 '유효함'
                    new_user = dict(user = username, address = addr, client = sock) #새로운 딕셔너리 값을 만듭니다.
                    self.connected_clients_dict[username] = new_user #딕셔너리 내에 새로운 key/value 쌍을 만듭니다.
                    self.connected_usernames_list.append(username) # 사용자 이름 리스트에 유저 이름을 추가한다.
                    self.send_msg_to_clients(username, "[*] " + username + "님이 입장하셨습니다. ") #새로운 참가자가 들어왔다는 메시지를 모든 현재 연결된 클라이언트에게 보냅니다.
                    self.send_list_of_users() # 현재 접속 유저들에게 접속 유저 모두 전송

                    # 스레드 - username(유저 소켓), addr(주소), sock(소켓 객체)를 인자로 가지고 __message_handler함수로 넘겨준다.
                    client_thread = threading.Thread(target=self.__message_handler,args=(username, addr, sock))
                    client_thread.start() # 쓸레드 시작

                else:
                    sock.send("Invalid".encode(self.format_type)) # 유효하지 않음 신호전달

        # 오류 난 경우
        except socket.error as ex:
            print("클라이언트 연결 수신 중 오류 발생.") # 콘솔에 출력


    def check_validate_username(self, username):
        """서버에 연결한 클라이언트의 사용자 이름이 유효한지 확인합니다.
           해당 메서드는 Server 클래스의 딕셔너리를 검색하고 사용자 이름을 사용하여 key/value 쌍을 검색합니다.
           검색 결과가 없으면 사용자 이름이 유효하고 사용할 수 있습니다.

           :param str username: 서버에 연결한 클라이언트의 사용자 이름.
           :return: 사용자 이름이 유효한지 여부.
           :rtype: bool
        """

        if self.connected_clients_dict.get(username) == None: # 주어진 사용자 이름이 연결된 클라이언트에게 매핑되어있지 않은 경우
            return True # True값 리턴
        else:
            return False


    def send_list_of_users(self):
        """현재 접속중인 클라이언트의 유저네임 리스트를 모든 클라이언트에게 전송."""
        user_list = pickle.dumps(self.connected_usernames_list) # 연결된 유저들을 모두 pickle로 직렬화 하여 리스트에 담는다.
        for _, values in self.connected_clients_dict.items(): # 연결된 클라이언트들의 username : value 값을 for문으로 돌려서
            # print('for문돌리는중', _, values)
            values['client'].send(user_list) # 현재 접속중인 클라이언트의 유저네임 리스트를 모든 클라이언트에게 전송하는 메소드


    def send_msg_to_clients(self, username, message):
        """현재 연결된 모든 클라이언트에게 메시지를 보냅니다.
           해당 메서드는 연결된 클라이언트의 소켓에 메시지를 보내기 위해 딕셔너리를 반복합니다.
           모든 전송이 제대로 이루어지면 True를 반환합니다.

           :param str username: 메시지를 보낸 사용자 이름.
           :param str message: 보낼 메시지.
           :return: 모든 메시지가 제대로 전송되었는지 여부.
           :rtype: bool
        """
        for key, values in self.connected_clients_dict.items(): # 연결된 유저들을 for문으로 돌려서 key값이 user_name과 같다면(접속한 클라이언트라면)
            if key == username:
                continue  # 현재 클라이언트 배제
            else:
                values['client'].send(message.encode(self.format_type)) # 메세지를 포메팅해서 해독한 후에 클라이언트들에게 보내줌

        # for user, data in self.connected_clients_dict.items():
        #     client = data.get("client")
        #     try:
        #         client.send((username + ": " + message).encode(self.format_type))
        #     except socket.error as ex:
        #         print("메시지 전송 중 오류 발생.")
        #         return False
        # return True


    def __message_handler(self, username, addr, client):
        """클라이언트에서 들어오는 메시지를 처리합니다. 해당 메서드는 클라이언트가
           연결을 해제할 때까지 동작합니다.
        """

        connected = True
        while connected:
            try:
                message = client.recv(self.buffer_num).decode(self.format_type)
                if message: # 메세지가 빈 값이 아니라면
                    if message == 'quit':
                        connected = False
                        # self.send_msg_to_clients(username, "[*] " + username + "님이 나가셨습니다. ")
                        # self.connected_usernames_list.remove(username)
                        continue
                    else:
                        message_date = datetime.datetime.now()
                        self.send_msg_to_clients(username, ">" + username + ": " + message + " - " + message_date.strftime(
                            " %x %I:%M %p"))

                # else:
                #     self.send_msg_to_clients(username, message)
            # except socket.error as ex:
            #     print("클라이언트 연결 해제.")
            #     connected = False
            except ConnectionResetError:  # 클라이언트가 갑자기 창을 닫을 때
                break
        client.close()
        self.remove_user(username)

    def remove_user(self, username):
        """서버에서 유저를 제거한다.
           :param str username: 서버에 연결되어 있는 클라이언트의 유저이름
        """

        del self.connected_clients_dict[username]
        self.connected_usernames_list.remove(username)

        if len(self.connected_usernames_list) != 0:  # 만약 마지막 사람이 제거된다면, 이 메세지를 출력하지 않는다.
            self.send_list_of_users()
            self.send_msg_to_clients(username, "[*] " + username + " has disconnected from the server.")

def main():
    SERVER = Server()
    SERVER.start()


if __name__ == "__main__":
    main()