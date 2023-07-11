from PyQt5.QtGui import QFont

class Font:
    @staticmethod
    def title(num=1):
        font = QFont()
        #
        if num == 1:
            font.setPointSize(50)
        elif num == 2:
            font.setPointSize(25)
        elif num == 3:
            font.setPointSize(15)
        elif num == 5:
            font.setPointSize(10)

        font.setFamily("나눔스퀘어라운드 ExtraBold")
        return font

    @staticmethod
    def button(num=1):
        font = QFont()
        if num == 1:
            font.setPointSize(12)
        elif num == 2:
            font.setPointSize(11)
        elif num == 3:
            font.setPointSize(10)
        elif num == 5:
            font.setPointSize(8)

        font.setFamily("나눔스퀘어라운드 ExtraBold")
        return font

    @staticmethod
    def text(num=1):
        font = QFont()
        if num == 1:
            font.setPointSize(12)
        elif num == 2:
            font.setPointSize(11)
        elif num == 3:
            font.setPointSize(10)
        font.setFamily("나눔스퀘어라운드 Bold")
        return font
