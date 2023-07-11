from datetime import datetime

from PyQt5.QtWidgets import QWidget, QListView, QLabel, QLayout
from PyQt5.QtGui import QResizeEvent

from Source.Views.UI_MainWidget import Ui_MainWidget

from Source.Views.Font import Font
from Source.Views.DialogWarning import DialogWarning
from Source.Views.TalkBox import TalkBox
from Source.Views.DateLine import DateLine

from Source.client import Client


class MainWidget(QWidget, Ui_MainWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 화면 초기화
        self.set_ui()

        # 변수 및 위젯 선언
        self.dlg_warning = DialogWarning()

        # 이벤트 연결
        self.connect_event()

        self.__chatroom = Client(self, 'soyeon')


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
        self.page_talk.showEvent = self.resizeEvent
        # self.splitter.moveSplitter(600,0)

    # 화면 변화가 일어났을때 대화창 사이즈 변화
    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.scrollAreaWidgetContents.setFixedWidth(self.scrollArea.width()-30)


    # 레이아웃 비우기
    def clear_layout(self, layout:QLayout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()

            if widget is not None:
                print("1",widget)
                widget.setParent(None)

            # 아이템이 레이아웃일 경우 재귀 호출로 레이아웃 내의 위젯 삭제
            else:
                print("2",widget)
                self.clear_layout(item.layout())

    # ================================================== 회원가입 ==================================================

    # 회원가입 입력확인
    def join_input_check(self):

        self.dlg_warning.set_dialog_type(2, "test")

        if self.dlg_warning.exec():
            self.stack_main.setCurrentWidget(self.page_talk)
            # self.init_talk()
        else:
            pass

    # ==============================================================================================================

    # ================================================== 대화 화면 ==================================================

    # 대화 방 생성

    # self.__chatroom = Client(self, 'soyeon')
    # def init_talk(self):
    #     self.add_date_line()
    #
    #     text = "말풍선선선선~~~~\n 말풍선!!\nzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
    #     for i in range(5):
    #         talkbox = TalkBox("", "자몽자몽", text, datetime.now())
    #         self.layout_talk.addLayout(talkbox.layout)
    #
    #     # self.clear_layout(self.layout_talk)
    #     # talkbox = TalkBox("", "자몽자몽", text, datetime.now())
    #     # self.layout_talk.addLayout(talkbox.layout)
    #
    # # 일자 표시선 추가
    # def add_date_line(self):
    #     talkbox = DateLine(datetime.now())
    #     self.layout_talk.addLayout(talkbox.layout)

    # ==============================================================================================================