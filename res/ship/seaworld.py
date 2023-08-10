#배조아에서 공용으로 사용하는 모듈 임포트하기
import vcommonTest
import common
import scommon

# 배조아 계정
VejoaID='ju5979'
VejoaPD='hj748159'



# 사이트 접속
try:

    # 배조아 로그인
    vcommonTest.y_vejoaLogin(VejoaID,VejoaPD)


    # 녹동 상태 변경 
    vcommonTest.y_statusChange("녹동")


    # 새로 고침 하며 주문 내역 선택 후 새로운 탭으로 접속 (10초 단위)
    vcommonTest.y_refreshFind(10)        

    
    # 씨월드 실행
    scommon.y_runSeaworld()


    # 씨월드 예약하기 진행
    scommon.y_reservation()
    # scommon.y_reservation(ship_date[0],ship_name[0],'1340')
    

    # a 누를 시 복귀
    common.gostop_quit("press 'a'")
    

    # 씨월드 선박예약 탭 닫기
    scommon.y_resClose()


    # 배조아 탭 닫기
    vcommonTest.y_vejoaTabClose()


    


except :
    print("사이트 접속 오류")
    common.printErrMsg()


