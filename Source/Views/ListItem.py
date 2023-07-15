from datetime import datetime

from PyQt5.QtWidgets import QGridLayout, QLabel, QWidget, QCheckBox, QPushButton, QAction, QHBoxLayout
from PyQt5.QtCore import Qt

from Source.Views.Font import Font
from Source.Views.ProfileImage import ProfileImage
from Source.Views.NoMsgCnt import NoMsgCnt


class ListItem:
    def __init__(self, t_id: str, t_name: str, t_text: str, t_img_type=0):
        """
        :param t_name: 닉네임 또는 방이름
        :param t_text: 상태메시지 또는 마지막 메시지
        :param t_img_type: 프로필 이미지 타입 (기본 방장:0)
        """

        _grid_layout = QGridLayout()
        _grid_layout.setAlignment(Qt.AlignLeft)
        _grid_layout.setColumnStretch(0, 0)
        _grid_layout.setColumnStretch(1, 1)
        _grid_layout.setColumnStretch(2, 0)
        _grid_layout.setColumnStretch(3, 0)
        _grid_layout.setHorizontalSpacing(10)
        _grid_layout.setVerticalSpacing(10)
        _grid_layout.setContentsMargins(0, 0, 0, 0)

        # 프로필 이미지
        self._lbl_profile = ProfileImage(t_img_type)
        _grid_layout.addWidget(self._lbl_profile.image, 0, 0, 2, 1, Qt.AlignTop)

        # 닉네임
        self._lbl_nick = QLabel()
        self._lbl_nick.setObjectName(t_id)
        self._lbl_nick.setText(f"[ {t_name} ]")
        self._lbl_nick.setFont(Font.text(3))
        _grid_layout.addWidget(self._lbl_nick, 0, 1, Qt.AlignVCenter)

        # 상태메시지 또는 마지막 메시지
        self._lbl_text = QLabel()
        self._lbl_text.setText(f"{t_text}")
        self._lbl_text.setFont(Font.text(4, False))
        _grid_layout.addWidget(self._lbl_text, 1, 1, 1, 2, Qt.AlignVCenter)

        # 채팅방 인원
        self._lbl_cnt = QLabel()
        self._lbl_cnt.setFont(Font.text(4))
        self._lbl_cnt.setFixedWidth(30)
        self._lbl_cnt.setAlignment(Qt.AlignCenter)
        _grid_layout.addWidget(self._lbl_cnt, 0, 2, Qt.AlignCenter)

        # 발송 시간
        self._lbl_last_date = QLabel()
        self._lbl_last_date.setFont(Font.text(4, False))
        _grid_layout.addWidget(self._lbl_last_date, 0, 3, Qt.AlignVCenter)

        # 미확인 메시지 수
        self._lbl_no_check = NoMsgCnt()
        _grid_layout.addWidget(self._lbl_no_check.label, 1, 3, 1, 1, Qt.AlignCenter)

        self._frame = QWidget()
        self._frame.setLayout(_grid_layout)

    @property
    def item_id(self):
        return self._lbl_nick.objectName()

    @item_id.setter
    def item_id(self, t_id):
        if isinstance(t_id, str):
            self._lbl_nick.setObjectName(t_id)
        else:
            raise "Type Error: item_id only string."

    @property
    def item_nm(self):
        nm_ = self._lbl_nick.text()
        # nm_ = nm_.lstrip("[ ")
        # nm_ = nm_.rstrip(" ]")
        return nm_

    @property
    def member_cnt(self):
        return self._lbl_cnt.text()

    @member_cnt.setter
    def member_cnt(self, t_cnt: int):
        self._lbl_cnt.setText(f"{t_cnt}명")

    @property
    def no_msg_cnt(self):
        return self._lbl_no_check.label.text()

    @no_msg_cnt.setter
    def no_msg_cnt(self, t_cnt):
        if isinstance(t_cnt, int):
            self._lbl_no_check.set_count(t_cnt)
        else:
            raise "Type Error: no_cnt only int."

    @property
    def layout(self):
        return self.frame.layout()

    @property
    def frame(self):
        return self._frame

    @property
    def item_state(self):
        return self._lbl_text.text()

    # 방장 라벨 추가
    def set_host(self):
        self._lbl_profile.crown()

    def set_info(self, t_last:datetime, t_no_check:int):
        t_last = t_last.strftime("%H:%M")
        self._lbl_last_date.setText(t_last)
        self._lbl_no_check.set_count(t_no_check)

    def set_button_box(self, t_func):
        # 수락/거절 버튼
        _btn_yes = QPushButton()
        _btn_yes.setText("수락")
        _btn_yes.setFont(Font.text(3))
        _btn_yes.clicked.connect(lambda _: t_func(1, self.item_id))

        _btn_no = QPushButton()
        _btn_no.setText("거절")
        _btn_no.setFont(Font.text(3))
        _btn_no.clicked.connect(lambda _: t_func(0, self.item_id))

        _box_layout = QHBoxLayout()
        _box_layout.addWidget(_btn_yes)
        _box_layout.addWidget(_btn_no)
        _layout: QGridLayout = self._frame.layout()
        _layout.addLayout(_box_layout, 1, 2, 1, 2, Qt.AlignVCenter)

        self._frame.setStyleSheet("QPushButton {"
                                  "border: None;"
                                  "background: rgb(248,228,208);"
                                  "padding: 6px 8px;"
                                  "border-radius: 6px;"
                                  "}")

    def set_context_menu(self, t_act_nm: str, t_func, t_para=None):
        """
        :param t_act_nm: 메뉴 이름
        :param t_func: 메뉴 함수
        :param t_para: 함수에 파라미터가 필요한 경우
        """
        self._frame.setContextMenuPolicy(Qt.ActionsContextMenu)
        context_action = QAction(f"{t_act_nm}", self._frame)
        if t_para:
            context_action.triggered.connect(lambda: t_func(t_para))
        else:
            context_action.triggered.connect(t_func)
        self._frame.addAction(context_action)
        self._frame.setStyleSheet("QMenu::item::selected{color: rgb(248,228,208);}")

    def add_checkbox(self):
        """체크박스 위해 추가했습니다."""
        check_box = QCheckBox()
        _layout: QGridLayout = self._frame.layout()
        _layout.addWidget(check_box, 1, 4, 1, 1, Qt.AlignCenter)
