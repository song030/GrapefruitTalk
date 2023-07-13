from datetime import datetime

from PyQt5.QtWidgets import QGridLayout, QLabel, QCheckBox
from PyQt5.QtCore import Qt

from Source.Views.Font import Font
from Source.Views.ProfileImage import ProfileImage
from Source.Views.NoMsgCnt import NoMsgCnt

class ListItem:
    def __init__(self, t_name:str, t_text:str, t_img_type=0):
        """
        :param t_name: 닉네임 또는 방이름
        :param t_text: 상태메시지 또는 마지막 메시지
        :param t_img_type: 프로필 이미지 타입 (기본 방장:0)
        """

        self._grid_layout = QGridLayout()
        self._grid_layout.setAlignment(Qt.AlignLeft)
        self._grid_layout.setColumnStretch(0, 0)
        self._grid_layout.setColumnStretch(1, 1)
        self._grid_layout.setColumnStretch(2, 0)
        self._grid_layout.setColumnStretch(3, 0)
        self._grid_layout.setHorizontalSpacing(10)
        self._grid_layout.setVerticalSpacing(10)

        # 프로필 이미지
        self._lbl_profile = ProfileImage()
        self._grid_layout.addWidget(self._lbl_profile.image, 0, 0, 2, 1, Qt.AlignTop)

        # 닉네임
        self._lbl_nick = QLabel()
        self._lbl_nick.setText(f"[ {t_name} ]")
        self._lbl_nick.setFont(Font.text(3))
        self._grid_layout.addWidget(self._lbl_nick, 0, 1, Qt.AlignVCenter)

        # 상태메시지 또는 마지막 메시지
        self._lbl_text = QLabel()
        self._lbl_text.setText(f"{t_text}")
        self._lbl_text.setFont(Font.text(4, False))
        self._grid_layout.addWidget(self._lbl_text, 1, 1, 1, 2, Qt.AlignVCenter)

        # 채팅방 인원
        self._lbl_cnt = QLabel()
        self._lbl_cnt.setFont(Font.text(4))
        self._lbl_cnt.setFixedWidth(30)
        self._lbl_cnt.setAlignment(Qt.AlignCenter)
        self._grid_layout.addWidget(self._lbl_cnt, 0, 2, Qt.AlignCenter)

        # 발송 시간
        self._lbl_last_date = QLabel()
        self._lbl_last_date.setFont(Font.text(4, False))
        self._grid_layout.addWidget(self._lbl_last_date, 0, 3, Qt.AlignVCenter)

        # 미확인 메시지 수
        self._lbl_no_check= NoMsgCnt()
        self._grid_layout.addWidget(self._lbl_no_check.label, 1, 3, 1, 1, Qt.AlignCenter)

        # 방 생성 체크박스
        # self._check_box = QCheckBox()
        # self._grid_layout.addWidget(self._check_box, 1, 4, 1, 1, Qt.AlignCenter)


    @property
    def layout(self):
        return self._grid_layout

    def set_info(self, t_last:datetime, t_no_check:int):
        t_last = t_last.strftime("%H:%M")
        self._lbl_last_date.setText(t_last)
        self._lbl_no_check.set_count(t_no_check)

    def set_member_count(self, t_cnt:int):
        self._lbl_cnt.setText(f"{t_cnt}명")

    def add_checkbox(self):
        """체크박스 위해 추가했습니다."""
        check_box = QCheckBox()
        self._grid_layout.addWidget(check_box, 1, 4, 1, 1, Qt.AlignCenter)