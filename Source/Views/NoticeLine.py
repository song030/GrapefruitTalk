from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSpacerItem
from PyQt5.QtCore import Qt

from Source.Views.Font import Font


class NoticeLine:
    def __init__(self, text:str):
        """
        :param t_nick: 유저 닉네임
        :param t_type: 입장 / 퇴장
        """
        self._layout = QHBoxLayout()

        # 안내 문구
        t_notice = text
        self._lbl_notice = QLabel()
        self._lbl_notice.setAlignment(Qt.AlignCenter)
        self._lbl_notice.setText(t_notice)
        self._lbl_notice.setFont(Font.text(3))
        self._lbl_notice.setStyleSheet("""border: None;
                                        background: rgba(248,228,208, 70);
                                        border-radius: 14px;
                                        padding: 8px 12px;""")

        self._layout.addStretch(1)
        self._layout.addWidget(self._lbl_notice)
        self._layout.addStretch(1)
        self._layout.setContentsMargins(0, 9, 0, 9)

    @property
    def layout(self):
        return self._layout
