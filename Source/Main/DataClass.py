from datetime import datetime

import pandas

# 클래스 이름 시작 단어 기준으로 구분
# Req : 클라이언트 → 서버
# Per : 서버 → 클라이언트

# ==================== 로그인

# 로그인 요청 : 아이디, 비밀번호
class ReqLogin:
    def __init__(self, id:str, pw:str):
        self.id = id
        self.password = pw

# 로그인 허가 응답 : 허가번호, 아이디
# rescode = 0 ("아이디 존재하지 않음")
# rescode = 1 ("비밀번호 존재하지 않음")
# rescode = 2 ("로그인 한 아이디")
# rescode = 3 ("로그인 허가 완료")
class PerLogin:
    def __init__(self, rescode: int, id: str, pw: str):
        self.rescode = rescode
        self.id = id
        self.pw = pw

# ==================== 로그아웃

# 로그아웃 요청 : 아이디, 시간
class ReqLoout:
    def __init__(self, id: str):
        self.id = id

# 로그아웃 허가 응답
class PerLogout:
    def __init__(self):
        pass

# ==================== 회원가입

# 회원가입 중복 아이디 체크 요청 : 아이디
class ReqDuplicateCheck:
    def __init__(self, id:str):
        self.id = id

# 아이디 중복 체크 응답 : True(중복), False(중복아님)
class PerDuplicateCheck:
    def __init__(self, isExisited: bool):
        self.isExisited = isExisited

# 회원가입 요청 : 아이디, 비밀번호, 닉네임, 이메일, 가입일자, 프로필 이미지경로, 상태메세지
class ReqMembership:
    def __init__(self, id: str, pw: str, nm: str, email: str, c_date: str, img: str):
        self.id = id
        self.pw = pw
        self.nm = nm
        self.email = email
        self.c_date = c_date
        self.img = img

# 회원가입 허가 응답
class PerRegist:
    def __init__(self, Success: bool):
        self.Success = Success

# 이메일 유효성 확인 및 전송 요청
class ReqEmailSend:
    def __init__(self, r_email: str):
        self.r_email = r_email

# 이메일 전송 응답
class PerEmailSend:
    def __init__(self, isSend: bool):
        self.isSend = isSend

# 이메일 인증번호 확인 요청
class ReqEmailNumber:
    def __init__(self, num1: str, num2: str):
        self.num1 = num1
        self.num2 = num2

# 이메일 인증번호 일치 여부 응답
class PerEmailNumber:
    def __init__(self, ismatch: bool):
        self.ismatch = ismatch




# ==================== 친구 초대

# 친구 초대 요청
class ReqSuggetsFriend:
    def __init__(self, user_id: str, frd_id: str, result=False):
        self.user_id = user_id
        self.frd_id = frd_id
        self.result = False

# 친구 수락 허가 응답
class PerAcceptFriend:
    def __init__(self, user_id: str, frd_id: str):
        self.user_id = user_id
        self.frd_id = frd_id
        self.result = False

# 친구 수락 요청
class ReqAcceptFriend:
    def __init__(self, user_id: str, frd_id: str):
        self.user_id = user_id
        self.frd_id = frd_id
        self.result = False

# ==================== 채팅방 개설

# 채팅방 요청
class JoinChat:
    def __init__(self, user_id: str, member: list, title:str):
        self.user_id = user_id
        self.member = member
        self.title = title

# 채팅방 나가기
class OutChat:
    def __init__(self, cr_id: str, user_id: str):
        self.cr_id = cr_id
        self.user_id = user_id

def get_data_tuple(t_class):
    data_dict = t_class.__dict__
    data_tuple = tuple(data_dict.values())
    return data_tuple

# ==================== 메시지 송신

# 채팅 송수신
class ReqChat:
    def __init__(self, cr_id:str, user_id:str, msg: str): #msg = self.edt_txt.text()
        self.cr_id = cr_id
        self.user_id = user_id
        self.msg = msg

class ReadChat:
    def __init__(self, cr_id:str):
        self.cr_id = cr_id
        self.msg:pandas.DataFrame