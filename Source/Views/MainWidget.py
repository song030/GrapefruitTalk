import sqlite3

from datetime import datetime
import random

import pandas
import pandas as pd

#이메일 전송을 위한 SMTP프로토콜 접근 지원을 위한 라이브러리
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QWidget, QListView, QLabel, QLayout, QCompleter, QAction
from PyQt5 import QtTest

from Source.Views.UI_MainWidget import Ui_MainWidget

from Source.Views.Font import Font
from Source.Views.DialogWarning import DialogWarning
from Source.Views.AddChat import AddChat
from Source.Views.TalkBox import TalkBox
from Source.Views.DateLine import DateLine
from Source.Views.NoticeLine import NoticeLine
from Source.Views.ListItem import ListItem
from Source.Client.Client import Client
from Source.Client.ReceiveThread import ReceiveThread
from Source.Main.DataClass import *
from Source.Client.DBConnector import *

class MainWidget(QWidget, Ui_MainWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 화면 초기화
        self.set_ui()
        self.set_theme_color()

        # 변수 및 위젯 선언
        self.dlg_warning = DialogWarning()
        self.dlg_add_chat = AddChat()

        self.user_id = ""
        self.room_id = "PA_1"
        self.user_info:pandas.DataFrame

        # DB연결
        self.db = DBConnector()

        # 현재 리스트 화면에 노출되는 리스트 아이템 ListItem dict : self.chat_room["item_id"] = ListItem
        self.current_list = dict()

        # 회원가입 요건 충족
        self.r_email = ''
        self.v_num = ''
        self.join_permission = False
        self.list_v_nums = []
        self.use_id_check = False

        # 인증메일 송신자
        self.s_email = 'rhrnaka@gmail.com'
        self.s_pwd = 'sxrrxnbbfstqniee'

        # 이벤트 연결
        self.connect_event()

        # 서버 연결
        self.client = Client()
        if not self.client.connect():
            self.dlg_warning.exec()
            print("연결 불가능")
        else:
            self.receive_thread = ReceiveThread(self.client)
            self.address = self.client.address()
            self.connect_thread_signal()
            self.receive_thread.start()

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
        self.lbl_room_name.setFont(Font.button(4))
        self.edt_txt.setFont(font_txt_normal)

    # 화면 위젯 초기화
    def set_ui(self):
        self.set_font()

        # ===== 메인 (로그인)
        self.stack_main.setCurrentWidget(self.page_login)

        # ===== 회원가입
        self.widget_email.setVisible(False)
        self.cb_join_email.setView(QListView())
        self.cb_join_email.addItems(["naver.com", "gmail.com", "nate.com", "hanmail.com"])

        self.back = QLabel(self)
        self.back.setGeometry(0, 0, 1024, 860)
        self.back.setStyleSheet("background-color: rgba(20, 20, 20, 50);")
        self.back.hide()

        # ===== 리스트화면
        self.badge_single = self.init_badge(self.box_single, 16)
        self.badge_single.setVisible(False)
        self.badge_multi = self.init_badge(self.box_multi, 16)
        self.badge_multi.setVisible(False)

    # 안읽은 메시지 알림 마커 생성
    def init_badge(self, t_parent: QWidget, t_size: int):
        a_x, a_y = 25, 29
        badge_ = QLabel(t_parent)
        badge_.setGeometry(a_x, a_y, t_size, t_size)
        badge_.setAlignment(Qt.AlignCenter)
        badge_.setFont(Font.button(5))
        badge_.setStyleSheet(f"background: #E6A157;border: none;border-radius: {t_size // 2}px;color: white;font: bold 7px;")
        return badge_

    # 테마(색상) 설정 기능 > 나중에
    def set_theme_color(self, t_main: str = "#E6A157", t_room: str = "#FFF3E2"):
        self.page_login.setStyleSheet(f"background: {t_main}")
        self.page_join.setStyleSheet(f"background: {t_main}")
        self.scrollAreaWidgetContents.setStyleSheet(f"background: {t_room}")

    # 이벤트 연결
    def connect_event(self):
        # ===== 공통
        self.dlg_warning.showEvent = lambda e: self.back.show()
        self.dlg_warning.closeEvent = lambda e: self.back.hide()

        # ===== 메인 (로그인)
        self.lbl_join.mousePressEvent = lambda e: self.stack_main.setCurrentWidget(self.page_join)
        self.btn_login.clicked.connect(self.check_login_info)

        # ===== 회원가입
        self.btn_join_id.clicked.connect(self.check_duplicate_id)
        self.edt_join_id.textEdited.connect(self.check_id_condition)

        #비밀번호
        #닉네임

        self.btn_join_mail.clicked.connect(self.check_email_info)
        self.btn_email_num.clicked.connect(self.check_varify_number)
        self.btn_join.clicked.connect(self.check_membership_info)
        self.btn_join_cancel.clicked.connect(lambda: self.stack_main.setCurrentWidget(self.page_login))

        # ===== 대화방
        self.splitter.moveSplitter(100, 0)
        self.btn_send.clicked.connect(self.send_message)
        self.edt_txt.returnPressed.connect(self.send_message)

        # ===== 리스트 메뉴
        self.btn_single.clicked.connect(lambda: self.list_btn_check("single"))
        self.btn_multi.clicked.connect(lambda: self.list_btn_check("multi"))
        self.btn_member.clicked.connect(lambda: self.list_btn_check("member"))
        self.btn_friend.clicked.connect(lambda: self.list_btn_check("friend"))
        self.btn_out.clicked.connect(self.out_room)
        self.btn_add.clicked.connect(self.add_room)

    # 쓰레드 함수 연결
    def connect_thread_signal(self):
        # 메세지 발송
        self.receive_thread.res_message.connect(self.receive_message)

        # 로그인
        self.receive_thread.res_login.connect(self.check_login)

        # 회원가입
        self.receive_thread.res_regist.connect(self.join_input_check)
        self.receive_thread.res_duplicate_id_check.connect(self.check_id_txt)
        self.receive_thread.res_emailcheck_1.connect(self.check_email_condition)
        self.receive_thread.res_emailcheck_2.connect(self.email_check_or_not)

    # 레이아웃 비우기
    def clear_layout(self, layout: QLayout):
        if layout is None:
            return
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
        """send : 아이디 중복 확인"""
        insert_id = self.edt_join_id.text()
        self.client.send(ReqDuplicateCheck(insert_id))

    def check_id_txt(self, data: PerDuplicateCheck):
        """qt check : 아이디 중복 확인"""
        if data.isExisited:
            self.dlg_warning.set_dialog_type(1, 'used_id')
            self.join_permission = True
        else:
            self.dlg_warning.set_dialog_type(1, 'user_can_use_id')
            self.use_id_check = True
            self.join_permission = False
        self.dlg_warning.exec()

    def check_id_condition(self):
        """아이디 5~16자 조건 확인"""
        if 5 <= len(self.edt_join_id.text()) <= 16:
            return True
        else:
            return False

    def check_pwd_condition(self):
        """비밀번호 조건 확인 함수 : 영대문자(1), 특수문자(1) 필수포함 및 최대 16자"""

        insert_pwd = self.edt_join_pwd1.text()

        # 영대문자
        upper_mathct = re.match('.*[A-Z]+.*', insert_pwd)
        # 특수문자
        special_mark = re.findall('[`~!@#$%^&*(),<.>/?]+', insert_pwd)

        check = True
        if not upper_mathct:
            txt = "pw_alphabet_1"
            check = False
        elif not special_mark:
            txt = "pw_unique_word"
            check = False
        elif len(insert_pwd) < 5 or len(insert_pwd) > 16:
            check = False
            txt = "pw_len_limited"

        if not check:
            return check, txt

        all_condition = '^(?=.*[A-Z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{5,16}$'
        if re.match(all_condition, insert_pwd):
            return True, ''

    def check_between_pwd(self):
        """비밀번호1, 2 일치 확인"""
        insert_pwd_1 = self.edt_join_pwd1.text()
        insert_pwd_2 = self.edt_join_pwd2.text()

        if insert_pwd_1 == '':
            txt = "pw_input"
        elif insert_pwd_2 == '':
            txt = "pw_input"

        if insert_pwd_1 != insert_pwd_2:
            txt = "pw_not_match"
            return False, txt
        else:
            return True, ''

    def check_nickname_condition(self):
        """닉네임 최대 20자 조건 확인 : 20자 이하의 한글/영문/숫자 조합"""
        insert_nickname = self.edt_join_nick.text()

        if len(insert_nickname) > 20:
            txt = "nick_name_len_limit"
            return False, txt
        elif len(insert_nickname) == 0:
            txt = "nick_name_no_input"
            return False, txt
        else:
            return True, ''

    def check_email(self):
        if self.btn_email_num.isEnabled():
            return False
        else:
            return True

    def check_email_info(self):
        if len(self.edt_join_email.text()) == 0:
            self.dlg_warning.set_dialog_type(1, 'email_no_input')
            self.dlg_warning.exec()
        else:
            self.widget_email.setVisible(True)

            """send : 클라이언트 이메일 정보"""
            email_addr = self.cb_join_email.currentText()
            self.r_email = self.edt_join_email.text() + '@' + email_addr
            self.client.send(ReqEmailSend(self.r_email))

    def check_email_condition(self, data: PerEmailSend):
        """이메일 형식 유효성 확인"""
        if data.isSend:
            # 형식 유효 시 별도의 팝업은 뜨지 않고 이메일 전송.
            self.send_membership_email()
            self.join_permission = True
        else:
            self.dlg_warning.set_dialog_type(1, "not_vaild_email_addr")
            self.join_permission = False

    def email_content(self):
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
             <h4>안녕하세요. [자몽톡 가입요청자] 님. </h4>
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
            server.sendmail(self.s_email, self.r_email, self.email_content().as_string())
            self.dlg_warning.set_dialog_type(1, "email_send")
            print("이메일 전송 성공")
        except:
            print("이메일 전송 실패")

        # 작업을 마친 후 SMTP와의 연결을 끊는다.
        server.quit()

    def check_varify_number(self):
        if len(self.edt_join_email.text()) == 0:
            self.dlg_warning.set_dialog_type(1, 'email_num_no_input')
            self.dlg_warning.exec()
        else:
            """send : 발송 인증번호, 입력 인증번호"""
            insert_email_num = self.lbl_email_num.text()
            self.client.send(ReqEmailNumber(insert_email_num, self.v_num))

    def email_check_or_not(self, data: PerEmailNumber):
        """qt check : 발송한 인증번호 / 입력한 인증번호의 일치 여부 확인"""
        if data.ismatch:
            self.dlg_warning.set_dialog_type(1, "email_check")
            self.dlg_warning.exec()
            self.btn_join_mail.setEnabled(False)
            self.btn_email_num.setEnabled(False)
            self.join_permission = True
        else:
            self.dlg_warning.set_dialog_type(1, "email_not_check")
            self.dlg_warning.exec()
            self.join_permission = False

    def assign_random_image(self):
        """랜덤으로 프로필 사진을 배정함"""
        num = random.randrange(1, 25)
        img = f'./Images/img_profile_{num}.png'
        return img

    def check_membership_info(self):
        """send: 회원가입 입력 정보"""
        id = self.edt_join_id.text()
        pwd = self.edt_join_pwd2.text()
        nm = self.edt_join_nick.text()
        email = self.r_email
        c_date = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        img = '../../Images/img_profile.png'

        # 아이디 확인
        if not self.check_id_condition():
            self.dlg_warning.set_dialog_type(1, 'id_len_limited')
            self.dlg_warning.exec()

        # 비밀번호 확인
        elif not self.check_pwd_condition()[0]:
            self.dlg_warning.set_dialog_type(1, self.check_pwd_condition()[1])
            self.dlg_warning.exec()

        # 비밀번호+비밀번호확인 확인
        elif not self.check_between_pwd()[0]:
            self.dlg_warning.set_dialog_type(1, self.check_between_pwd()[1])
            self.dlg_warning.exec()

        # # 이메일 인증 확인
        elif not self.check_email():
            self.dlg_warning.set_dialog_type(1, "email_no_check")
            self.dlg_warning.exec()

        # 닉네임 확인
        elif not self.check_nickname_condition()[0]:
            self.dlg_warning.set_dialog_type(1, self.check_nickname_condition()[1])
            self.dlg_warning.exec()

        # 아이디 중복확인 진행 여부
        elif not self.use_id_check:
            self.dlg_warning.set_dialog_type(1, "used_id_no_check")
            self.dlg_warning.exec()

        else:
            self.user_id = id
            self.client.send(ReqMembership(id, pwd, nm, email, c_date, img))

    def join_input_check(self, data: PerRegist):
        """회원가입 정보 입력 , 서버 허가 요청 송신"""
        if data.Success:
            self.dlg_warning.set_dialog_type(2, "success_join_membership")
            if self.dlg_warning.exec():
                self.set_page_talk()
        else:
            self.dlg_warning.set_dialog_type(2, "failed_join_membership")
            self.dlg_warning.exec()

    # ==================================================== 로그인 ==================================================

    def check_login_info(self):
        """send : 로그인 정보"""
        self.user_id = self.edt_login_id.text()
        pwd_ = self.edt_login_pwd.text()

        self.client.send(ReqLogin(self.user_id, pwd_))

        # 로그인 후 db에 유저 아이디 전달, 유저 정보 가져오기
        self.db.set_user_id(self.user_id)
        self.user_info = self.db.get_table("CTB_USER", user_id=self.user_id).iloc[0]
        print(self.user_info)


    def check_login(self, data: PerLogin):
        """qt : 입력 ID, PASSWORD 확인 함수"""
        if data.rescode == 0:
            self.dlg_warning.set_dialog_type(1, '로그인 안내', "※로그인 실패※ \n 존재하지 않는 아이디/비밀번호 입니다. \n 다시 확인해주세요.")
            self.dlg_warning.exec()
            return False
        elif data.rescode == 1:
            self.dlg_warning.set_dialog_type(1, '로그인 안내', "※로그인 실패※ \n 잘못된 아이디 또는 패스워드 입니다.")
            self.dlg_warning.exec()
            return False
        else:
            self.dlg_warning.set_dialog_type(1, '로그인 안내', f"※로그인 완료※ \n {self.user_id}님 로그인 완료")
            self.dlg_warning.exec()
            self.set_page_talk()
            return True

    # ================================================== 대화 화면 ==================================================

    # 채팅 화면 최초 출력
    def set_page_talk(self):
        print("user_id :", self.user_id)
        # -- 채팅 화면 초기화
        self.init_list("single")
        self.clear_layout(self.layout_list)
        self.init_list("multi")
        self.init_talk(self.room_id)
        # --- 스플리터, 스크롤 위치 보정
        self.splitter.setSizes([self.splitter.width() - 100, 100])
        QtTest.QTest.qWait(100)
        self.edt_txt.setText("")
        self.scroll_talk.ensureVisible(0, self.scrollAreaWidgetContents.height())
        # -- 화면 출력
        self.stack_main.setCurrentWidget(self.page_talk)

    # 채팅방 초기화 (입장)
    def init_talk(self, t_room_id):
        """
        :param t_room_id: ListItem.item_id
        """
        target_: ListItem = self.current_list[t_room_id]
        target_.no_msg_cnt = 0
        self.lbl_room_name.setObjectName(t_room_id)
        self.lbl_room_name.setText(f"{target_.item_nm}")
        # 채팅방 아이디로 조건 분기
        if "OA" in t_room_id:
            self.check_no_msg_cnt("multi")
            self.lbl_room_number.setText(f"{target_.member_cnt}")
        elif "OE" in t_room_id:
            self.check_no_msg_cnt("single")
            self.lbl_room_number.clear()
        # --- 임시 채팅방 데이터 설정
        self.clear_layout(self.layout_talk)
        self.add_date_line()
        self.add_notice_line(f"{self.user_id}")
        num_ = random.randrange(3, 8)
        text = "말풍선선선선~~~~\n 말풍선!!\nzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
        for i in range(num_):
            self.add_talk(0, "자몽자몽", text, datetime.now())
        # --- 스크롤 테스트 중
        self.scroll_talk.ensureVisible(0, self.scrollAreaWidgetContents.height())

    # 일자 표시선 추가
    def add_date_line(self):
        talkbox = DateLine(datetime.now())
        self.layout_talk.addLayout(talkbox.layout)

    # 입퇴장 안내 문구 추가
    def add_notice_line(self, t_nick: str, t_type: str = "입장"):
        noticeline = NoticeLine(t_nick, t_type)
        self.layout_talk.addLayout(noticeline.layout)

    # 대화 박스 추가
    def add_talk(self, t_img: int, t_nick: str, t_text: str, t_time: datetime):
        talkbox = TalkBox(t_img, t_nick, t_text, t_time)
        self.layout_talk.addLayout(talkbox.layout)

    # 메시지 발송
    def send_message(self):
        # 네트워크 발신 내용 추가하기
        text = self.edt_txt.text()

        if self.check_banchat():
            # widget = self.add_talk(0, "발송", text, datetime.now())
            chat = ReqChat(self.room_id, self.user_id, text)
            if self.client.send(chat):
                self.db.insert_content(chat)
                print("발송 완료")
                self.add_talk(self.user_info["USER_IMG"], self.user_info["USER_NM"], text, datetime.now())
                pass

            QtTest.QTest.qWait(100)
            self.edt_txt.setText("")
            self.scroll_talk.ensureVisible(0, self.scrollAreaWidgetContents.height())
        else:
            self.edt_txt.setStyleSheet("""color: rgb(255, 0, 4);""")
            self.edt_txt.setText('')
            self.dlg_warning.set_dialog_type(1, 'use_ban_word')
            self.dlg_warning.exec()

    # 금칙어 체크
    def check_banchat(self):
        text = self.edt_txt.text()

        banchat_df = self.db.get_table("CTB_BANCHAT")

        for i, banchat in banchat_df.iterrows():
            if text == banchat_df.BC_CONTENT[i]:
                print("금칙어 사용!!!!")
                return False
        return True

    # 메시지 수신
    def receive_message(self, data: ReqChat):
        self.add_talk(self, data.user_id, data.msg, datetime.now())

    # ==============================================================================================================

    # ================================================== 리스트 메뉴 ==================================================

    def get_list_info(self, t_type):
        df = self.db.get_list_menu_info(t_type)
        pass

    # 리스트 메뉴는 반드시 하나가 노출 되어야 하기 때문에
    # 활성화 버튼 한번 더 클릭 할 경우 화면 변화가 없도록 하기 위해 예외처리 추가
    def list_btn_check(self, t_type):
        clear_check = False

        if t_type == "single":
            if not self.btn_single.isChecked():
                self.btn_single.setChecked(True)
            else:
                self.btn_add.setVisible(True)

                # 다른 버튼 체크 비활성
                self.btn_multi.setChecked(False)
                self.btn_member.setChecked(False)
                self.btn_friend.setChecked(False)
                clear_check = True

        elif t_type == "multi":
            if not self.btn_multi.isChecked():
                self.btn_multi.setChecked(True)
            else:
                self.btn_add.setVisible(True)

                # 다른 버튼 체크 비활성
                self.btn_single.setChecked(False)
                self.btn_member.setChecked(False)
                self.btn_friend.setChecked(False)
                clear_check = True

        elif t_type == "member":
            if not self.btn_member.isChecked():
                self.btn_member.setChecked(True)
            else:
                self.btn_add.setVisible(False)

                # 다른 버튼 체크 비활성
                self.btn_single.setChecked(False)
                self.btn_multi.setChecked(False)
                self.btn_friend.setChecked(False)
                clear_check = True

        elif t_type == "friend":
            if not self.btn_friend.isChecked():
                self.btn_friend.setChecked(True)
            else:
                self.btn_add.setVisible(False)

                # 다른 버튼 체크 비활성
                self.btn_single.setChecked(False)
                self.btn_multi.setChecked(False)
                self.btn_member.setChecked(False)
                clear_check = True

        # 출력 메뉴가 달라진 경우 레이아웃을 비우고 리스트 다시 출력
        if clear_check and self.layout_list.count() > 0:
            self.clear_layout(self.layout_list)
            self.get_list_info(t_type)
            self.init_list(t_type)

    # 리스트 메뉴 초기화
    def init_list(self, t_type):
        self.btn_add.setVisible(True)
        self.current_list = dict()  # dict 초기화
        # 1:1 갠톡방
        if t_type == "single":
            # 온라인
            online = QLabel()
            online.setFont(Font.button(3))
            self.layout_list.addWidget(online)
            offline_items = list()

            # ListItem 객체 생성 : 접속 중 상태 확인 후 online 이면 바로 addwidget 아니면 offline 지역변수에 임보
            for i in range(7):
                item = ListItem(f"OE_{i:0>2}", f"개인방 {i+1}", "마지막 메시지 입니다.")
                item.set_info(datetime.now(), i)
                item.frame.mousePressEvent = lambda _, v=item.item_id: self.init_talk(v)
                self.current_list[item.item_id] = item
                if i < 4:       # --------- 접속 중 구분 조건문 → 추후 수정
                    self.layout_list.addWidget(item.frame)
                else:
                    offline_items.append(item)

            on_num = self.layout_list.count() - 1
            online.setText(f"온라인 - {on_num}명")

            # 오프라인
            offline = QLabel()
            offline.setFont(Font.button(3))
            self.layout_list.addWidget(offline)
            off_num = len(offline_items)
            offline.setText(f"오프라인 - {off_num}명")
            for item in offline_items:
                self.layout_list.addWidget(item.frame)

        # 단체방
        elif t_type == "multi":
            for i in range(5):
                if not i:
                    item = ListItem(f"PA_1", f"전체방", "마지막 메시지 입니다.")
                else:
                    item = ListItem(f"OA_{i:0>2}", f"단체방-{i}", "마지막 메시지 입니다.")
                item.set_info(datetime.now(), i)
                item.member_cnt = 10 - i
                item.frame.mousePressEvent = lambda _, v=item.item_id: self.init_talk(v)
                self.current_list[item.item_id] = item
                self.layout_list.addWidget(item.frame)

        # 채팅방 멤버 리스트
        elif t_type == "member":
            self.btn_add.setVisible(False)
            # 온라인
            online = QLabel()
            online.setFont(Font.button(3))
            self.layout_list.addWidget(online)
            offline_items = list()

            for i in range(6):
                item = ListItem(f"member{i}", "멤버", "상태상태상태상태상태상태")
                item.set_context_menu("친구 추가 요청", self.friend_request)  # 우클릭 메뉴
                # self.current_list[item.item_id] = item
                if i < 4:
                    self.layout_list.addWidget(item.frame)
                else:
                    offline_items.append(item)

            on_num = self.layout_list.count() - 1
            online.setText(f"온라인 - {on_num}명")

            # 오프라인
            offline = QLabel()
            offline.setFont(Font.button(3))
            self.layout_list.addWidget(offline)
            off_num = len(offline_items)
            offline.setText(f"오프라인 - {off_num}명")

            for item in offline_items:
                self.layout_list.addWidget(item.frame)

        # 친구 리스트
        elif t_type == "friend":
            self.btn_add.setVisible(False)

            # --- 친구 신청
            request_ = QLabel()
            request_.setFont(Font.button(3))
            self.layout_list.addWidget(request_)
            item = ListItem(f"request0", "친구 후보", '')
            item.set_button_box(self.add_friend)
            self.layout_list.addWidget(item.frame)
            reque_num = self.layout_list.count() - 1
            request_.setText(f"친구 요청 - {reque_num}명")

            # 온라인
            online = QLabel()
            online.setFont(Font.button(3))
            self.layout_list.addWidget(online)
            offline_items = list()

            for i in range(6):
                item = ListItem(f"friend{i}", "친구", "상태상태상태상태상태상태")
                item.set_context_menu("1:1 대화", self.move_single_chat, item)
                # self.current_list[item.item_id] = item
                if i < 3:       # --------- 접속 중 구분 조건문 → 추후 수정
                    self.layout_list.addWidget(item.frame)
                else:
                    offline_items.append(item)

            on_num = self.layout_list.count() - 1
            online.setText(f"온라인 - {on_num}명")

            # 오프라인
            offline = QLabel()
            offline.setFont(Font.button(3))
            self.layout_list.addWidget(offline)
            off_num = len(offline_items)
            offline.setText(f"오프라인 - {off_num}명")
            for item in offline_items:
                self.layout_list.addWidget(item.frame)

        self.check_no_msg_cnt(t_type)

    # 안읽은 메시지 배지 갱신
    def check_no_msg_cnt(self, t_type: str):
        target_ = None
        if t_type == "single":
            target_ = self.badge_single
        elif t_type == "multi":
            target_ = self.badge_multi
        else:
            return

        if target_ and self.current_list:
            total_num = 0
            for item in self.current_list.values():
                total_num += int(item.no_msg_cnt)

            if total_num:
                target_.setText(f"{total_num}")
                target_.setVisible(True)
                return

        target_.setVisible(False)

    # 리스트 메뉴에서 원하는 줄 삭제 (가장 위에서 0부터 시작) --> ListItem 최상위 widget 추가로 메소드 변경
    def delete_list_item(self, t_row: int):
        layout = self.layout_list
        for i in range(layout.count()):
            item = layout.itemAt(i)
            widget = item.widget()
            if t_row == i:
                if widget is not None:
                    widget.deleteLater()
                # 아이템이 레이아웃일 경우 재귀 호출로 레이아웃 내의 위젯 삭제
                else:
                    self.clear_layout(item.layout())

    # 현재 열려 있는 방 나가기
    def out_room(self):
        target_id = self.lbl_room_name.objectName()
        if target_id == "PA_1":
            self.dlg_warning.set_dialog_type(1, "cannot_exit_room")
            return
        else:
            self.dlg_warning.set_dialog_type(2, "exit_chat_room")
        if self.dlg_warning.exec():
            self.current_list[target_id]: ListItem.frame.deleter
            del self.current_list[target_id]

    # 방 추가 버튼 클릭 시 다이얼로그 연결
    def add_room(self):
        self.dlg_add_chat.reset_dialog()
        if self.dlg_add_chat.exec():
            chat_name = self.dlg_add_chat.chat_name
            chat_mem = self.dlg_add_chat.members
            if not chat_name:
                chat_name = ', '.join(chat_mem)

            member_cnt = len(self.dlg_add_chat.members)

            if member_cnt == 1:      # 개인방 추가
                self.new_chat_room("single", chat_name, chat_mem)
            elif member_cnt > 1:     # 단체방 추가
                self.new_chat_room("multi", chat_name, chat_mem)

    def new_chat_room(self, t_type: str, t_name: str, t_member: list):
        """
        새 채팅방 생성 함수
        :param t_type: single / multi
        :param t_name: 채팅방 이름
        :param t_member: 채팅방 참여멤버 (현재는 객체로 받고 있음 → DB 연결시 id로 수정)
        :return:
        """
        if t_type == "single":
            self.btn_single.setChecked(True)
            self.list_btn_check("single")
            item = ListItem(f"OE_{len(self.current_list):0>2}", f"{t_name}", "")
        elif t_type == "multi":
            self.btn_multi.setChecked(True)
            self.list_btn_check("multi")
            item = ListItem(f"OA_{len(self.current_list):0>2}", f"{t_name}", "")
        item.member_cnt = len(t_member)
        item.set_info(datetime.now(), 0)
        item.frame.mousePressEvent = lambda _, v=item.item_id: self.init_talk(v)
        self.current_list[item.item_id] = item
        self.layout_list.addWidget(item.frame)
        self.init_talk(item.item_id)    # 새 채팅방으로 이동

    # 친구 요청 수락/거절
    def add_friend(self, t_type):
        self.delete_list_item(0)
        self.delete_list_item(1)
        if t_type:
            item = ListItem(f"friend{self.layout_list.count()-2}", "새 친구", "신선한 상태")
            item.set_context_menu("1:1 대화", self.move_single_chat, item)
            self.current_list[item.item_id] = item
            self.layout_list.addWidget(item.frame)

    # 친구 추가 신청보내기
    @pyqtSlot()
    def friend_request(self):
        print("친구 신청!")

    # 친구와 1:1 대화하기
    @pyqtSlot()
    def move_single_chat(self, t_friend: ListItem):
        """
        :param t_friend
        """
        self.btn_single.setChecked(True)
        self.list_btn_check("single")
        for value_ in self.current_list.values():
            if value_.item_nm == t_friend.item_nm:
                self.init_talk(value_.item_id)
                return
        self.new_chat_room("single", t_friend.item_nm, [t_friend])

# ==============================================================================================================
