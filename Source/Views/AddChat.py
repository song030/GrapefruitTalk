from PyQt5.QtWidgets import *
from Source.Views.ListItem import ListItem
from datetime import datetime
from Source.Views.Font import Font

class AddChat(QDialog):
    """친구 방 추가하는 부분"""
    def __init__(self):
        super().__init__()

        # --- 화면 설정
        self.set_style()

        # --- 화면 객체 생성 및 크기조정
        layout = QVBoxLayout(self) # vbox

        # 스크롤 영역
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        scroll_contents = QWidget()

        layout_2 = QVBoxLayout(scroll_contents)
        layout_1 = QVBoxLayout()
        layout_2.addLayout(layout_1)
        self.scroll_area.setWidget(scroll_contents)
        layout.addWidget(self.scroll_area)

        # --- 화면에 아이템 추가
        for i in range(50):
            item = ListItem("아이디", "닉네임", "이것은 상태창 상태창 상태창")
            layout_1.addWidget(item.frame)
            layout_1.addLayout(item.add_checkbox())

        # --- vbox에 추가
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout_1.addSpacerItem(spacer)
        # layout_2.addLayout(cnt_layout)

        # --- 라벨, 스페이서, 라벨이 들어간 horizonal 레이아웃 추가
        label1 = QLabel('선택한 명수: ')
        label1.setFont(Font.text(3))
        self.label2 = QLabel('0명')
        self.label2.setFont(Font.text(3))
        spacer2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        h_layout = QHBoxLayout()
        h_layout.addWidget(label1)
        h_layout.addItem(spacer2)
        h_layout.addWidget(self.label2)
        layout.addLayout(h_layout)

        # --- 버튼 추가
        add_btn = QPushButton('확인')
        add_btn.setFont(Font.text(4))
        add_btn.setMinimumSize(0, 50)
        add_btn.setStyleSheet("background-color:rgb(248,228,208);border-radius:25px")
        layout.addWidget(add_btn)

        # -- 메인 레이아웃에 추가
        self.setLayout(layout)

        # -- 체크박스 체크될 때마다 라벨 변하는 부분 추가
        self.checkboxes =  self.findChildren(QCheckBox)
        for checkbox in self.checkboxes:
            checkbox.clicked.connect(self.change_cnt_label)

    def change_cnt_label(self):
        """체크박스 누를 때마다 라벨 변하는 부분"""
        count = sum(checkbox.isChecked() for checkbox in self.checkboxes)
        self.label2.setText(f'{str(count)}명')

    def set_style(self):
        """화면 스타일시트 추가"""
        self.setStyleSheet('background-color: white')
        self.setFixedSize(420, 750)
        self.setWindowTitle("방 추가 화면")

if __name__ == '__main__':
    app = QApplication([])
    dialog = AddChat()
    dialog.show()
    app.exec_()
