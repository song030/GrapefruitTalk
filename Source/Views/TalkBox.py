from datetime import datetime

from PyQt5.QtWidgets import QGridLayout, QLabel, QPlainTextEdit
from PyQt5.QtGui import QPixmap, QPainterPath, QPainter
from PyQt5.QtCore import Qt, QRectF, QSizeF, QPoint

from Source.Views.Font import Font

class TalkBox:
    def __init__(self, t_img:str, t_nick:str, t_talk:str, t_time:datetime):
        """
        :param t_img: 프로필 타입 → 추 후 수정예정
        :param t_nick: 닉네임
        :param t_talk: 텍스트
        :param t_time: 발송 시간
        """

        self._grid_layout = QGridLayout()
        self._grid_layout.setAlignment(Qt.AlignLeft)
        self._grid_layout.setColumnStretch(0, 0)
        self._grid_layout.setColumnStretch(1, 2)
        self._grid_layout.setHorizontalSpacing(10)
        self._grid_layout.setVerticalSpacing(10)
        # 프로필 이미지
        self._lbl_profile = QLabel()
        self._lbl_profile.setFixedSize(50, 50)
        self._lbl_profile.setPixmap(QPixmap("../Images/img_profile_king.png"))
        self._lbl_profile.setStyleSheet("background-color:rgb(248,228,208);border-radius:25px")
        self._grid_layout.addWidget(self._lbl_profile, 0, 0, 2, 1, Qt.AlignTop)
        # 닉네임
        self._lbl_nick = QLabel()
        self._lbl_nick.setText(f"[ {t_nick} ]")
        self._lbl_nick.setFont(Font.button(3))
        self._grid_layout.addWidget(self._lbl_nick, 0, 1)
        # 말풍선
        self._lbl_talk = QPlainTextEdit()
        self._lbl_talk.setReadOnly(True) # readonly로 설정
        self._lbl_talk.setFont(Font.text(3))
        self._lbl_talk.setStyleSheet("""background-color:rgb(248,228,208);
                                    border:1px solid rgb(248,228,208);
                                    border-radius:5px;
                                    padding:10px;""")
        self._lbl_talk.setPlainText(t_talk)
        self._lbl_talk.setReadOnly(True)
        self._grid_layout.addWidget(self._lbl_talk, 1, 1)
        # 발송 시간
        t_time = t_time.strftime("%H:%M")
        self._lbl_time = QLabel()
        self._lbl_time.setFont(Font.text(3))
        self._lbl_time.setText(t_time)
        self._grid_layout.addWidget(self._lbl_time, 2, 1)

    @property
    def layout(self):
        return self._grid_layout