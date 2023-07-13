from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSpacerItem
from PyQt5.QtCore import Qt

from Source.Views.Font import Font


class NoticeLine:
    def __init__(self, t_nick: str, t_type: str):
        """
        :param t_nick: 유저 닉네임
        :param t_type: 입장 / 퇴장
        """
        self._layout = QHBoxLayout()

        # 안내 문구
        t_notice = f"{t_nick}님이 {t_type}하셨습니다."
        self._lbl_notice = QLabel()
        self._lbl_notice.setAlignment(Qt.AlignCenter)
        self._lbl_notice.setText(t_notice)
        self._lbl_notice.setFont(Font.text(3))
        self._lbl_notice.setStyleSheet("""border: None;
                                        background: rgb(248,228,208);
                                        border-radius: 14px;
                                        padding: 8px 12px;""")

        self._layout.addStretch(1)
        self._layout.addWidget(self._lbl_notice)
        self._layout.addStretch(1)
        self._layout.setContentsMargins(0, 9, 0, 9)

    @property
    def layout(self):
        return self._layout
