# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './UI/MainWidget.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWidget(object):
    def setupUi(self, MainWidget):
        MainWidget.setObjectName("MainWidget")
        MainWidget.setWindowModality(QtCore.Qt.ApplicationModal)
        MainWidget.resize(1024, 860)
        MainWidget.setStyleSheet("background-color:white;")
        self.verticalLayout = QtWidgets.QVBoxLayout(MainWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.stack_main = QtWidgets.QStackedWidget(MainWidget)
        self.stack_main.setObjectName("stack_main")
        self.page_login = QtWidgets.QWidget()
        self.page_login.setObjectName("page_login")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.page_login)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(322, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(10)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.lbl_main_title = QtWidgets.QLabel(self.page_login)
        font = QtGui.QFont()
        font.setPointSize(43)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_main_title.setFont(font)
        self.lbl_main_title.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_main_title.setObjectName("lbl_main_title")
        self.verticalLayout_3.addWidget(self.lbl_main_title)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.lbl_main_name = QtWidgets.QLabel(self.page_login)
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_main_name.setFont(font)
        self.lbl_main_name.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_main_name.setObjectName("lbl_main_name")
        self.verticalLayout_3.addWidget(self.lbl_main_name)
        self.lbl_main_team = QtWidgets.QLabel(self.page_login)
        self.lbl_main_team.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_main_team.setObjectName("lbl_main_team")
        self.verticalLayout_3.addWidget(self.lbl_main_team)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem3)
        self.edt_login_id = QtWidgets.QLineEdit(self.page_login)
        self.edt_login_id.setMinimumSize(QtCore.QSize(0, 30))
        self.edt_login_id.setStyleSheet("background-color:white;\n"
"border:1px solid lightgray;\n"
"border-radius:5px;\n"
"padding:5px;")
        self.edt_login_id.setInputMask("")
        self.edt_login_id.setObjectName("edt_login_id")
        self.verticalLayout_3.addWidget(self.edt_login_id)
        self.edt_login_pwd = QtWidgets.QLineEdit(self.page_login)
        self.edt_login_pwd.setMinimumSize(QtCore.QSize(0, 30))
        self.edt_login_pwd.setStyleSheet("background-color:white;\n"
"border:1px solid lightgray;\n"
"border-radius:5px;\n"
"padding:5px;")
        self.edt_login_pwd.setText("")
        self.edt_login_pwd.setObjectName("edt_login_pwd")
        self.verticalLayout_3.addWidget(self.edt_login_pwd)
        self.btn_login = QtWidgets.QPushButton(self.page_login)
        self.btn_login.setMinimumSize(QtCore.QSize(0, 30))
        self.btn_login.setStyleSheet("QPushButton{\n"
"background-color:white;\n"
"border:1px solid lightgray;\n"
"border-radius:5px;\n"
"}")
        self.btn_login.setObjectName("btn_login")
        self.verticalLayout_3.addWidget(self.btn_login)
        spacerItem4 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem4)
        self.lbl_join = QtWidgets.QLabel(self.page_login)
        self.lbl_join.setMinimumSize(QtCore.QSize(20, 0))
        self.lbl_join.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lbl_join.setObjectName("lbl_join")
        self.verticalLayout_3.addWidget(self.lbl_join, 0, QtCore.Qt.AlignHCenter)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem5)
        self.verticalLayout_3.setStretch(0, 2)
        self.verticalLayout_3.setStretch(5, 1)
        self.verticalLayout_3.setStretch(11, 2)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        spacerItem6 = QtWidgets.QSpacerItem(322, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem6)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(2, 1)
        self.stack_main.addWidget(self.page_login)
        self.page_join = QtWidgets.QWidget()
        self.page_join.setObjectName("page_join")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.page_join)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem7 = QtWidgets.QSpacerItem(277, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem7)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem8)
        self.lbl_join_title = QtWidgets.QLabel(self.page_join)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_join_title.setFont(font)
        self.lbl_join_title.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_join_title.setObjectName("lbl_join_title")
        self.verticalLayout_2.addWidget(self.lbl_join_title)
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem9)
        self.frame = QtWidgets.QFrame(self.page_join)
        self.frame.setStyleSheet("border:1px solid lightgray;\n"
"border-radius:5px;")
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setLineWidth(5)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(15, 15, 15, 15)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(10)
        self.gridLayout.setObjectName("gridLayout")
        self.edt_join_nick = QtWidgets.QLineEdit(self.frame)
        self.edt_join_nick.setMinimumSize(QtCore.QSize(280, 30))
        self.edt_join_nick.setStyleSheet("border:1px solid lightgray;\n"
"border-radius:5px;\n"
"padding:5px;")
        self.edt_join_nick.setObjectName("edt_join_nick")
        self.gridLayout.addWidget(self.edt_join_nick, 4, 0, 1, 3)
        self.lbl_join_dot = QtWidgets.QLabel(self.frame)
        self.lbl_join_dot.setStyleSheet("border:solid;")
        self.lbl_join_dot.setObjectName("lbl_join_dot")
        self.gridLayout.addWidget(self.lbl_join_dot, 3, 1, 1, 1)
        self.btn_join_id = QtWidgets.QPushButton(self.frame)
        self.btn_join_id.setMinimumSize(QtCore.QSize(90, 30))
        self.btn_join_id.setStyleSheet("QPushButton{\n"
"background-color:white;\n"
"border:1px solid lightgray;\n"
"border-radius:5px;\n"
"}")
        self.btn_join_id.setObjectName("btn_join_id")
        self.gridLayout.addWidget(self.btn_join_id, 0, 3, 1, 1)
        self.edt_join_id = QtWidgets.QLineEdit(self.frame)
        self.edt_join_id.setMinimumSize(QtCore.QSize(280, 30))
        self.edt_join_id.setStyleSheet("border:1px solid lightgray;\n"
"border-radius:5px;\n"
"padding:5px;")
        self.edt_join_id.setObjectName("edt_join_id")
        self.gridLayout.addWidget(self.edt_join_id, 0, 0, 1, 3)
        self.edt_join_pwd1 = QtWidgets.QLineEdit(self.frame)
        self.edt_join_pwd1.setMinimumSize(QtCore.QSize(280, 30))
        self.edt_join_pwd1.setStyleSheet("border:1px solid lightgray;\n"
"border-radius:5px;\n"
"padding:5px;")
        self.edt_join_pwd1.setObjectName("edt_join_pwd1")
        self.gridLayout.addWidget(self.edt_join_pwd1, 1, 0, 1, 3)
        self.cb_join_email = QtWidgets.QComboBox(self.frame)
        self.cb_join_email.setMinimumSize(QtCore.QSize(0, 30))
        self.cb_join_email.setStyleSheet("QComboBox{\n"
"background-color:white;\n"
"border-radius:5px;\n"
"border:1px solid lightgray;\n"
"padding:5px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"background-color:white;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item {\n"
"min-height:20px;\n"
"margin:5px;\n"
"}\n"
"")
        self.cb_join_email.setObjectName("cb_join_email")
        self.gridLayout.addWidget(self.cb_join_email, 3, 2, 1, 1)
        self.edt_join_email = QtWidgets.QLineEdit(self.frame)
        self.edt_join_email.setMinimumSize(QtCore.QSize(0, 30))
        self.edt_join_email.setStyleSheet("border:1px solid lightgray;\n"
"border-radius:5px;\n"
"padding:5px;")
        self.edt_join_email.setObjectName("edt_join_email")
        self.gridLayout.addWidget(self.edt_join_email, 3, 0, 1, 1)
        self.edt_join_pwd2 = QtWidgets.QLineEdit(self.frame)
        self.edt_join_pwd2.setMinimumSize(QtCore.QSize(280, 30))
        self.edt_join_pwd2.setStyleSheet("border:1px solid lightgray;\n"
"border-radius:5px;\n"
"padding:5px;")
        self.edt_join_pwd2.setObjectName("edt_join_pwd2")
        self.gridLayout.addWidget(self.edt_join_pwd2, 2, 0, 1, 3)
        self.btn_join_mail = QtWidgets.QPushButton(self.frame)
        self.btn_join_mail.setMinimumSize(QtCore.QSize(90, 30))
        self.btn_join_mail.setStyleSheet("QPushButton{\n"
"background-color:white;\n"
"border:1px solid lightgray;\n"
"border-radius:5px;\n"
"}")
        self.btn_join_mail.setObjectName("btn_join_mail")
        self.gridLayout.addWidget(self.btn_join_mail, 3, 3, 1, 1)
        self.gridLayout.setColumnStretch(0, 2)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.verticalLayout_2.addWidget(self.frame)
        spacerItem10 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem10)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem11)
        self.btn_join = QtWidgets.QPushButton(self.page_join)
        self.btn_join.setMinimumSize(QtCore.QSize(100, 30))
        self.btn_join.setStyleSheet("QPushButton{\n"
"background-color:white;\n"
"border:1px solid lightgray;\n"
"border-radius:5px;\n"
"}")
        self.btn_join.setObjectName("btn_join")
        self.horizontalLayout_3.addWidget(self.btn_join)
        self.btn_join_cancel = QtWidgets.QPushButton(self.page_join)
        self.btn_join_cancel.setMinimumSize(QtCore.QSize(100, 30))
        self.btn_join_cancel.setStyleSheet("QPushButton{\n"
"background-color:white;\n"
"border:1px solid lightgray;\n"
"border-radius:5px;\n"
"}")
        self.btn_join_cancel.setObjectName("btn_join_cancel")
        self.horizontalLayout_3.addWidget(self.btn_join_cancel)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem12)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(3, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        spacerItem13 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem13)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(6, 2)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        spacerItem14 = QtWidgets.QSpacerItem(277, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem14)
        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(2, 1)
        self.stack_main.addWidget(self.page_join)
        self.page_talk = QtWidgets.QWidget()
        self.page_talk.setObjectName("page_talk")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.page_talk)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frame_2 = QtWidgets.QFrame(self.page_talk)
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.lbl_room_name = QtWidgets.QLabel(self.frame_2)
        self.lbl_room_name.setObjectName("lbl_room_name")
        self.horizontalLayout_5.addWidget(self.lbl_room_name)
        spacerItem15 = QtWidgets.QSpacerItem(779, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem15)
        self.btn_single = QtWidgets.QPushButton(self.frame_2)
        self.btn_single.setStyleSheet("border: 1px solid lightgray;\n"
"border-radius: 5px;\n"
"padding: 3px;")
        self.btn_single.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../Images/btn_single.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_single.setIcon(icon)
        self.btn_single.setIconSize(QtCore.QSize(22, 22))
        self.btn_single.setFlat(True)
        self.btn_single.setObjectName("btn_single")
        self.horizontalLayout_5.addWidget(self.btn_single)
        self.btn_multi = QtWidgets.QPushButton(self.frame_2)
        self.btn_multi.setStyleSheet("border: 1px solid lightgray;\n"
"border-radius: 5px;\n"
"padding: 3px;")
        self.btn_multi.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../Images/btn_multi.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_multi.setIcon(icon1)
        self.btn_multi.setIconSize(QtCore.QSize(22, 22))
        self.btn_multi.setFlat(True)
        self.btn_multi.setObjectName("btn_multi")
        self.horizontalLayout_5.addWidget(self.btn_multi)
        self.btn_menu = QtWidgets.QPushButton(self.frame_2)
        self.btn_menu.setStyleSheet("border: 1px solid lightgray;\n"
"border-radius: 5px;\n"
"padding: 3px;")
        self.btn_menu.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../Images/btn_menu.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_menu.setIcon(icon2)
        self.btn_menu.setIconSize(QtCore.QSize(22, 22))
        self.btn_menu.setFlat(True)
        self.btn_menu.setObjectName("btn_menu")
        self.horizontalLayout_5.addWidget(self.btn_menu)
        self.verticalLayout_4.addWidget(self.frame_2)
        self.splitter = QtWidgets.QSplitter(self.page_talk)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.frame_4 = QtWidgets.QFrame(self.splitter)
        self.frame_4.setStyleSheet("")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.scrollArea = QtWidgets.QScrollArea(self.frame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setStyleSheet("QScrollArea {\n"
"    border: None;\n"
"    background-color:rgba(100, 100, 100, 100);\n"
"}\n"
"\n"
"QScrollBar:vertical{\n"
"    border: None;\n"
"    background-color: white;\n"
"    width:18px;\n"
"    margin: 0 0 0 0;\n"
"    border-radius: 0px;\n"
"}\n"
"\n"
"/* 핸들러 바 */\n"
"QScrollBar::handle:vertical {\n"
"    background-color: white;\n"
"    min-width: 30px;\n"
"    border: 2px solid rgb(242,234,232);\n"
"    border-radius:8px;\n"
"\n"
"}\n"
"QScrollBar::sub-line:vertical {\n"
"    border: None;\n"
"    background-color: white;\n"
"    width:18px;\n"
"    margin: 0 0 0 0;\n"
"    border-radius: 0px;\n"
"}")
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 948, 736))
        self.scrollAreaWidgetContents.setStyleSheet("")
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_6.setContentsMargins(15, 15, 15, 15)
        self.verticalLayout_6.setSpacing(10)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.layout_talk = QtWidgets.QVBoxLayout()
        self.layout_talk.setSpacing(20)
        self.layout_talk.setObjectName("layout_talk")
        self.verticalLayout_6.addLayout(self.layout_talk)
        spacerItem16 = QtWidgets.QSpacerItem(20, 685, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem16)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_7.addWidget(self.scrollArea)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.edt_txt = QtWidgets.QLineEdit(self.frame_4)
        self.edt_txt.setMinimumSize(QtCore.QSize(0, 30))
        self.edt_txt.setStyleSheet("border:1px solid lightgray;\n"
"border-radius:5px;\n"
"padding:5px;")
        self.edt_txt.setObjectName("edt_txt")
        self.horizontalLayout_6.addWidget(self.edt_txt)
        self.btn_emoticon = QtWidgets.QPushButton(self.frame_4)
        self.btn_emoticon.setMinimumSize(QtCore.QSize(0, 30))
        self.btn_emoticon.setStyleSheet("border: 1px solid lightgray;\n"
"border-radius: 5px;\n"
"padding: 3px;")
        self.btn_emoticon.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../Images/btn_emoticon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_emoticon.setIcon(icon3)
        self.btn_emoticon.setIconSize(QtCore.QSize(22, 22))
        self.btn_emoticon.setFlat(True)
        self.btn_emoticon.setObjectName("btn_emoticon")
        self.horizontalLayout_6.addWidget(self.btn_emoticon)
        self.btn_send = QtWidgets.QPushButton(self.frame_4)
        self.btn_send.setMinimumSize(QtCore.QSize(0, 30))
        self.btn_send.setStyleSheet("border: 1px solid lightgray;\n"
"border-radius: 5px;\n"
"padding: 3px;")
        self.btn_send.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("../Images/btn_send.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_send.setIcon(icon4)
        self.btn_send.setIconSize(QtCore.QSize(22, 22))
        self.btn_send.setFlat(True)
        self.btn_send.setObjectName("btn_send")
        self.horizontalLayout_6.addWidget(self.btn_send)
        self.verticalLayout_7.addLayout(self.horizontalLayout_6)
        self.stack_menu = QtWidgets.QStackedWidget(self.splitter)
        self.stack_menu.setObjectName("stack_menu")
        self.page_single = QtWidgets.QWidget()
        self.page_single.setObjectName("page_single")
        self.stack_menu.addWidget(self.page_single)
        self.page_multi = QtWidgets.QWidget()
        self.page_multi.setObjectName("page_multi")
        self.stack_menu.addWidget(self.page_multi)
        self.page_setting = QtWidgets.QWidget()
        self.page_setting.setObjectName("page_setting")
        self.stack_menu.addWidget(self.page_setting)
        self.verticalLayout_4.addWidget(self.splitter)
        self.verticalLayout_4.setStretch(1, 1)
        self.stack_main.addWidget(self.page_talk)
        self.verticalLayout.addWidget(self.stack_main)

        self.retranslateUi(MainWidget)
        self.stack_main.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWidget)

    def retranslateUi(self, MainWidget):
        _translate = QtCore.QCoreApplication.translate
        MainWidget.setWindowTitle(_translate("MainWidget", "GraperfruitTalk"))
        self.lbl_main_title.setText(_translate("MainWidget", "G.G.G"))
        self.lbl_main_name.setText(_translate("MainWidget", "Graperfruit Talk"))
        self.lbl_main_team.setText(_translate("MainWidget", "- Girl\'s Generation -"))
        self.edt_login_id.setPlaceholderText(_translate("MainWidget", "아이디"))
        self.edt_login_pwd.setPlaceholderText(_translate("MainWidget", "비밀번호"))
        self.btn_login.setText(_translate("MainWidget", "로그인"))
        self.lbl_join.setText(_translate("MainWidget", "회원가입"))
        self.lbl_join_title.setText(_translate("MainWidget", "회원가입"))
        self.edt_join_nick.setPlaceholderText(_translate("MainWidget", "닉네임 (최대20자)"))
        self.lbl_join_dot.setText(_translate("MainWidget", "@"))
        self.btn_join_id.setText(_translate("MainWidget", "중복확인"))
        self.edt_join_id.setPlaceholderText(_translate("MainWidget", "아이디"))
        self.edt_join_pwd1.setPlaceholderText(_translate("MainWidget", "비밀번호 (영대문자,숫자,특수문자 필수,5~16자)"))
        self.edt_join_email.setPlaceholderText(_translate("MainWidget", "이메일"))
        self.edt_join_pwd2.setPlaceholderText(_translate("MainWidget", "비밀번호 확인"))
        self.btn_join_mail.setText(_translate("MainWidget", "인증 메일 발송"))
        self.btn_join.setText(_translate("MainWidget", "회원가입"))
        self.btn_join_cancel.setText(_translate("MainWidget", "취소"))
        self.lbl_room_name.setText(_translate("MainWidget", "방이름"))
