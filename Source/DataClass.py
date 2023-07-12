#############클라이언트 -> 서버#############

# 회원가입 중복 아이디 체크 요청 : 아이디
class ReqDuplicateCheck:
    def __init__(self, id:str):
        self.id = id

# 회원가입 요청 : 아이디, 비밀번호, 닉네임, 이메일, 가입일자, 프로필 이미지경로, 상태메세지
class ReqMembership:
    def __init__(self, id: str, pw: str, nm: str, email: str, c_date: str, img: str, state: str):
        self.id = id
        self.pw = pw
        self.nm = nm
        self.email = email
        self.c_date = c_date
        self.img = img
        self.state = state

# 로그인 요청 : 아이디, 비밀번호
class ReqLogin:
    def __init__(self, id:str, pw:str):
        self.id = id
        self.password = pw

# 로그아웃 요청 : 아이디, 시간
class ReqLoout:
    def __init__(self, id: str):
        self.id = id

# 채팅 송신 요청
class ReqChat:
    def __init__(self, msg: str): #msg = self.edt_txt.text()
        self.msg = msg

# 친구 초대 요청
class ReqSuggetsFriend:
    def __init__(self, myAddr: tuple, otherAddr: tuple): #myAddr : 초대요청자 소켓주소, otherAddr : 초대수락자 소켓주소
        self.myAddr = myAddr
        self.otherAddr = otherAddr

# 친구 수락 요청
class ReqAcceptFriend:
    def __init__(self, myAddr: tuple, otherAddr: tuple):
        self.myAddr = myAddr
        self.otherAddr = otherAddr

# 채팅방 개설 요청
class ReqJoinChat:
    def __init__(self, myAddr: tuple, otherAddr: tuple):
        self.myAddr = myAddr
        self.otherAddr = otherAddr

#############서버 -> 클라이언트#############

# 아이디 중복 체크 응답 : True(중복), False(중복아님)
class PerDuplicateCheck:
    def __init__(self, isExisited: bool):
        self.isExisited = isExisited

# 회원가입 허가 응답
class PerRegist:
    def __init__(self, Success: bool):
        self.Success = Success

# 로그인 허가 응답 : 허가번호, 아이디
# rescode = 0 ("아이디 존재하지 않음")
# rescode = 1 ("비밀번호 존재하지 않음")
# rescode = 2 ("로그인 한 아이디")
# rescode = 3 ("로그인 허가 완료")
class PerLogin:
    def __init__(self, rescode: int, id: str, time: str):
        self.rescode = rescode
        self.id = id
        self.time = time

# 로그아웃 허가 응답
class PerLogout:
    def __init__(self):
        pass

# 채팅 송신 허가 응답
class PerChat:
    def __init__(self, senderid: str, msg: str): #발신 아이디, 메세지
        self.senderid = senderid
        self.msg = msg

# 친구 초대 허가 응답
class PerSuggestFriend:
    def __init__(self, senderid: str, senderAddr: tuple): #발신 아이디, 발신 소켓 주소
        self.senderid = senderid
        self.senderAddr = senderAddr

# 친구 수락 허가 응답
class PerAcceptFriend:
    def __init__(self, senderid: str, senderAddr: tuple, receiveid: str, receiveAddr: tuple):
        self.senderid = senderid
        self.senderAddr = senderAddr
        self.receiveid = receiveid
        self.receiveAddr = receiveAddr

# 채팅방 개설 허가 응답
class PerJoinChat:
    def __init__(self): #개설 요청자 아이디,소켓 / #채팅방 참여자 아이디,소켓 (일대일, 일대다 고려)
        pass
