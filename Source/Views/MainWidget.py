from datetime import datetime

from PyQt5.QtWidgets import QWidget, QListView, QLabel, QLayout
from PyQt5.QtGui import QResizeEvent

from Source.Views.UI_MainWidget import Ui_MainWidget

from Source.Views.Font import Font
from Source.Views.DialogWarning import DialogWarning
from Source.Views.TalkBox import TalkBox
from Source.Views.DateLine import DateLine
from Source.Views.ListItem import ListItem
from Source.Client.Client import Client
from Source.Client.ReceiveThread import ReceiveThread
from Source.DataClass import *


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

        # 이벤트 연결
        self.connect_event()

        # 서버 연결
        self.client = Client()
        if not self.client.connect():
            self.disconnect()
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

        # ===== 회원가입
        self.btn_join_cancel.clicked.connect(lambda: self.stack_main.setCurrentWidget(self.page_login))
        self.btn_join.clicked.connect(self.join_input_check)

        # ===== 대화방
        self.splitter.moveSplitter(100,0)
        self.btn_send.clicked.connect(self.send_message)
        self.edt_txt.returnPressed.connect(self.send_message)

        # ===== 리스트 메뉴
        self.btn_single.clicked.connect(lambda: self.list_btn_check("single"))
        self.btn_multi.clicked.connect(lambda: self.list_btn_check("multi"))
        self.btn_friend.clicked.connect(lambda: self.list_btn_check("friend"))
        self.btn_out.clicked.connect(self.out_room)
        self.btn_add.clicked.connect(self.add_room)

    def connect_thread_signal(self):
        self.receive_thread.res_message.connect(self.receive_message)

    # 레이아웃 비우기
    def clear_layout(self, layout:QLayout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()

            if widget is not None:
                widget.setParent(None)
            # 아이템이 레이아웃일 경우 재귀 호출로 레이아웃 내의 위젯 삭제
            else:
                self.clear_layout(item.layout())

    # ================================================== 회원가입 ==================================================

    # 회원가입 입력확인
    def join_input_check(self):

        self.dlg_warning.set_dialog_type(2, "test")

        if self.dlg_warning.exec():
            self.stack_main.setCurrentWidget(self.page_talk)
            self.init_talk()
            self.init_list("multi")
        else:
            pass

    # ==============================================================================================================

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
    def add_talk(self, t_img:int, t_nick:str, t_text:str, t_time:datetime):
        talkbox = TalkBox(t_img, t_nick, t_text, t_time)
        self.layout_talk.addLayout(talkbox.layout)

    # 메시지 발송
    def send_message(self):
        # 네트워크 발신 내용 추가하기
        text = self.edt_txt.text()
        if self.client.send(text):
            print("발송 완료")
            # self.add_talk(0, "테스트", text, datetime.now())
            pass

        self.edt_txt.setText("")

    # 메시지 수신
    def receive_message(self, data:ReqChat):
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
                item.set_member_count(10 - i)
                self.layout_list.addLayout(item.layout)

        # 친구 리스트
        elif t_type == "friend":
            # 온라인
            online = QLabel()
            online.setFont(Font.button(3))
            self.layout_list.addWidget(online)

            for i in range(3):
                item = ListItem("닉네임", "상태상태상태상태상태상태")
                self.layout_list.addLayout(item.layout)

            on_num = self.layout_list.count() - 1
            online.setText(f"온라인 - {on_num}명")

            # 오프라인
            offline = QLabel()
            offline.setFont(Font.button(3))
            self.layout_list.addWidget(offline)

            for i in range(3):
                item = ListItem("닉네임", "상태상태상태상태상태상태")
                self.layout_list.addLayout(item.layout)

            off_num = self.layout_list.count() - 1 - on_num
            offline.setText(f"오프라인 - {off_num}명")

        self.delete_list_item(2)

    # 리스트 메뉴에서 원하는 줄 삭제 (가장 위에서 0부터 시작)
    def delete_list_item(self, t_row: int):
        layout = self.layout_list
        for i in range(layout.count()):
            item = layout.itemAt(i)
            widget = item.widget()

            if widget is None and t_row == i:
                self.clear_layout(item.layout())

    # 현재 열여있는 방 나나기
    def out_room(self):
        pass

    # 방 추가 하기
    def add_room(self):
        if self.btn_single.isChecked():
            pass
        elif self.btn_multi.isChecked():
            pass
        else:
            pass

# ==============================================================================================================
