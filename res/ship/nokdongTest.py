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
OpponentEmail1 = 'tmdgh5979@naver.com'
OpponentEmail2 = 'ysh5979@nate.com'

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


        # 배조아 데이터 가져오기(녹동)
        isRoundTrip, is_same, NK_name, NK_PhoneNumber, NK_From, NK_RoomName, NK_Date, NK_Time, NK_CustomerList, FromListCopyInfo, ToListCopyInfo, NK_Car = vcommon.y_data("녹동")


        # 네이트 이메일 전송
        ncommon.y_nateEmailSend(OpponentEmail1, OpponentEmail2,isRoundTrip, is_same, NK_name, NK_PhoneNumber, NK_From, NK_RoomName, NK_Date, NK_Time, NK_CustomerList, FromListCopyInfo, ToListCopyInfo, NK_Car)


        # 배조아 호출 사항 수정 및 입력 후 저장
        vcommon.y_vejoaUpdateOrder_nok()

        
        # 실행, 중지
        common.gostop_quit("한 번더돌릴거면 a 아니면 아무거나")
        continue
    except :
        # 오류 메세지 출력
        common.printErrMsg()
        break







