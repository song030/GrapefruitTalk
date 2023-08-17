import sqlite3
import datetime

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
                  f"VALUES ('{data.id_}','{data.pw}','{data.nm}','{data.email}','{data.c_date}',1, 0)"
            self.conn.execute(sql)

            self.conn.execute(f"insert into CTB_USER_CHATROOM values ('PA_1', '{data.id_}');")

            self.conn.commit()
        except:
            self.conn.rollback()
            result.Success = False
        finally:
            self.conn.close()
        return result

    def change_user_state(self, data:ReqStateChange):
        sql = f"UPDATE CTB_USER SET USER_IMG = '{data.user_img}' WHERE USER_ID = '{data.user_id}'"
        self.conn.execute(sql)
        sql = f"UPDATE CTB_USER SET USER_STATE = '{data.user_state}' WHERE USER_ID = '{data.user_id}'"
        self.conn.execute(sql)

        self.conn.commit()

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
        print("create room ", data.cr_id_)
        # 채팅방 정보 추가
        self.conn.execute(f"insert into CTB_CHATROOM values (?, ?)", (data.cr_id_, data.title))

        # 방장 추가
        self.conn.execute(f"insert into CTB_USER_CHATROOM values (?, ?)", (data.cr_id_, data.user_id_))
        # 채팅 맴버 추가
        for member in data.member_id:
            self.conn.execute(f"insert into CTB_USER_CHATROOM values (?, ?)", (data.cr_id_, member))

        # 대화 테이블 생성
        self.conn.execute(f""" CREATE TABLE IF NOT EXISTS CTB_CONTENT_{data.cr_id_} (
                    "USER_ID" TEXT,
                    "CNT_ID" INTEGER,
                    "CNT_CONTENT" TEXT,
                    "CNT_SEND_TIME" TEXT,
                    PRIMARY KEY ("CNT_ID" AUTOINCREMENT));""")

        self.conn.commit()

        self.create_tb_read_cnt(JoinChat("", list(), list(), "", cr_id_=data.cr_id_))

    def delete_my_table(self, data:DeleteTable):
        """PK,FK를 고려하여 순서작성함"""

        if self.user_id != data.my_id:
            # CTB_CHATROOM 의 CR_ID 삭제
            sql_2 = f"DELETE FROM CTB_CHATROOM WHERE CR_ID = '{data.cr_id}' and USER_ID = '{data.my_id}'"
            self.conn.execute(sql_2)
            self.commit_db()
        else:
            sql_2 = f"DELETE FROM CTB_CHATROOM WHERE CR_ID = '{data.cr_id}'"
            #CTB_USER_CHATROOM의 CR_ID에 해당하는 내용 삭제
            sql_1 = f"DELETE FROM CTB_USER_CHATROOM WHERE CR_ID = '{data.cr_id}'"
            #CTB_READ_CNT_{CR_ID} 테이블 삭제
            sql_3 = f"DROP TABLE CTB_READ_CNT_{data.cr_id}"
            #CTB_CONTENT_{CR_ID} 테이블 삭제
            sql_4 = f"DROP TABLE CTB_CONTENT_{data.cr_id}"

            process_sql = [sql_1, sql_2, sql_3, sql_4]
            try:
                for sql in process_sql:
                    self.conn.execute(sql)
                self.commit_db()
            except Exception as e:
                self.conn.rollback()
                # 오류 처리 또는 로깅
                print(f"delete_my_table에서 Error occurred: {e}")

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

    def create_tb_read_cnt(self, data:JoinChat):
        """채팅방 별 메시지 읽음 구분 테이블 생성"""
        # 필요인자 : CR_ID, USER_ID
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.conn.executescript(f"""
        CREATE TABLE IF NOT EXISTS "CTB_READ_CNT_{data.cr_id_}" (
        "CR_ID" TEXT,
        "USER_ID" TEXT,
        "LAST_READ_TIME" TEXT,
        FOREIGN KEY("USER_ID") REFERENCES "CTB_CONTENT_{data.cr_id_}"("USER_ID") );
        """)
        for i in range(len(data.member_id)):
            self.conn.execute(f"""
            INSERT INTO CTB_READ_CNT_{data.cr_id_} (CR_ID, USER_ID, LAST_READ_TIME) VALUES ('{data.cr_id_}', '{data.member_id[i]}', '{now}' ) ;
            """)

        self.commit_db()

    def update_last_read_time(self, cr_id, user_id):
        """유저가 방을 열때마다 안읽은 날짜를 갱신한다"""

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = f"UPDATE CTB_READ_CNT_{cr_id} SET LAST_READ_TIME = '{now}' WHERE USER_ID = '{user_id}'"
        self.conn.execute(sql)

    def count_not_read_chatnum(self, cr_id, user_id):
        """유저별로 읽지 않음 메세지 수량을 계산한다"""
        # 필요인자 : CR_ID, USER_ID

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # now = datetime.now().strftime("%y/%m/%d %H:%M:%S")
        try:
            formatted_time = self.conn.execute(f"select LAST_READ_TIME from CTB_READ_CNT_{cr_id} where USER_ID = '{user_id}'").fetchone()[0]
        except:
            self.create_tb_read_cnt(JoinChat(user_id, [user_id], list(), "", cr_id_=cr_id))
            formatted_time = self.conn.execute(f"select LAST_READ_TIME from CTB_READ_CNT_{cr_id} where USER_ID = '{user_id}'").fetchone()[0]

        last_content = self.conn.execute(f"SELECT CNT_SEND_TIME FROM CTB_CONTENT_{cr_id} ORDER BY CNT_ID DESC LIMIT 1")
        if last_content.rowcount > 0:
            last_content = last_content.fetchone()[0]

            print(f"{user_id}가 채팅방에서 마지막으로 읽은 시간 : {formatted_time}")
            print(f"채팅방 {cr_id}의 마지막 메세지발송시간 : {last_content}")
            #마지막으로 읽은 시간보다 더 이후에 메시지가 발송되었는지 확인
            #메시지 발송 시간이 마지막 메시지 발송 시간보다 이전 또는 동일한지 확인
            cnt = self.conn.execute(f"SELECT CNT_SEND_TIME "
                                    f"FROM CTB_CONTENT_{cr_id} LEFT JOIN CTB_READ_CNT_{cr_id} ON "
                                    f"CTB_CONTENT_{cr_id}.USER_ID = CTB_READ_CNT_{cr_id}.USER_ID "
                                    f"WHERE '{formatted_time}' < CNT_SEND_TIME AND CNT_SEND_TIME <= '{last_content}' "
                                    f"AND CTB_CONTENT_{cr_id}.USER_ID = CTB_READ_CNT_{cr_id}.USER_ID").fetchall()

            if len(cnt) == 0:
                return 0
            else:
                return len(cnt[0])
        else:
            return 0


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
        sql1 = f"""select CTB_FRIEND.USER_ID as F_ID, CTB_USER.USER_NM, CTB_USER.USER_IMG, CTB_USER.USER_STATE, CTB_FRIEND.FRD_ACCEPT FROM CTB_FRIEND 
                            left join CTB_USER on CTB_FRIEND.USER_ID = CTB_USER.USER_ID 
                            WHERE CTB_FRIEND.FRD_ID = '{self.user_id}' and CTB_FRIEND.FRD_ACCEPT=1;"""

        sql2 = f"""select CTB_FRIEND.FRD_ID as F_ID, CTB_USER.USER_NM, CTB_USER.USER_IMG, CTB_USER.USER_STATE, CTB_FRIEND.FRD_ACCEPT FROM CTB_FRIEND 
                            left join CTB_USER on CTB_FRIEND.FRD_ID = CTB_USER.USER_ID 
                            WHERE CTB_FRIEND.USER_ID = '{self.user_id}' and CTB_FRIEND.FRD_ACCEPT=1;"""

        # 친구 수락 대기
        sql3 = f"""select CTB_FRIEND.USER_ID, CTB_USER.USER_NM, CTB_USER.USER_IMG, CTB_USER.USER_STATE, CTB_FRIEND.FRD_ACCEPT FROM CTB_FRIEND 
                    left join CTB_USER on CTB_FRIEND.USER_ID = CTB_USER.USER_ID WHERE CTB_FRIEND.FRD_ID = '{self.user_id}' and CTB_FRIEND.FRD_ACCEPT=0;"""

        df1 = pd.read_sql(sql1, self.conn)
        df2 = pd.read_sql(sql2, self.conn)
        df3 = pd.read_sql(sql3, self.conn)
        result = df1._append(df2)

        return result, df3

    def get_last_content(self, cr_id):
        df = pd.read_sql(f"select CNT_CONTENT, CNT_SEND_TIME from CTB_CONTENT_{cr_id} natural join CTB_USER order by CNT_SEND_TIME DESC LIMIT 1;", self.conn)
        return df

    def save_user_db(self, db:dict):
        client_cursor = self.conn.cursor()
        for table, df in db.items():
            client_cursor.executescript(f"DROP TABLE IF EXISTS {table}")
            df.to_sql(table, self.conn, index=False)
            if table[:2] == "OE":
                cr_id = table[-4:]
                sql = f"select USER_ID from CTB_USER_CHATROOM where CR_ID = {cr_id};"
                member = pd.read_sql(sql, self.conn)
                member = member.values.tolist()
                self.create_tb_read_cnt(JoinChat(member[0], member[1:], list(), "", cr_id_=cr_id))

        self.commit_db()

if __name__ == "__main__":

    pass
