import sys

from PyQt5.QtWidgets import QDialog, QApplication, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from Source.Views.Font import Font
from Source.Views.UI_DialogSetting import Ui_DialogSetting


class DialogSetting(QDialog, Ui_DialogSetting):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.setWindowFlags(Qt.FramelessWindowHint)

        self.btn_profile.setFont(Font.button(2))
        self.btn_notice.setFont(Font.button(2))
        self.btn_logout.setFont(Font.button(2))

        self.connect_event()

    # 예, 확인 눌렀을 때
    def accept(self) -> None:
        self.setResult(1)
        self.close()

    def reject(self) -> None:
        self.setResult(0)
        self.close()

    # 이벤트 연결
    def connect_event(self):
        self.btn_close_1.clicked.connect(self.close)
        self.btn_close_2.clicked.connect(self.close)

        self.btn_profile.clicked.connect(lambda: self.stack_setting.setCurrentWidget(self.page_profile))
        self.btn_img_edit.clicked.connect(lambda: self.stack_setting.setCurrentWidget(self.page_img_choice))

        self.btn_back_1.clicked.connect(lambda x, y=1: self.back_page(y))
        self.btn_back_2.clicked.connect(lambda x, y=2: self.back_page(y))

        self.btn_notice.clicked.connect(self.notice_on_off)
        self.btn_choice.clicked.connect(self.change_profile_image)

    # 이전 페이지 이동
    def back_page(self, b):
        if b == 1:
            self.stack_setting.setCurrentWidget(self.page_setting)
        elif b == 2:
            self.stack_setting.setCurrentWidget(self.page_profile)

    # 메시지 설정 버튼 클릭 시 텍스트 변경
    def notice_on_off(self):
        if self.btn_notice.isChecked():
            self.btn_notice.setText("메시지 알림 ON")
        else:
            self.btn_notice.setText("메시지 알림 OFF")

    # 메시지 설정 반환
    @property
    def notice_setting(self):
        """1 = ON / 0 = OFF"""
        ret = 1
        if not self.btn_notice.isChecked():
            ret = 0
        return ret

    # 외부 로그아웃 이벤트와 연결
    def set_logout_event(self, f_):
        """
        f_ : 로그아웃 시 발생할 이벤트 함수
        """
        self.btn_logout.clicked.connect(f_)

    def change_profile_image(self):
        for btn in self.btn_bundle.findChildren(QPushButton):
            if btn.isChecked():
                self.ret = btn.objectName()
                self.lbl_img_profile.setPixmap(QPixmap(f"../../Images/{self.ret}.png"))
                break

        self.stack_setting.setCurrentWidget(self.page_profile)

    # 유저 프로필 적용
    def set_profile_page(self, nick_, img_, state_):
        self.ret = None
        self.stack_setting.setCurrentWidget(self.page_setting)
        self.lbl_img_profile.setPixmap(QPixmap(f"../../Images/img_profile_{img_}.png"))
        self.lineEdit_nickname.setText(nick_)
        self.lineEdit_state.setText(state_)

    # 프로필 변경 사항 전달
    def return_profile_data(self):
        if self.ret is None:
            return

        img_ = self.ret[12:]
        nick_ = self.lineEdit_nickname.text()
        state_ = self.lineEdit_state.text()

        return nick_, img_, state_


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DialogSetting()
    ex.show()
    app.exec()
