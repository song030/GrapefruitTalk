from PyQt5.QtGui import QFont

class Font:
    @staticmethod
    def title(t_size=1):
        font = QFont()
        #
        if t_size == 1:
            font.setPointSize(50)
        elif t_size == 2:
            font.setPointSize(25)
        elif t_size == 3:
            font.setPointSize(15)
        elif t_size == 5:
            font.setPointSize(10)

        font.setFamily("나눔스퀘어라운드 ExtraBold")
        return font

    @staticmethod
    def button(t_size=1):
        font = QFont()
        if t_size == 1:
            font.setPointSize(12)
        elif t_size == 2:
            font.setPointSize(11)
        elif t_size == 3:
            font.setPointSize(10)
        elif t_size == 5:
            font.setPointSize(8)

        font.setFamily("나눔스퀘어라운드 ExtraBold")
        return font

    @staticmethod
    def text(t_size=1, t_blod=True):
        font = QFont()
        if t_size == 1:
            font.setPointSize(12)
        elif t_size == 2:
            font.setPointSize(11)
        elif t_size == 3:
            font.setPointSize(10)
        elif t_size == 4:
            font.setPointSize(9)

        if t_blod:
            font.setFamily("나눔스퀘어라운드 Bold")
        else:
            font.setFamily("나눔스퀘어라운드 Regular")

        return font
