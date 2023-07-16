import sqlite3

# 정규식 표현
import re

import pandas as pd

from Source.Main.DataClass import *

class DBConnector:      # DB를 총괄하는 클래스
    def __init__(self):
        self.conn = sqlite3.connect("data.db", check_same_thread=False)

    def end_conn(self):  # db 종료
        self.conn.close()

    def commit_db(self):  # db 커밋
        self.conn.commit()

    # 테이블 비우기
    def clear_table(self, col_name):
        self.conn.execute(f"delete from {col_name}")
        self.commit_db()

    # 원하는 테이블의 원하는 정보 가져오기
    def get_table(self, tb_name: str, user_id="", add_where=""):
        sql = f"select * from {tb_name}"

        if user_id:
            sql += f" where USER_ID = '{user_id}'"

        if add_where:
            if user_id:
                sql += " and"
            else:
                sql += " where"

            sql += add_where

        df = pd.read_sql(sql, self.conn)
        return df

    # 원하는 데이터에 정도 일괄 추가
    def insert_data(self, tb_name, data: list):
        size = len(data[0])
        column = ""
        for i in range(size):
            column += "?, "
        column = column[:-2]
        print(column)

        for d in data:
            self.conn.execute(f"insert into {tb_name} values ({column})", d)
        self.commit_db()

    ## CREATE TABLES ======================================================================== ##

    # 테이블 초기 설정
    def init_tables(self):
        # 단체 방 정보추가
        self.conn.execute("insert into TB_CHATROOM values ('PA_1', '[단체방] 자몽톡 가입자');")

        # 단체방 대화 테이블 생성
        self.conn.executescript("""
            CREATE TABLE "TB_CONTENT_PA_1" (
                "USER_ID" TEXT,
                "CNT_ID" INTEGER,
                "CNT_CONTENT" TEXT,
                "CNT_SEND_TIME" TEXT,
                PRIMARY KEY ("CNT_ID" AUTOINCREMENT) );
                """)

        # 단체방 관리자 정보 추가
        self.conn.execute("insert into TB_USER_CHATROOM values ('PA_1', 'admin');")

        self.commit_db()

    ## TB_USER ================================================================================ ##
    # 회원 정보 테이블 값 입력
    def insert_user(self, user_id, user_name, user_email, user_pw,
                    user_create_date, user_img, user_state):
        self.conn.execute("insert into TB_USER (USER_ID, USER_NAME, USER_EMAIL, USER_PW, USER_CRATE_DATE, "
                  "USER_IMG, USER_STATE) values (?, ?, ?, ?, ?, ?, ?)",
                  (user_id, user_name, user_email, user_pw, user_create_date, user_img, user_state))
        self.commit_db()

    # 회원 정보 테이블 전체 조회
    def find_user(self):
        rows_data = self.conn.execute("select * from TB_USER").fetchall()
        if len(rows_data) == 0:
            return None

        find_result_list = list()
        for row in rows_data:
            find_result_list.append(row)
        return rows_data

    # user_id를 기준으로 행 조회
    def find_user_by_id(self, user_id: str):
        row = self.conn.execute("select * from TB_USER where USER_ID = ?", (user_id,)).fetchall()
        id = row[0]
        return id

    # user_id를 기준으로 행 삭제
    def delete_user(self, user_id: str):
        self.conn.execute("delete from TB_USER where USER_ID = ?", (user_id,))
        self.commit_db()

    # 회원 ID, PW 결과값 가져오기
    def login(self, data: ReqLogin) -> PerLogin:
        print("[ login ]")
        """클라이언트 로그인 요청 -> 서버 로그인 허가 """
        result: PerLogin = PerLogin(rescode=2, user_id_=data.id_)
        sql = f"SELECT * FROM TB_USER WHERE USER_ID = '{data.id_}' AND USER_PW = '{data.password}'"
        print(sql)
        df = pd.read_sql(sql, self.conn)
        row = len(df)
        print("row",row)

        if row in [None, 0]:
            result.rescode = 0
        # 입력한 아이디와 비밀번호, db에서 가진 아이디와 비밀번호
        # elif data.id_ != row[1] or data.password != row[2]:
        #     result.rescode = 1
        else:
            result.rescode = 2
        return result

    def membership_id_check(self, data: ReqDuplicateCheck) -> PerDuplicateCheck:
        """클라이언트 중복 아이디 확인 요청 -> 서버 db에서 아이디 중복 여부 응답"""
        result: PerDuplicateCheck = PerDuplicateCheck(isExisited=True)
        sql = f"SELECT * FROM TB_USER WHERE USER_ID = '{data.id_}'"
        row = pd.read_sql(sql, self.conn)

        if len(row) != 0:
            result.isExisited = True
        else:
            result.isExisited = False
        return result

    def email_check_1(self, data: ReqEmailSend) -> PerEmailSend:
        """클라이언트 이메일 전송 요청 -> 서버 이메일 전송완료 응답"""
        if re.match(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', data.r_email):
            result = PerEmailSend(True)
        else:
            result = PerEmailSend(False)
        return result

    def email_check_2(self, data: ReqEmailNumber) -> PerEmailNumber:
        """클라이언트 이메일 인증번호 요청 -> 서버 이메일 인증번호 허가"""
        if data.num1 == data.num2:
            result = PerEmailNumber(True)
        else:
            result = PerEmailNumber(False)
        return result

    def regist(self, data: ReqMembership) -> PerRegist:
        result: PerRegist = PerRegist(True)
        try:
            sql = f"INSERT INTO TB_USER (USER_ID, USER_PW, USER_NM, USER_EMAIL, USER_CREATE_DATE, USER_IMG, USER_STATE)" \
                  f"VALUES ('{data.id_}','{data.pw}','{data.nm}','{data.email}','{data.c_date}',1, 0)"
            self.conn.execute(sql)

            self.conn.execute(f"insert into TB_USER_CHATROOM values ('PA_1', '{data.id_}');")
            self.insert_content(ReqChat("PA_1", "", f"'{data.nm}'님이 입장했습니다."))
            self.conn.commit()
        except:
            self.conn.rollback()
            result.Success = False
        finally:
            self.conn.close()
        return result

    def change_user_state(self, data:ReqStateChange):
        sql = f"UPDATE TB_USER SET USER_IMG = {data.user_img} WHERE USER_ID = '{data.user_id}'"
        self.conn.execute(sql)
        sql = f"UPDATE TB_USER SET USER_STATE = '{data.user_state}' WHERE USER_ID = '{data.user_id}'"
        self.conn.execute(sql)

        self.conn.commit()
        return data

    ## TB_friend ================================================================================ ##
    # 친구 목록 정보 테이블 값 입력
    def insert_friend(self, data: ReqSuggetsFriend):
        self.conn.execute("insert into TB_FRIEND (USER_ID, FRD_ID, FRD_ACCEPT) values (?, ?, ?)", get_data_tuple(data))
        self.commit_db()

    # def insert_friend(self, data:PlusFriend):
    #     """get_data_tuple(data)[1]는 bool값이므로 db저장될 수 없음, 가공 필요"""
    #     self.conn.execute("insert into TB_FRIEND (USER_ID, FRD_ID, FRD_ACCEPT) values (?, ?, ?)",
    #                       (get_data_tuple(data)[0][0], get_data_tuple(data)[0][1], get_data_tuple(data)[1]))


    # 친구 요청 결과 적용
    def update_friend(self, data: ReqSuggetsFriend):
        print(get_data_tuple(data))
        self.conn.execute("update tb_friend set frd_accept = ? where user_id=? and frd_id=?", (data.result, data.user_id_, data.frd_id_))
        self.commit_db()

    # 친구 삭제
    def delete_friend(self, data: ReqSuggetsFriend):
        self.conn.execute(f"delete from TB_FRIEND where USER_ID = {data.user_id_} and FRD_ID = {data.frd_id_}")
        self.commit_db()

    ## TB_log ================================================================================ ##
    # LOG 정보 테이블 값 입력
    def insert_log(self, user_id, login_time, logout_time):
        self.conn.execute("insert into TB_LOG (USER_ID, LOGIN_TIME, LOGOUT_TIME) values (?, ?, ?)", (user_id, login_time, logout_time))
        self.commit_db()

    # LOG 테이블 전체 조회
    def find_log(self):
        rows_data = self.conn.execute("select * from TB_LOG").fetchall()
        if len(rows_data) == 0:
            return None

        find_result_list = list()
        for row in rows_data:
            find_result_list.append(row)
        return rows_data

    ## TB_chatroom ================================================================================ ##

    # 채팅방 개설
    def create_chatroom(self, data:JoinChat):
        # 인원 확인
        if len(data.member) == 0:
            return False

        # 타입 확인 - OE_ 1:1, OA_ 1:N
        elif len(data.member) == 1:
            _type = "OE_"
        else:
            _type = "OA_"

        # 일련번호 부여
        df = pd.read_sql(f"select MAX(CR_ID) from TB_CHATROOM where CR_ID like '{_type}%'", self.conn)
        df = df["MAX(CR_ID)"].iloc[0]

        if df is None:
            _num = 1
        else:
            _cr_id = df[3:]
            _cr_id = int(_cr_id)
            _num = _cr_id + 1

        _cr_id = f"{_type}{_num}"

        # 채팅방 정보 추가
        self.conn.execute(f"insert into TB_CHATROOM values (?, ?)", (_cr_id, data.title))

        # 방장 추가
        self.conn.execute(f"insert into TB_USER_CHATROOM values (?, ?)", (_cr_id, data.user_id_))
        # 채팅 맴버 추가
        for member in data.member:
            self.conn.execute(f"insert into TB_USER_CHATROOM values (?, ?)", (_cr_id, member))

        # 대화 테이블 생성
        self.conn.execute(f""" CREATE TABLE TB_CONTENT_{_cr_id} (
                            "USER_ID" TEXT,
                            "CNT_ID" INTEGER,
                            "CNT_CONTENT" TEXT,
                            "CNT_SEND_TIME" TEXT,
                            PRIMARY KEY ("CNT_ID" AUTOINCREMENT));""")

        self.conn.commit()

        return df

    def delete_table(self, data:DeleteTable):
        """PK,FK를 고려하여 순서작성함"""

        if len(data.user_id_list) > 1:
            # 나간 유저를 제외한 접속 멤버로 값 update
            df = pd.read_sql(f"SELECT * FROM TB_USER_CHATROOM WHERE CR_ID = '{data.cr_id}'", self.conn)
            user_id_list = df['USER_ID'].tolist()
            user_id_list.pop(f'{data.my_id}')

            self.conn.execute(f"UPDATE TB_USER_CHATROOM SET USER_ID = {user_id_list} WHERE CR_ID = {data.cr_id}")
            self.conn.commit()

        elif len(data.user_id_list) <= 1:
            # TB_USER_CHATROOM의 CR_ID에 해당하는 내용 삭제
            sql_1 = f"DELETE FROM TB_USER_CHATROOM WHERE CR_ID = {data.cr_id}"
            # TB_CHATROOM 의 CR_ID 삭제
            sql_2 = f"DELETE FROM TB_CHATROOM WHERE CR_ID = {data.cr_id}"
            # TB_READ_CNT_{CR_ID} 테이블 삭제
            sql_3 = f"DROP TABLE TB_READ_CNT_{data.cr_id}"
            # TB_CONTENT_{CR_ID} 테이블 삭제
            sql_4 = f"DROP TABLE TB_CONTENT_{data.cr_id}"

            process_sql = [sql_1, sql_2, sql_3, sql_4]
            try:
                for sql in process_sql:
                    self.conn.execute(sql)
                self.commit_db()
            except Exception as e:
                self.conn.rollback()
                # 오류 처리 또는 로깅
                print(f"delete_table에서 Error occurred: {e}")
            finally:
                self.end_conn()


    ## TB_user_chatroom ================================================================================ ##

    # 방 맴버 정보 조회
    def find_user_chatroom(self, cr_id):
        df = pd.read_sql(f"select * from TB_USER_CHATROOM where cr_id = '{cr_id}'", self.conn)
        return df["USER_ID"].values

    # 유저의 방 정보 조회
    def find_user_chatroom_by_to(self, user_id):
        df = pd.read_sql(f"select * from TB_USER_CHATROOM natural join TB_CHATROOM where USER_ID = {user_id}", self.conn)
        return df

    # # 채팅방 나가기
    # def delete_chatroom_member(self, cr_id: str, user_id):
    #     self.conn.execute("delete from TB_USER_CHATROOM where CR_ID = ? and USER_ID", (cr_id,user_id))
    #     self.commit_db()

    ## TB_content ================================================================================ ##
    # 대화 추가
    def insert_content(self, data:ReqChat):
        print("insert_content")
        self.conn.execute(f"insert into TB_CONTENT_{data.cr_id_} (USER_ID, CNT_CONTENT, CNT_SEND_TIME) "
                         "values (?, ?, ?)",
                         (data.user_id_, data.msg, datetime.now().strftime("%Y-%m-%d %H:%M:%S")) )

        self.commit_db()
        print("save complete")

    def find_content(self, cr_id):
        df = pd.read_sql(f"select * from TB_CONTENT_{cr_id}", self.conn)
        self.commit_db()
        return df

if __name__ == "__main__":
    # df = DBConnector().find_user_chatroom("PA_1")
    # print()
    pass