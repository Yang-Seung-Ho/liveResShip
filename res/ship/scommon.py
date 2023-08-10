import common
import time
import pyautogui as pg
import pyperclip
import keyboard
import vcommonTest


pg.FAILSAFE = False

global Existence

# 바탕화면으로 이동
def y_moveBackground() :


    # 스크린의 너비와 높이를 가져옵니다
    screen_width, screen_height = pg.size()


    # 바탕화면의 오른쪽 하단 좌표 계산
    desktop_x = screen_width - 1
    desktop_y = screen_height - 1


    # 바탕화면의 오른쪽 하단으로 마우스 이동
    pg.click(desktop_x, desktop_y)
    
    time.sleep(1)


# 씨월드 접속
def y_goSeaworld() :

    common.search_click('res\images\seaworld_bg.PNG')
    pg.hotkey('enter')
    time.sleep(3)

    # count = 0


    # # 이전 실행된 씨월드 프로그램이 없을 시 (하단에 없을 시)
    # if count == 0 :
    #     common.search_doubleClick('res/images/seaworld_bg.PNG')
    #     count += 1


    # # 이전 실행된 씨월드 프로그램이 있을 시 (하단에 있을 시)
    # else : 
    #     pg.hotkey('alt','tab')


# 씨월드 로그인 및 실행
def y_LoginSeaworld() :
    
    # 씨월드 로그인
    time.sleep(3)

    # 비밀번호 입력 칸 클릭
    common.search_click("res/images/seaworld_pd.PNG",region=(0,0,1000,1000))
    time.sleep(1)
    pg.press('1')
    time.sleep(1)
    pg.hotkey('enter')
    time.sleep(3)


    # 선박 예약 더블 클릭
    common.search_doubleClick('res/images/res_shipLogo.PNG',region=(0,0,1000,1000))

    time.sleep(3)
    

# 씨월드 실행 함수 (종합)
def y_runSeaworld():
    Existence = False

    # 기존 실행된 씨월드 없을 시
    if Existence == False :
        y_moveBackground()
        y_goSeaworld()
        y_LoginSeaworld()
        Existence = True
    # 기존 실행된 씨월드 있을 시
    else :

        # 추후 수정
        pg.hotkey('alt','tab')
    
    time.sleep(3)



# 선박 및 출발지로 클릭할 이미지 리턴
def y_shipSelect(ship, ship_from) :
    

    # 선박이 산타모니카 일 경우 (진도)
    if ship == '산타모니카' :
        return "산타모니카"
    # 선박이 산타모니카 아닐 경우 (목포)
    elif ship == '퀸제누비아' :
        if ship_from == "목포" :
            return "res/ship_images/qjm.PNG"
        elif ship_from == "제주" :
            return "res/ship_images/qjj.PNG"
    elif ship == '퀸메리2' :
        if ship_from == "목포" :
            return "res/ship_images/qmm.PNG"
        elif ship_from == "제주" :
            return "res/ship_images/qmj.PNG"
    
    time.sleep(1)


# 선박 예약 창 닫기
def y_resClose():        
    common.search_click("res/images/res_exit.PNG", region=(0,0,2000,200))
    time.sleep(1)
    keyboard.press_and_release('tab')
    time.sleep(1)
    keyboard.press_and_release('enter')
    time.sleep(1)



# 씨월드 예약 처리 
def y_reservation() :

    
    # 배조아에서 선박명, 날짜, 시간 데이터 가져오기
    ship_name, ship_from ,ship_date ,ship_time = vcommonTest.y_data('씨월드')
    # ship_name, ship_from ,ship_date = vcommonTest.y_data('씨월드')
    
    # def y_reservation(ship_date[0]) :

    while True :
        # 프로그램 내 선박 예약 클릭
        common.search_click('res/images/res_shipSeaworld.PNG', region=(0,0,600,200))
        # common.gostop_exit("a")
        time.sleep(3)


        # 선박 예약 클릭 되었는지 확인, 안되었을 시 재시도
        checkLogo =pg.locateOnScreen('res/images/ship_resCheck.PNG',confidence=0.5,region=(0,0,500,500))
        print(checkLogo)
        if checkLogo == None :
            continue
        else :
            break
        


    # 엔터 3번 입력
    for _ in range(3):
        pg.press('enter')
        time.sleep(0.5)

    
    # 날짜 입력
    pyperclip.copy(ship_date[0])
    # pyperclip.copy(20230925)
    pg.hotkey('ctrl', 'v')
    time.sleep(3)
    keyboard.press_and_release('f2')
    time.sleep(1)
    
    
    try :
        # 선박 선택
        common.search_click(y_shipSelect(ship_name[0],ship_from[0]), region=(100,100,1200,1000))
        time.sleep(1)
    
    # 이미지 못찾을 시 남은 좌석 없는 것
    except:

        # 선박 테이블 창 닫기
        keyboard.press_and_release('esc')
        time.sleep(1)

        # 선박 예약 창 닫기
        y_resClose()
        print("해당 선박 없음")



    # 엔터 3번 입력
    for _ in range(3):
        pg.press('enter')
        time.sleep(0.5)

    #


    
    

