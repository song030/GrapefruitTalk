import sqlite3
import pandas as pd
from datetime import datetime
import random

# 이메일 전송을 위한 SMTP프로토콜 접근 지원을 위한 라이브러리
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# 이메일의 유효성점검을 위한 정규 표현식 지원 라이브러리
import re

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QListView, QLabel, QLayout, QCompleter

from Source.Views.UI_MainWidget import Ui_MainWidget

from Source.Views.Font import Font
from Source.Views.DialogWarning import DialogWarning
from Source.Views.TalkBox import TalkBox
from Source.Views.DateLine import DateLine
from Source.Views.ListItem import ListItem
from Source.Client.Client import Client
from Source.Client.ReceiveThread import ReceiveThread
from Source.Main.DataClass import *


class MainWidget(QWidget, Ui_MainWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 화면 초기화
        self.set_ui()

        # 변수 및 위젯 선언
        self.dlg_warning = DialogWarning()

        self.user_id = "test0"
        self.room_id = 0

        # 회원가입 요건 충족
        self.r_email = ''
        self.v_num = ''
        self.join_permission = False
        self.list_v_nums = []

        # 인증메일 송신자
        self.s_email = 'rhrnaka@gmail.com'
        self.s_pwd = 'jqlhqjmuddnptivj'

        # 이벤트 연결
        self.connect_event()

        # 서버 연결
        # self.client = Client()
        # if not self.client.connect():
        #     self.disconnect()
        # else:
        #     self.receive_thread = ReceiveThread(self.client)
        #     self.address = self.client.address()
        #     self.connect_thread_signal()
        #     self.receive_thread.start()
        #     self.client.send(self.user_id)

    # 화면 글꼴 설정
    def set_font(self):
        font_txt_normal = Font.text(3)
        font_btn = Font.button(3)

        # ===== 메인 (로그인)
        self.lbl_main_title.setFont(Font.title(1))
        self.lbl_main_name.setFont(Font.title(5))
        self.lbl_main_team.setFont(Font.title(5))
        self.lbl_join.setFont(Font.text(3))

        self.edt_login_id.setFont(font_txt_normal)
        self.edt_login_pwd.setFont(font_txt_normal)
        self.btn_login.setFont(font_btn)

        # ===== 회원가입
        self.lbl_join_title.setFont(Font.title(2))

        self.edt_join_id.setFont(font_txt_normal)
        self.edt_join_pwd1.setFont(font_txt_normal)
        self.edt_join_pwd2.setFont(font_txt_normal)
        self.edt_join_email.setFont(font_txt_normal)
        self.edt_join_nick.setFont(font_txt_normal)

        self.btn_join_id.setFont(font_btn)
        self.btn_join_mail.setFont(Font.button(5))
        self.btn_join.setFont(font_btn)
        self.btn_join_cancel.setFont(font_btn)

        self.cb_join_email.setFont(font_txt_normal)

        # ===== 채팅방
        self.lbl_room_name.setFont(Font.button(3))
        self.edt_txt.setFont(font_txt_normal)
        self.splitter.moveSplitter(100, 0)

    # 화면 위젯 초기화
    def set_ui(self):
        self.set_font()

        # ===== 메인 (로그인)
        self.stack_main.setCurrentWidget(self.page_login)

        # ===== 회원가입
        self.cb_join_email.setView(QListView())
        self.cb_join_email.addItems(["naver.com", "gmail.com", "nate.com", "hanmail.com"])

        self.back = QLabel(self)
        self.back.setGeometry(0, 0, 1024, 860)
        self.back.setStyleSheet("background-color: rgba(20, 20, 20, 50);")
        self.back.hide()

    # 이벤트 연결
    def connect_event(self):
        # ===== 공통
        self.dlg_warning.showEvent = lambda e: self.back.show()
        self.dlg_warning.closeEvent = lambda e: self.back.hide()

        # ===== 메인 (로그인)
        self.lbl_join.mousePressEvent = lambda e: self.stack_main.setCurrentWidget(self.page_join)
        self.btn_login.clicked.connect(self.check_login_info)

        # ===== 회원가입
        self.btn_join_id.clicked.connect(self.check_id_txt)
        self.btn_join.clicked.connect(self.join_input_check)
        self.btn_join_cancel.clicked.connect(lambda: self.stack_main.setCurrentWidget(self.page_login))
        self.btn_join_mail.clicked.connect(self.send_membership_email)
        self.btn_email_num.clicked.connect(self.check_varify_number)

        # ===== 대화방
        self.splitter.moveSplitter(100, 0)
        self.btn_send.clicked.connect(self.send_message)
        self.edt_txt.returnPressed.connect(self.send_message)

        # ===== 리스트 메뉴
        self.btn_single.clicked.connect(lambda: self.list_btn_check("single"))
        self.btn_multi.clicked.connect(lambda: self.list_btn_check("multi"))
        self.btn_friend.clicked.connect(lambda: self.list_btn_check("friend"))
        self.btn_out.clicked.connect(self.out_room)
        self.btn_add.clicked.connect(self.add_room)

    # 쓰레드 함수 연결
    def connect_thread_signal(self):
        self.receive_thread.res_message.connect(self.receive_message)
        self.receive_thread.res_login.connect(self.check_login)

    # 레이아웃 비우기
    def clear_layout(self, layout: QLayout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()

            if widget is not None:
                widget.setParent(None)
            # 아이템이 레이아웃일 경우 재귀 호출로 레이아웃 내의 위젯 삭제
            else:
                self.clear_layout(item.layout())

    # ================================================== 회원가입 ==================================================

    def check_duplicate_id(self):
        membership_id = self.edt_join_id.text()
        self.client.send(ReqMembership(membership_id))

    def check_id_txt(self):
        """아이디 중복 확인"""
        user_id = self.edt_join_id.text()
        print(user_id, self.id_list)
        if user_id in self.id_list:
            self.dlg_warning.set_dialog_type(1, "로그인 안내", "사용 중인 아이디입니다.")
            self.join_permission = True
        elif user_id not in self.id_list:
            self.dlg_warning.set_dialog_type(1, "로그인 안내", "사용가능한 아이디입니다.")
            self.join_permission = False

    def check_id_condition(self):
        """아이디 최대 16자 조건 확인"""
        if len(self.create_id.text()) >= 16:
            self.dlg_warning.set_dialog_type(1, "로그인 안내", "아이디는 최대 16자까지 입력 가능합니다.")
            self.join_permission = False

    def check_pwd_condition(self):
        """비밀번호 조건 확인 함수 : 영대문자(1), 특수문자(1) 필수포함 및 최대 16자"""

        insert_pwd = self.edt_join_pwd1.text()
        REGEX_PASSWORD = '^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{5,16}$'
        if not re.fullmatch(REGEX_PASSWORD, insert_pwd):
            self.dlg_warning.set_dialog_type(1, "비밀번호를 확인하세요. 최소 1개 이상의 소문자, 대문자, 숫자, 특수문자, 길이는 5~16자리 이어야 합니다.")
            self.join_permission = False

        # num_ = 0
        # upper_ = 0
        # special_ = 0
        # list_special = ['!', '@', '#', '$', '%', '^', '&', '*']
        #
        # for word in insert_pwd:
        #     if word.isupper():
        #         upper_ += 1
        #     if word.isdecimal():
        #         num_ += 1
        #     if word in list_special:
        #         special_ += 1
        #
        # if upper_ == 0:
        #     self.dlg_warning.set_dialog_type(1, "비밀번호 필수 포함", "비밀번호에 최소 영대문자 1글자 이상 포함되어야 합니다.")
        #     self.join_permission = False
        # elif special_ == 0:
        #     self.dlg_warning.set_dialog_type(1, "비밀번호 필수 포함", "최소 특수문자 1글자 이상 포함되어야 합니다.")
        #     self.join_permission = False
        # elif len(insert_pwd) >= 17:
        #     self.dlg_warning.set_dialog_type(1, "비밀번호 글자 수 제한", "비밀번호는 최대 16자까지 입력가능합니다.")
        #     self.join_permission = False
        # elif insert_pwd == '':
        #     self.dlg_warning.set_dialog_type(1, "비밀번호 입력없음", "비밀번호를 입력해주세요")
        #     self.join_permission = False
        # else:
        #     self.join_permission = True

    def check_between_pwd(self):
        """비밀번호1, 2 일치 확인"""
        insert_pwd_1 = self.edt_join_pwd1.text()
        insert_pwd_2 = self.edt_join_pwd2.text()

        if insert_pwd_1 != insert_pwd_2:
            self.dlg_warning.set_dialog_type(1, "비밀번호 일치 오류", "비밀번호가 서로 일치하지 않습니다.")
            self.join_permission = False
        else:
            self.join_permission = True

    def check_nickname_condition(self):
        """닉네임 최대 20자 조건 확인 : 20자 이하의 한글/영문/숫자 조합"""
        insert_nickname = self.edt_join_nick.text()
        if len(insert_nickname) > 20:
            self.dlg_warning.set_dialog_type(1, "닉네임 글자 수 제한", "닉네임은 최대 20자까지 가능합니다.")
            self.join_permission = False
        else:
            self.join_permission = True

    def check_email_condition(self):
        """이메일 형식 유효성 확인"""
        email_addr = self.cb_join_email.currentText()
        self.r_email = self.edt_join_email.text()
        # reg = '([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
        reg = "^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$"
        if bool(re.match(reg, self.r_email)):
            self.dlg_warning.set_dialog_type(1, "이메일 유효 검사", "유효한 이메일 주소 입니다.")
            self.join_permission = True
        else:
            self.dlg_warning.set_dialog_type(1, "이메일 유효 검사", "유효한 이메일 주소가 아닙니다.")
            self.join_permission = False

    def make_email_content(self):
        """인증메일 html 리턴"""

        verify_num = random.sample(range(0, 10), k=4)
        list_v_num = [str(num) for num in verify_num]

        for i in range(4):
            self.v_num += list_v_num[i]
        del list_v_num[:]

        self.list_v_nums.append(self.v_num)

        for num in self.list_v_nums:
            if num == verify_num:
                continue
            else:
                break

        To = f'{self.r_email}'
        e_content_1 = f"이메일 계정 인증을 위한 인증번호 4자리를 보내드립니다."
        e_content_2 = f"아래의 인증번호 4자리를 인증번호 칸에 입력하세요."
        e_content_3 = f"인증번호 : {verify_num[0]} {verify_num[1]} {verify_num[2]} {verify_num[3]}"
        title = "[자몽톡] 회원가입용 이메일 계정을 인증해주세요"

        html = f"""\
        <!DOCTYPE html>
         <html lang="en">
         <head>
             <meta charset="UTF-8" />
             <meta name="viewport" content="width=device-width, initial-scale=1.0" />
             <title>{title}</title>
         </head>
         <body>
             <h4>안녕하세요. {self.name}님. </h4>
             <p style="padding:5px 0 0 0;">{e_content_1} </p>
             <p style="padding:5px 0 0 0;">{e_content_2} </p>
             <p style="padding:5px 0 0 0;">{e_content_3} </p>
         </body>
         </html>
         """

        msg = MIMEMultipart('alternative')
        msg['Subject'] = title
        msg['From'] = self.s_email
        msg['To'] = self.r_email
        html_msg = MIMEText(html, 'html')
        msg.attach(html_msg)

        return msg

    def send_membership_email(self):
        # SMTP()서버의 도메인 및 포트를 인자로 접속하여 객체 생성
        server = smtplib.SMTP('smtp.gmail.com', 587)
        # SSL : SMTP_SSL('smtp.gmail.com', 465)

        # 접속 후 프로토콜에 맞춰 먼저 SMTP서버에 HELLO 메세지를 전송한다.
        server.ehlo()

        # 서버의 암호화 방식을 설정 -> TLS : Gmail 권장, SSL보다 향상된 보안
        server.starttls()

        # 서버 로그인
        server.login(self.s_email, self.s_pwd)

        # 이메일 발송
        try:
            server.sendmail(self.s_email, self.r_email, self.make_email_content().as_string())
            self.dlg_warning.set_dialog_type(1, "이메일 발송", "가입을 위한 인증번호 이메일이 발송되었습니다.")
            print("이메일 전송 성공")
        except:
            print("이메일 전송 실패")

        # 작업을 마친 후 SMTP와의 연결을 끊는다.
        server.quit()

    def check_varify_number(self):
        """발송한 인증번호 / 입력한 인증번호의 일치 여부 확인"""
        insert_v_num = self.lbl_email_num.text()
        if self.v_num == insert_v_num:
            self.dlg_warning.set_dialog_type(1, "인증번호 확인", "이메일 인증 완료")
            self.join_permission = True
        else:
            self.dlg_warning.set_dialog_type(1, "인증번호 확인", "이메일 인증 실패, 확인 후 재입력 해주시기 바랍니다.")
            self.join_permission = False

    def assign_random_image(self):
        """랜덤으로 프로필 사진을 배정함"""
        num = random.randrange(1, 5)
        img = f'./Images/{num}.png'
        return img

    def join_input_check(self):
        """회원가입 정보 입력 , 서버 허가 요청 송신"""
        if self.join_permission:
            self.dlg_warning.set_dialog_type(2, "회원가입 안내", "※회원가입 완료※ 환영 합니다")
            if self.dlg_warning.exec():
                self.stack_main.setCurrentWidget(self.page_talk)
                self.init_talk()
                self.init_list("multi")
            else:
                pass
        else:
            self.dlg_warning.set_dialog_type(2, "회원가입 안내", "※회원가입실패※ 잘못된 정보 입력")
            self.dlg_warning.exec()

    # ==================================================== 로그인 ==================================================

    # 서버 쪽으로 보낼 정보만 담고 있는 함수
    def check_login_info(self):
        self.id_ = self.edt_login_id.text()
        self.pwd_ = self.edt_login_pwd.text()
        self.client.send(ReqLogin(self.id_, self.pwd_))

    # 로그인 요청에 대한 결과 함수
    def check_login(self, data: PerLogin):
        """입력 ID, PASSWORD 확인 함수"""
        print(data.rescode)
        if data.rescode == 0:
            self.dlg_warning.set_dialog_type(1, '로그인 안내', "※로그인 실패※ \n 존재하지 않는 아이디/비밀번호 입니다. \n 다시 확인해주세요.")
            self.dlg_warning.exec()
            return False
        elif data.rescode == 1:
            self.dlg_warning.set_dialog_type(1, '로그인 안내', "※로그인 실패※ \n 잘못된 아이디 또는 패스워드 입니다.")
            self.dlg_warning.exec()
            return False
        else:
            self.dlg_warning.set_dialog_type(1, '로그인 안내', f"※로그인 완료※ \n {self.id_}님 로그인 완료")
            self.dlg_warning.exec()
            return True

    # ================================================== 대화 화면 ==================================================

    # 대화 방 초기화
    def init_talk(self):
        self.add_date_line()

        text = "말풍선선선선~~~~\n 말풍선!!\nzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
        for i in range(5):
            self.add_talk(0, "자몽자몽", text, datetime.now())

        # self.clear_layout(self.layout_talk)
        # talkbox = TalkBox("", "자몽자몽", text, datetime.now())
        # self.layout_talk.addLayout(talkbox.layout)

    # 일자 표시선 추가
    def add_date_line(self):
        talkbox = DateLine(datetime.now())
        self.layout_talk.addLayout(talkbox.layout)

    # 대화 박스 추가
    def add_talk(self, t_img: int, t_nick: str, t_text: str, t_time: datetime):
        talkbox = TalkBox(t_img, t_nick, t_text, t_time)
        self.layout_talk.addLayout(talkbox.layout)

    # 메시지 발송
    def send_message(self):
        # 네트워크 발신 내용 추가하기
        text = self.edt_txt.text()
        if self.client.send(ReqChat(self.user_id, 0, text)):
            print("발송 완료")
            self.add_talk(0, "발송", text, datetime.now())
            pass

        self.edt_txt.setText("")

    # 메시지 수신
    def receive_message(self, data: ReqChat):
        print("in receive")
        self.add_talk(0, data.user_id, data.msg, datetime.now())

    # ==============================================================================================================

    # ================================================== 리스트 메뉴 ==================================================

    # 리스트 메뉴는 반드시 하나가 노출 되어야 하기 때문에
    # 활성화 버튼 한번 더 클릭 할 경우 화면 변화가 없도록 하기 위해 예외처리 추가
    def list_btn_check(self, t_type):
        clear_check = False

        if t_type == "single":
            if not self.btn_single.isChecked():
                self.btn_single.setChecked(True)
            else:
                self.btn_add.setVisible(False)

                # 다른 버튼 체크 비활성
                self.btn_multi.setChecked(False)
                self.btn_friend.setChecked(False)
                clear_check = True

        elif t_type == "multi":
            if not self.btn_multi.isChecked():
                self.btn_multi.setChecked(True)
            else:
                self.btn_add.setVisible(False)

                # 다른 버튼 체크 비활성
                self.btn_single.setChecked(False)
                self.btn_friend.setChecked(False)
                clear_check = True

        elif t_type == "friend":
            if not self.btn_friend.isChecked():
                self.btn_friend.setChecked(True)
            else:
                self.btn_add.setVisible(True)

                # 다른 버튼 체크 비활성
                self.btn_single.setChecked(False)
                self.btn_multi.setChecked(False)
                clear_check = True

        # 출력 메뉴가 달라진 경우 레이아웃 비우로 리스트 다시 출력
        if clear_check and self.layout_list.count() > 0:
            self.clear_layout(self.layout_list)
            self.init_list(t_type)

    # 리스트 메뉴 초기화
    def init_list(self, t_type):
        # 1:1 단톡방
        if t_type == "single":
            # 온라인
            online = QLabel()
            online.setFont(Font.button(3))
            self.layout_list.addWidget(online)

            for i in range(3):
                item = ListItem("닉네임", "마지막 메시지 입니다.")
                item.set_info(datetime.now(), i)
                self.layout_list.addLayout(item.layout)

            on_num = self.layout_list.count() - 1
            online.setText(f"온라인 - {on_num}명")

            # 오프라인
            offline = QLabel()
            offline.setFont(Font.button(3))
            self.layout_list.addWidget(offline)

            for i in range(3):
                item = ListItem("닉네임", "마지막 메시지 입니다.")
                item.set_info(datetime.now(), i)
                self.layout_list.addLayout(item.layout)

            off_num = self.layout_list.count() - 1 - on_num
            offline.setText(f"오프라인 - {off_num}명")

        # 단체방
        elif t_type == "multi":
            for i in range(5):
                item = ListItem("닉네임", "상태상태상태상태상태상태")
                item.set_info(datetime.now(), i)
                item.member_cnt = 10 - i
                self.layout_list.addWidget(item.frame)
                item.frame.mousePressEvent = lambda _, v=item: self.open_chat_room(v)

        # 채팅방 멤버 리스트
        elif t_type == "member":
            self.btn_add.setVisible(False)
            # 온라인
            online = QLabel()
            online.setFont(Font.button(3))
            self.layout_list.addWidget(online)

            for i in range(3):
                item = ListItem(f"member{i}", "멤버", "상태상태상태상태상태상태")
                self.layout_list.addWidget(item.frame)
                # --- 우클릭 : 친구 추가 메뉴
                item.frame.setContextMenuPolicy(Qt.ActionsContextMenu)
                request_action = QAction("친구 요청", item.frame)
                request_action.triggered.connect(self.friend_request)
                item.frame.addAction(request_action)
                item.frame.setStyleSheet("QMenu::item {color: #E6A157; background: #FFF3E2; font-size: 12px;}"
                                         "QMenu::item::selected{color: #FFF3E2; background: #E6A157;}")

            on_num = self.layout_list.count() - 1
            online.setText(f"온라인 - {on_num}명")

            # 오프라인
            offline = QLabel()
            offline.setFont(Font.button(3))
            self.layout_list.addWidget(offline)

            for i in range(3):
                item = ListItem(f"member{i}", "멤버", "상태상태상태상태상태상태")
                self.layout_list.addWidget(item.frame)

            off_num = self.layout_list.count() - 1 - on_num
            offline.setText(f"오프라인 - {off_num}명")

        # 친구 리스트
        elif t_type == "friend":
            self.btn_add.setVisible(False)
            # 온라인
            online = QLabel()
            online.setFont(Font.button(3))
            self.layout_list.addWidget(online)

            for i in range(3):
                item = ListItem(f"friend{i}", "친구", "상태상태상태상태상태상태")
                self.layout_list.addWidget(item.frame)

            on_num = self.layout_list.count() - 1
            online.setText(f"온라인 - {on_num}명")

            # 오프라인
            offline = QLabel()
            offline.setFont(Font.button(3))
            self.layout_list.addWidget(offline)

            for i in range(3):
                item = ListItem(f"friend{i:53d}", "닉네임", "상태상태상태상태상태상태")
                self.layout_list.addWidget(item.frame)

            off_num = self.layout_list.count() - 1 - on_num
            offline.setText(f"오프라인 - {off_num}명")

    def open_chat_room(self, t_room: ListItem):
        """임시 ID로 검증"""
        t_room.no_msg_cnt = 0
        self.lbl_room_name.setObjectName(t_room.item_id)
        self.lbl_room_name.setText(f"{t_room.item_nm}")
        if "multi" in t_room.item_id:
            self.lbl_room_number.setText(f"{t_room.member_cnt}")
        elif "single" in t_room.item_id:
            self.lbl_room_number.clear()

    # 리스트 메뉴에서 원하는 줄 삭제 (가장 위에서 0부터 시작) --> ListItem 최상위 widget 추가로 메소드 변경
    def delete_list_item(self, t_row: int):
        self.layout_list.takeAt(t_row)

    # 현재 열여있는 방 나나기
    def out_room(self):
        pass

    # 방 추가 하기
    def add_room(self):
        self.dlg_add_chat.reset_dialog()
        if self.dlg_add_chat.exec():
            chat_name = self.dlg_add_chat.chat_name
            chat_mem = self.dlg_add_chat.members
            if not chat_name:
                chat_name = ', '.join(chat_mem)

            chat_mem = len(self.dlg_add_chat.members)

            if chat_mem == 1:      # 개인방 추가
                pass
            elif chat_mem > 1:     # 단체방 추가
                self.list_btn_check("multi")
                item = ListItem(f"multi{self.layout_list.count()}", f"{chat_name}", "새로 추가한 채팅방입니다.")
                item.member_cnt = chat_mem
                item.set_info(datetime.now(), 0)
                self.layout_list.addWidget(item.frame)
                item.frame.mousePressEvent = lambda _, v=item: self.open_chat_room(v)

                self.open_chat_room(item)
                self.clear_layout(self.layout_talk)
                self.add_date_line()
                self.add_notice_line(f"{self.user_id}")

    # 친구 추가 신청
    @pyqtSlot()
    def friend_request(self):
        print("친구 신청!")
# ==============================================================================================================
