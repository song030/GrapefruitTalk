from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap


class ProfileImage:
    def __init__(self, t_type=0):
        self._lbl_img = QLabel()
        self._lbl_img.setFixedSize(50, 50)
        self._lbl_img.setPixmap(QPixmap("../Images/img_profile_king.png"))
        self._lbl_img.setStyleSheet("background-color:rgb(248,228,208);border-radius:25px")

    @property
    def image(self):
        return self._lbl_img
