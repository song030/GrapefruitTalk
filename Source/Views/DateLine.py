from datetime import datetime

from PyQt5.QtWidgets import QHBoxLayout, QFrame, QLabel
from PyQt5.QtCore import Qt

from Source.Views.Font import Font

class DateLine:
    def __init__(self, t_date:datetime):
        """
        :param t_date: 표시 일자
        """
        self._layout = QHBoxLayout()

        # 왼쪽 선
        self._line_left = QFrame()
        self._line_left.setFrameShadow(QFrame.Raised)
        self._line_left.setFrameShape(QFrame.HLine)
        self._line_left.setLineWidth(1)
        self._layout.addWidget(self._line_left)

        # 일자
        t_date = t_date.strftime("%Y-%m-%d")
        self._date = QLabel()
        self._date.setAlignment(Qt.AlignCenter)
        self._date.setText(t_date)
        self._date.setFont(Font.text(3))
        self._layout.addWidget(self._date)

        # 오른쪽 선
        self._line_right = QFrame()
        self._line_right.setFrameShadow(QFrame.Raised)
        self._line_right.setFrameShape(QFrame.HLine)
        self._line_right.setLineWidth(1)
        self._layout.addWidget(self._line_right)

        self._layout.setSpacing(10)
        self._layout.setStretch(0, 1)
        self._layout.setStretch(1, 0)
        self._layout.setStretch(2, 1)

    @property
    def layout(self):
        return self._layout
        

