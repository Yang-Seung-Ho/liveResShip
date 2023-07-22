#배조아에서 공용으로 사용하는 모듈 임포트하기
import vcommon
import ncommon
import common

# 배조아 계정
VejoaID='ju5979'
VejoaPD='hj748159'

# 네이트 계정
NateID = 'ysh5979'
NatePD = 'hj748159'

# 네이트 보낼 이메일 주소 2개 
SendEmail1 = 'tmdgh5979@naver.com'
SendEmail2 = 'ysh5979@nate.com'

# 사이트 접속
try:

    # 배조아 로그인
    vcommon.y_vejoaLogin(VejoaID,VejoaPD)


    # 네이트 로그인 및 메일 보내기 접속
    ncommon.y_nateLogin(NateID,NatePD)

except :
    print("사이트 접속 오류")
    common.printErrMsg()
while True:
    try :
        # 녹동 상태 변경 
        vcommon.y_statusChange("녹동")


        # 새로 고침 하며 주문 내역 선택 후 새로운 탭으로 접속 (10초 단위)
        vcommon.y_refreshFind(10)

        # 네이트 이메일 전송
        ncommon.y_nateEmailSend(SendEmail1, SendEmail2)


        # 배조아 호출 사항 수정 및 입력 후 저장
        vcommon.y_vejoaUpdateOrder_nok()

        
        # 실행, 중지
        common.gostop_quit("한 번더돌릴거면 a 아니면 아무거나")
        continue
    except :
        # 오류 메세지 출력
        common.printErrMsg()
        break







