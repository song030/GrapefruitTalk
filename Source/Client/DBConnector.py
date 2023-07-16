import sqlite3

import pandas as pd

from Source.Main.DataClass import *

class DBConnector:      # DB를 총괄하는 클래스
    def __init__(self):
        self.conn = sqlite3.connect("../Client/data.db", check_same_thread=False)
        self.user_id = ""

    def set_user_id(self, user_id):
        print("db class set user_id", user_id)
        self.user_id = user_id

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
        self.conn.execute("insert into CTB_CHATROOM values ('PA_1', '[단체방] 자몽톡 가입자');")

        # 단체방 대화 테이블 생성
        self.conn.executescript("""
            CREATE TABLE "CTB_CONTENT_PA_1" (
                "USER_ID" TEXT,
                "CNT_ID" INTEGER,
                "CNT_CONTENT" TEXT,
                "CNT_SEND_TIME" TEXT,
                PRIMARY KEY ("CNT_ID" AUTOINCREMENT) );
                """)

        # 단체방 관리자 정보 추가
        self.conn.execute("insert into CTB_USER_CHATROOM values ('PA_1', 'admin');")

        self.commit_db()

    ## TB_USER ================================================================================ ##

    def regist(self, data: ReqMembership) -> PerRegist:
        result: PerRegist = PerRegist(True)
        try:
            sql = f"INSERT INTO CTB_USER (USER_ID, USER_PW, USER_NM, USER_EMAIL, USER_CREATE_DATE, USER_IMG, USER_STATE)" \
                  f"VALUES ('{data.id_}','{data.pw}','{data.nm}','{data.email}','{data.c_date}',0, 0)"
            self.conn.execute(sql)

            self.conn.execute(f"insert into CTB_USER_CHATROOM values ('PA_1', '{data.id_}');")

            self.conn.commit()
        except:
            self.conn.rollback()
            result.Success = False
        finally:
            self.conn.close()
        return result

    ## TB_friend ================================================================================ ##
    # 친구 목록 정보 테이블 값 입력
    def insert_friend(self, data):
        self.conn.execute("insert into CTB_FRIEND (USER_ID, FRD_ID, FRD_ACCEPT) values (?, ?, ?)", get_data_tuple(data))
        self.commit_db()

    # 친구 요청 결과 적용
    def update_friend(self, data):
        self.conn.execute("update ctb_friend set frd_accept = ? where user_id=? and frd_id=?", (data.result, data.user_id_, data.frd_id_))
        self.commit_db()

    # 친구 삭제
    def delete_friend(self, user_id, frd_id: str):
        self.conn.execute(f"delete from CTB_FRIEND where USER_ID = '{user_id}' and FRD_ID = '{frd_id}'")
        self.commit_db()

    # 친구 목록 가져오기
    def get_all_friend(self, user_id):
        df = pd.read_sql(f"select * from CTB_FRIEND where USER_ID = '{user_id}'", self.conn)
        return df

    # 채팅방 개설
    def create_chatroom(self, data:JoinChat):
        # data = JoinChat("admin", ["song030s"], "1:1 대화방 입니다.")
        len_member = len(data.member)

        # 인원 확인
        if len_member  == 0:
            return False

        # 방 아이디가 없는 경우 새로 생성
        if data.cr_id_ == "":
            # 타입 확인 - OE_ 1:1, OA_ 1:N
            if len(data.member) == 1:
                _type = "OE_"
            else:
                _type = "OA_"

            # 일련번호 부여
            df = pd.read_sql(f"select MAX(CR_ID) from CTB_CHATROOM where CR_ID like '{_type}%'", self.conn)
            df = df["MAX(CR_ID)"].iloc[0]

            if df is None:
                _num = 1
            else:
                _cr_id = df[3:]
                _cr_id = int(_cr_id)
                _num = _cr_id+1

            _cr_id = f"{_type}{_num}"
        else:
            _cr_id = data.cr_id_


        # 채팅방 정보 추가
        self.conn.execute(f"insert into CTB_CHATROOM values (?, ?)", (_cr_id, data.title))

        # 방장 추가
        self.conn.execute(f"insert into CTB_USER_CHATROOM values (?, ?)", (_cr_id, data.user_id_))
        # 채팅 맴버 추가
        for member in data.member:
            self.conn.execute(f"insert into CTB_USER_CHATROOM values (?, ?)", (_cr_id, member))

        # 대화 테이블 생성
        self.conn.execute(f""" CREATE TABLE CTB_CONTENT_{_cr_id} (
                    "USER_ID" TEXT,
                    "CNT_ID" INTEGER,
                    "CNT_CONTENT" TEXT,
                    "CNT_SEND_TIME" TEXT,
                    PRIMARY KEY ("CNT_ID" AUTOINCREMENT));""")

        self.conn.commit()

        return _cr_id

    ## TB_content ================================================================================ ##
    # 대화 추가
    def insert_content(self, data:ReqChat):
        print("insert_content")
        self.conn.execute(f"insert into CTB_CONTENT_{data.cr_id_} (USER_ID, CNT_CONTENT, CNT_SEND_TIME) "
                          "values (?, ?, ?)",
                          (data.user_id_, data.msg, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        self.commit_db()
        print("save complete")

    def get_content(self, cr_id):
        df = pd.read_sql(f"select * from CTB_CONTENT_{cr_id} natural join CTB_USER;", self.conn)
        return df

    ## 오른쪽 리스트 메뉴 출력용 함수 ================================================================================ ##

    def get_list_menu_info(self, t_type, cr_id="PA_1"):
        if t_type == "single":
            sql = "select CR_ID, CR_NM from CTB_CHATROOM NATURAL JOIN CTB_USER_CHATROOM where cr_ID like 'OE%' group by cr_id;"

        elif t_type == "multi":
            sql = "select CR_ID, CR_NM, count(USER_ID) from CTB_CHATROOM NATURAL JOIN CTB_USER_CHATROOM where cr_ID like '_A%' group by cr_id;"

        elif t_type == "member":
            sql = f"select CTB_USER.USER_ID, CTB_USER.USER_NM, CTB_USER.USER_IMG, CTB_USER.USER_STATE FROM CTB_USER_CHATROOM left join CTB_USER on CTB_USER_CHATROOM.USER_ID = CTB_USER.USER_ID WHERE CTB_USER_CHATROOM.CR_ID = '{cr_id}';"

        else:
            return False

        df = pd.read_sql(sql, self.conn)
        return df

    def get_friend_list(self):
        # 친구 목록
        sql1 = f"""select CTB_FRIEND.FRD_ID, CTB_USER.USER_NM, CTB_USER.USER_IMG, CTB_USER.USER_STATE, CTB_FRIEND.FRD_ACCEPT FROM CTB_FRIEND 
                    left join CTB_USER on CTB_FRIEND.FRD_ID = CTB_USER.USER_ID 
                    WHERE ( CTB_FRIEND.FRD_ID = '{self.user_id}' or CTB_FRIEND.USER_ID = '{self.user_id}') and CTB_FRIEND.FRD_ACCEPT=1;"""

        # 친구 수락 대기
        sql2 = f"""select CTB_FRIEND.FRD_ID, CTB_USER.USER_NM, CTB_USER.USER_IMG, CTB_USER.USER_STATE, CTB_FRIEND.FRD_ACCEPT FROM CTB_FRIEND 
                    left join CTB_USER on CTB_FRIEND.FRD_ID = CTB_USER.USER_ID WHERE CTB_FRIEND.FRD_ID = '{self.user_id}' and CTB_FRIEND.FRD_ACCEPT=0;"""

        df1 = pd.read_sql(sql1, self.conn)
        df2 = pd.read_sql(sql2, self.conn)

        return df1, df2

    def get_last_content(self, cr_id):
        df = pd.read_sql(f"select CNT_CONTENT, CNT_SEND_TIME from CTB_CONTENT_{cr_id} natural join CTB_USER order by CNT_SEND_TIME DESC LIMIT 1;", self.conn)
        return df


if __name__ == "__main__":
    # DBConnector().create_chatroom("")
    pass
