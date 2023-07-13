from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt

from Source.Views.UI_DialogWarning import Ui_DlgWarning

class DialogWarning(QDialog, Ui_DlgWarning):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowFlags(Qt.FramelessWindowHint)

        self.connect_event()

    # 아니오, 닫기 눌렀을 때
    def reject(self) -> None:
        self.setResult(0)
        self.close()

    # 예, 확인 눌렀을 때
    def accept(self) -> None:
        self.setResult(1)
        self.close()

    # 이벤트 연결
    def connect_event(self):
        # 예, 확인 : accept (1)
        # 아니오, 닫기 : reject (0)
        self.btn_single.clicked.connect(self.accept)
        self.btn_yes.clicked.connect(self.accept)
        self.btn_close.clicked.connect(self.reject)
        self.btn_no.clicked.connect(self.reject)

    # 다이얼로그 타입 설정
    # bt_cnt : 버튼 수량
    # t_type : 다이얼로그 타입
    def set_dialog_type(self, bt_cnt: int, t_type: str):
        if bt_cnt == 1:
            self.layout_double.setVisible(False)
            self.btn_single.setVisible(True)

        elif bt_cnt == 2:
            self.layout_double.setVisible(True)
            self.btn_single.setVisible(False)

        if t_type == 'used_id':
            self.lbl_text.setText('사용 중인 아이디입니다.')
        elif t_type == 'user_can_used':
            self.lbl_text.setText('사용할 수 있는 아이디입니다.')
        elif t_type == 'id_len_limited':
            self.lbl_text.setText('아이디는 최대 16자까지 입력 가능합니다.')
        elif t_type == 'pw_alphabet_1':
            self.lbl_text.setText('비밀번호에 최소 영대문자 1글자 이상 포함되어야 합니다.')
        elif t_type == 'pw_unique_word':
            self.lbl_text.setText('비밀번호에 최소 특수문자 1글자 이상 포함되어야 합니다.')
        elif t_type == 'pw_len_limited':
            self.lbl_text.setText('비밀번호는 최대 16자까지 입력가능합니다.')
        elif t_type == 'pw_input':
            self.lbl_text.setText('비밀번호를 입력해주세요')
        elif t_type == 'pw_not_match':
            self.lbl_text.setText('비밀번호가 서로 일치하지 않습니다.')
        elif t_type == 'nick_name_len_limit':
            self.lbl_text.setText('닉네임은 최대 20자까지 가능합니다.')
        elif t_type == 'vaild_email_addr':
            self.lbl_text.setText('유효한 이메일 주소 입니다.')
        elif t_type == 'not_vaild_email_addr':
            self.lbl_text.setText('유효한 이메일 주소가 아닙니다.')
        elif t_type == 'email_send':
            self.lbl_text.setText('가입을 위한 인증번호 이메일이 발송되었습니다.')
        elif t_type == 'email_check':
            self.lbl_text.setText('이메일 인증 완료')
        elif t_type == 'email_not_check':
            self.lbl_text.setText('이메일 인증 실패, 확인 후 재입력 해주시기 바랍니다.')
        elif t_type == 'exit_chat_room':
            self.lbl_text.setText('대화 내용이 모두 삭제됩니다.\n정말 채팅방을 나가시겠습니까?')
