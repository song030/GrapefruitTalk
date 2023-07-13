import sqlite3

from datetime import datetime
from Source.Main.DataClass import *

class DBConnector:      # DB를 총괄하는 클래스
    _instance = None    # 싱글턴 패턴 사용
    conn = sqlite3.connect("../../Data/data.db", check_same_thread=False)     # db 속

    def __new__(cls):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        self.cur = self.conn.cursor()

    def end_conn(self):  # db 종료
        self.conn.close()

    def commit_db(self):  # db 커밋
        self.conn.commit()

    ## CREATE TABLES ======================================================================== ##
    def create_tables(self):  # 테이블 생성
        self.cur.executescript("""
            DROP TABLE IF EXISTS TB_USER;  
            CREATE TABLE "TB_USER" (
                "USER_NO" INTEGER,
                "USER_ID" TEXT NOT NULL,
                "USER_NM" TEXT NOT NULL,
                "USER_EMAIL" TEXT NOT NULL,
                "USER_PW" TEXT NOT NULL,
                "USER_CREATE_DATE" TEXT NOT NULL,
                "USER_IMG" TEXT,
                "USER_STATE" TEXT,
                PRIMARY KEY ("USER_NO" AUTOINCREMENT),
                UNIQUE KEY ("USER_ID")
            );
            DROP TABLE IF EXISTS TB_FRIEND;
            CREATE TABLE "TB_FRIEND" (
                "USER_ID" TEXT,
                "FRD_ID" TEXT,
                "FRD_ACCEPT" TEXT,
                FOREIGN KEY ("USER_ID") REFERENCES "TB_USER" ("USER_ID")
            );
            DROP TABLE IF EXISTS TB_LOG;
            CREATE TABLE "TB_LOG" (
                "USER_ID" TEXT,
                "LOGIN_TIME" TEXT,
                "LOGOUT_TIME" TEXT,
                FOREIGN KEY ("USER_ID") REFERENCES "TB_USER" ("USER_ID")
            );
            DROP TABLE IF EXISTS TB_CHATROOM;
            CREATE TABLE "TB_CHATROOM" (
                "CR_ID" TEXT,
                "CR_NM" TEXT,
                PRIMARY KEY ("CR_ID")
            );
            DROP TABLE IF EXISTS TB_USER_CHATROOM;
            CREATE TABLE "TB_USER_CHATROOM" (
                "CR_ID" TEXT,
                "USER_CR_FROM" TEXT,
                "USER_CR_TO" TEXT,
                FOREIGN KEY ("CR_ID") REFERENCES "TB_CHATROOM" ("CR_ID")
            );
            DROP TABLE IF EXISTS TB_CONTENT;
            CREATE TABLE "TB_CONTENT" (
                "CR_ID" TEXT,
                "USER_ID" TEXT,
                "CNT_ID" INTEGER,
                "CNT_CONTENT" TEXT,
                "CNT_SEND_TIME" TEXT,
                PRIMARY KEY ("CNT_ID" AUTOINCREMENT),
                FOREIGN KEY ("CR_ID") REFERENCES "TB_CHATROOM" ("CR_ID"),
                FOREIGN KEY ("USER_ID") REFERENCES "TB_USER" ("USER_ID")
            );
            DROP TABLE IF EXISTS TB_READ_CNT;
            CREATE TABLE "TB_READ_CNT" (
                "CNT_ID" INTEGER,
                "USER_ID" TEXT,
                "IS_READ" INTEGER,
                FOREIGN KEY ("CNT_ID") REFERENCES "TB_CONTENT" ("CNT_ID"),
                FOREIGN KEY ("USER_ID") REFERENCES "TB_USER" ("USER_ID")
            );
            DROP TABLE IF EXISTS TB_BANCHAT;
            CREATE TABLE "TB_BANCHAT" (
              "BC_NO" INTEGER,
              "BC_TYPE" TEXT,
              "BC_CONTENT" TEXT,
              PRIMARY KEY ("BC_NO" AUTOINCREMENT)
            );
        """)
        self.commit_db()

    # todo: 회원가입부터 로그인 친구목록
    ## TB_USER ================================================================================ ##
    # 회원 정보 테이블 값 입력
    def insert_user(self, user_id, user_name, user_email, user_pw,
                    user_create_date, user_img, user_state):
        self.cur.execute("insert into TB_USER (USER_ID, USER_NAME, USER_EMAIL, USER_PW, USER_CRATE_DATE, "
                  "USER_IMG, USER_STATE) values (?, ?, ?, ?, ?, ?, ?)",
                  (user_id, user_name, user_email, user_pw, user_create_date, user_img, user_state))
        self.commit_db()

    # 회원 정보 테이블 전체 조회
    def find_user(self):
        rows_data = self.cur.execute("select * from TB_USER").fetchall()
        if len(rows_data) == 0:
            return None

        find_result_list = list()
        for row in rows_data:
            find_result_list.append(row)
        return rows_data

    # user_id를 기준으로 행 조회
    def find_user_by_id(self, user_id: str):
        row = self.cur.execute("select * from TB_USER where USER_ID = ?", (user_id,)).fetchall()
        id = row[0]
        return id

    # user_id를 기준으로 행 삭제
    def delete_user(self, user_id: str):
        self.cur.execute("delete from TB_USER where USER_ID = ?", (user_id,))
        self.commit_db()

    ## TB_friend ================================================================================ ##
    # 친구 목록 정보 테이블 값 입력
    def insert_friend(self, user_id, frd_id):
        self.cur.execute("insert into TB_FRIEND (CR_ID, CR_NM) values (?, ?)", (user_id, frd_id))
        self.commit_db()

    # 친구 목록 테이블 전체 조회
    def find_friend(self):
        rows_data = self.cur.execute("select * from TB_FRIEND").fetchall()
        if len(rows_data) == 0:
            return None

        find_result_list = list()
        for row in rows_data:
            find_result_list.append(row)
        return rows_data

    # FRD_ID를 기준으로 행 조회
    def find_friend_by_frd_id(self, frd_id):
        row = self.cur.execute("select * from TB_FRIEND where FRD_ID = ?", (frd_id,)).fetchall()
        friend_id = row[0]
        return friend_id
        # todo: sql문에도 and와 or문을 넣을 수 있다. 첫 번째 조건 뒤에 연산자를 추가하여 다음에 두번째 (id 먼저 pw를 조회) 하여 찾기
        # sql문에서 개수를 가지고 오는 방법 -> * 말고 count(컬럼명) 숫자로 값이 나옴
        # 데이터 프레임으로 받아와지면 줄 수가 몇개인지 확인 0이면 x 1이면 o

    # FRD_ID를 기준으로 행 삭제
    def delete_friend(self, frd_id: str):
        self.cur.execute("delete from TB_FRIEND where FRD_ID = ?", (frd_id,))
        self.commit_db()

    ## TB_log ================================================================================ ##
    # LOG 정보 테이블 값 입력
    def insert_log(self, user_id, login_time, logout_time):
        self.cur.execute("insert into TB_LOG (USER_ID, LOGIN_TIME, LOGOUT_TIME) values (?, ?, ?)", (user_id, login_time, logout_time))
        self.commit_db()

    # LOG 테이블 전체 조회
    def find_log(self):
        rows_data = self.cur.execute("select * from TB_LOG").fetchall()
        if len(rows_data) == 0:
            return None

        find_result_list = list()
        for row in rows_data:
            find_result_list.append(row)
        return rows_data

    # LOGIN_TIME을 기준으로 행 조회
    def find_login_time(self, login_time: str):
        row = self.cur.execute("select * from TB_LOG where LOGIN_TIME = ?", (login_time,)).fetchall()
        time = row[0]
        return time

    # LOGOUT_TIME을 기준으로 행 조회
    def find_logout_time(self, logout_time: str):
        row = self.cur.execute("select * from TB_LOG where LOGOUT_TIME = ?", (logout_time,)).fetchall()
        time = row[0]
        return time

    ## TB_chatroom ================================================================================ ##
    # 채팅방 일련 번호 생성
    def chatroom_id_creation(self, cr_id, cr_name):
        ids = self.cur.execute("select * from TB_CHATROOM where CR_ID like ?", (f"%{cr_id}%",)).fetchall()
        if len(ids) == 0:       # ids의 값이 없을 경우 초기 번호로 자동 설정
            cr_id = cr_id + "_1"
            cr_name = cr_name
            return self.insert_chatroom(cr_id, cr_name)

        id_nm = None    # 채팅방 타입을 담기 위한 변수
        id_list = list()
        for row in ids:     # 일련 번호를 타입과 번호로 분리
            id_nm = row[0][:3]      # 채팅방 타입
            id_list.append(int(row[0][3:]))     # 채팅방 타입별 번호
        id_list.sort()
        id_num = max(id_list)

        cr_id = id_nm+str(id_num + 1)   # 일련 번호 중 최대값에 +1 하여 저장
        cr_name = cr_name

        return self.insert_chatroom(cr_id, cr_name)

    # 채팅방 정보 테이블에 값 입력
    def insert_chatroom(self, cr_id, cr_name):
        self.cur.execute("insert into TB_CHATROOM (CR_ID, CR_NM) values (?, ?)", (cr_id, cr_name))
        self.commit_db()

    # 채팅방 정보 테이블 전체 조회
    def find_chatroom(self):
        rows_data = self.cur.execute("select * from TB_CHATROOM").fetchall()
        # CR_ID, CR_NM
        if len(rows_data) == 0:     # chatroom 테이블에 값이 없을 경우 None으로 반환
            return None

        find_result_list = list()
        for row in rows_data:
            find_result_list.append(row)
        return find_result_list

    # 채팅방 번호를 기준으로 행 조회
    def find_chatroom_by_id(self, cr_id: str):
        row = self.cur.execute("select * from TB_CHATROOM where CR_ID = ?", (cr_id,)).fetchall()
        id = row[0]
        return id

    # 채팅방 이름을 기준으로 행 조회
    def find_chatroom_by_name(self, cr_name: str):
        row = self.cur.execute("select * from TB_CHATROOM where CR_NM = ?", (cr_name,)).fetchall()
        chatroom_name = row[0]
        return chatroom_name

    def delete_chatroom(self, cr_id: str):
        self.cur.execute("delete from TB_CHATROOM where CR_ID = ?", (cr_id,))
        self.commit_db()

    ## TB_user_chatroom ================================================================================ ##
    def insert_user_chatroom(self, cr_id, user_cr_from, user_cr_to):
        self.cur.execute("insert into TB_USER_CHATROOM (CR_ID, USER_CR_FROM, USER_CR_TO) values (?, ?, ?)", (cr_id, user_cr_from, user_cr_to))
        self.commit_db()

    def find_user_chatroom(self):
        rows_data = self.cur.execute("select * from TB_USER_CHATROOM").fetchall()
        # CR_ID, CR_NM
        if len(rows_data) == 0:
            return None

        find_result_list = list()
        for row in rows_data:
            find_result_list.append(row)
        return find_result_list

    def find_user_chatroom_by_from(self, user_cr_from):
        row = self.cur.execute("select * from TB_USER_CHATROOM where USER_CR_FROM = ?", (user_cr_from,)).fetchall()
        user_from = row[0]
        return user_from

    def find_user_chatroom_by_to(self, user_cr_to):
        row = self.cur.execute("select * from TB_USER_CHATROOM where USER_CR_TO = ?", (user_cr_to,)).fetchall()
        user_cr_to = row[0]
        return user_cr_to

    # todo: 어떤 부분을 삭제할 것인지 더 생각해보기
    def delete_user_chatroom(self, user_cr_to):
        self.cur.execute("delete from TB_CHATROOM where USER_CR_TO = ?", (user_cr_to,))
        self.commit_db()

    ## TB_content ================================================================================ ##
    def insert_content(self, data:ReqChat):
        print("insert_content")
        self.cur.execute("insert into TB_CONTENT (CR_ID, USER_ID, CNT_ID, CNT_CONTENT, CNT_SEND_TIME) "
                         "values (?, ?, ?, ?, ?)",
                         ("OE_1", data.user_id, 1, data.msg, datetime.now().strftime("%Y-%m-%d %H:%M:%S")) )

        self.commit_db()
        print("save complete")

    def find_content(self):
        rows_data = self.cur.execute("select * from TB_CONTENT").fetchall()
        # CR_ID, CR_NM
        if len(rows_data) == 0:
            return None

        find_result_list = list()
        for row in rows_data:
            find_result_list.append(row)
        return find_result_list

    def find_content_by_content(self, cnt_content):
        pass
        # todo: content_id로 찾아 msg_content를 찾을 수 있도록 생각하기

    def find_content_by_send_time(self):
        pass

    def delete_content(self):
        pass

    ## TB_read_cnt ================================================================================ ##
    def insert_read_cnt(self, cnt_id, user_id, is_read):
        pass

    def find_read_cnt(self):
        pass


    ## TB_banchat ================================================================================ ##
    def insert_banchat(self, bc_no, bc_type, bc_content):
        pass

    def find_banchat(self):
        pass

    def banchat_warning(self):
        pass



if __name__ == '__main__':
    db = DBConnector()
    c = DBConnector.conn

    db.create_tables()

    # user = db.insert_user("hong", "홍길동", "hong@naver.com", "hong1234", "2023.07.12", "", "")




    # b = db.chatroom_id_creation("OE", "개인방")

   # find_chatroom_list = db.find_chatroom_by_id()

    # for i in range(1, 3):
    #     db.delete_chatroom(f"OE_{i}")
    # db.delete_chatroom("OE_8")

    # a = c.execute("select * from TB_CHATROOM where CR_ID = ?", ("OE_1",)).fetchall()
    # print(a)
    # b = a[0]
    # print(b)

    chatroom_list = db.find_chatroom()
    print(chatroom_list)

    # db.commit_db()
    db.end_conn()


