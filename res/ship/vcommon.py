from ssl import ALERT_DESCRIPTION_ACCESS_DENIED
import time
import traceback
from datetime import date
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from common import gostop_quit
from selenium.common.exceptions import TimeoutException
# 전역 변수로 드라이버와 대기 객체 선언
vejoaDriver = None
wait = None


# 전역 변수로 드라이버와 대기 객체 선언 (20230810)
vejoaDriver = None
wait = None

#배조아 사이트 로그인 후 주문내역으로 이동
def y_vejoaLogin(vejoaID,vejoaPD):
    
    # 배조아 가상드라이버, 최대기다림 시간 전역변수로 설정
    global vejoaDriver, wait


    # 사이트 접속 및 로그인 성공 시 까지 무한 루프
    while True :


        # 배조아 사이트 접속
        vejoaDriver = webdriver.Chrome()


        # 가상 드라이버 최대화
        vejoaDriver.maximize_window()


        # 배조아 사이트 접속
        vejoaDriver.get("https://www.vejoa.com/admin")
        

        # 최대 기다림 시간 지정   
        wait = WebDriverWait(vejoaDriver, 10)  
        

        # 사이트 접속 여부 확인 후 접속 시 로그인 정보 입력
        try :         
            # 아이디 비밀번호 입력 후 로그인
            InputId = wait.until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[3]/div[2]/div/div/div/div/div[2]/form/div[1]/div/input")))
            InputPd = wait.until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[3]/div[2]/div/div/div/div/div[2]/form/div[2]/div/input")))

            
            # 아이디 비밀번호 입력
            InputId.send_keys(vejoaID)
            InputPd.send_keys(vejoaPD)

        
            #로그인 버튼 클릭
            LoginBtn = wait.until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[3]/div[2]/div/div/div/div/div[2]/form/div[3]/div[1]/button")))
            LoginBtn.click()


            #로그인 완료 시 반복 문 종료
            break


        # 사이트 접속 및 로그인 오류 시 
        except :
            
            
            # 가상 드라이버 닫기 후 재시도
            vejoaDriver.close()
            continue

    
    # 로그인 완료 여부 확인 
    AdminLogo = wait.until(EC.presence_of_element_located(
    (By.XPATH, "/html/body/div[3]/div[1]/div/div[1]/span/a")))
    if AdminLogo :
         # 주문내역 접속
        vejoaDriver.get("https://www.vejoa.com/admin/cmall/cmallorder")
        
    time.sleep(1)
    




# 주문내역 상태 변경 
def y_statusChange(statusName) :
    
    # 변경할 상태 클릭
    StatusSelect = Select(wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[3]/div[3]/div/div/form/div[1]/div[1]/select[1]"))))
    StatusSelect.select_by_visible_text(statusName)


    # 상태 변경 후 검색 버튼 클릭
    StatusSearchBtn = wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[3]/div[3]/div/div/form/div[1]/div[1]/button[2]")))
    StatusSearchBtn.click()
    time.sleep(1)
    

# 무한 새로고침 하며 하단 주문 내역 선택 후 접속
def y_refreshFind(period) : # (period) 몇 초 단위로 새로고침 하는 지
    
    while True:
        try:
            # 테이블 가장 하단 주문 내역 검색
            vejoaDriver.refresh()
            tr_elements = vejoaDriver.find_elements(By.XPATH, "//tbody/tr")
            last_tr_element = tr_elements[-1]
            a_element = last_tr_element.find_element(By.XPATH, ".//a")
            href_value = a_element.get_attribute("href")


            # 예외가 발생하지 않았을 경우 반복문 종료
            break  

        except Exception:
            print("주문 내역이 없습니다")
            
            #몇 초 마다 새로고침할지
            time.sleep(period)
            vejoaDriver.refresh()

            
            # 주문 내역이 없을 경우 다시 검색
            continue


    # 새로운 탭 열기    
    vejoaDriver.execute_script("window.open('about:blank', '_blank');")
    

    # 탭 전환
    vejoaDriver.switch_to.window(vejoaDriver.window_handles[-1])


    # 새로운 탭에서 링크 주소로 이동
    vejoaDriver.get(href_value)
    




# 배조아 데이터 가져와서 리턴하기
def y_data(ship) :
    
    # 전역 변수 선언
    global FirstBlockDiv_values, SecondBlockDiv_text, ThirdBlockDiv_values,NK_name,NK_PhoneNumber, isCar, isRoundTrip


    # 예약자 이름
    NameValue = wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[2]/div[1]/form[1]/div[5]/div[2]/input[1]"))).get_attribute('value')
    NK_name = NameValue
    
    
    # 예약자 전화번호
    PhoneNumberValue = wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[2]/div[1]/form[1]/div[5]/div[2]/input[2]"))).get_attribute('value')
    NK_PhoneNumber = PhoneNumberValue


    # 왕복, 편도 구별
    try:
        RoundTrip = WebDriverWait(vejoaDriver, 3).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[2]/div[1]/form[3]/div[2]")))
        isRoundTrip = True
    except:
        isRoundTrip = False

    
    # 데이터 저장 공간
    isCar = False
    CustomerFromList = []
    CustomerToList = []
    FirstBlockDiv_values = []
    SecondBlockDiv_text = []
    ThirdBlockDiv_values = []
    ListData = [[],[]]
    CarData = [[],[]]
    NK_CustomerList=[]


    def find_block_values(form_number):
        block_values = []
        
        FirstBlockDiv = wait.until(EC.presence_of_element_located(
            (By.XPATH, f"/html/body/div[2]/div[1]/form[{form_number}]/div[2]/div[2]/div[1]")))
        FirstBlockDiv_inputs = FirstBlockDiv.find_elements(By.XPATH, ".//input[@type='text']")
        block_values.append([input_element.get_attribute("value") for input_element in FirstBlockDiv_inputs])
        
        SecondBlockDiv = wait.until(EC.presence_of_element_located(
            (By.XPATH, f"/html/body/div[2]/div[1]/form[{form_number}]/div[2]/div[2]/div[2]")))
        block_values.append(SecondBlockDiv.text)
        
        ThirdBlockDiv = wait.until(EC.presence_of_element_located(
            (By.XPATH, f"/html/body/div[2]/div[1]/form[{form_number}]/div[2]/div[2]/div[3]")))
        ThirdBlockDiv_inputs = ThirdBlockDiv.find_elements(By.XPATH, ".//input[@type='text']")
        block_values.append([input_element.get_attribute("value") for input_element in ThirdBlockDiv_inputs])
        
        return block_values

    if isRoundTrip:
        for form_number in range(2, 4):
            block_values = find_block_values(form_number)
            FirstBlockDiv_values.append(block_values[0])
            SecondBlockDiv_text.append(block_values[1])
            ThirdBlockDiv_values.append(block_values[2])
    else:
        block_values = find_block_values(2)
        FirstBlockDiv_values.append(block_values[0])
        SecondBlockDiv_text.append(block_values[1])
        ThirdBlockDiv_values.append(block_values[2])


    # 명단관리 요소 가져오기
    # 명단관리 버튼 클릭
    ListManagementBtn = wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[2]/div[1]/div[1]/span/button[4]")))
    ListManagementBtn.click()


    # iframe 이 계속 전환되기에 그에 맞는 함수 작성
    vejoaDriver.switch_to.default_content()
    frame_id = "iframe_btn" 
    vejoaDriver.switch_to.frame(frame_id)

    
    # 편도는 무조건 출력
    tbody0_selector = vejoaDriver.find_element(By.ID, "tbody0")
    tr_elements0 = tbody0_selector.find_elements(By.TAG_NAME, "tr")
    tr_count = len(tr_elements0)
    
    
    # 명단관리 출력
    i = 0
    
    
    # 편도
    for tr_element0 in tr_elements0[2:]:
    
    
        # 성별
        checked_radio = tr_element0.find_element(
            By.CSS_SELECTOR, f'input[name="cope_sex[0][{i}]"]:checked')
        checked_value = checked_radio.get_attribute("value")
        if checked_value == "0":
            checked_text0 = "남"
        elif checked_value == "1":
            checked_text0 = "여"
        else:
            checked_text0 = "Unknown"
    
    
        # 분류
        ciop1_title_element = tr_element0.find_element(
            By.XPATH, f".//input[@name='ciop1_title[0][{i}]']")
        ciop1_title_value0 = ciop1_title_element.get_attribute("value")
    
    
        # 이름
        cope_name_element = tr_element0.find_element(
            By.XPATH, f"//input[@name='cope_name[0][{i}]']")
        cope_name_value0 = cope_name_element.get_attribute("value")
    
    
        # 생년월일
        cope_birth_element = tr_element0.find_element(
            By.XPATH, f"//input[@name='cope_birth[0][{i}]']")
        cope_birth_value0 = cope_birth_element.get_attribute("value")
    
    
        # 연락처
        cope_tel_element = tr_element0.find_element(
            By.XPATH, f"//input[@name='cope_tel[0][{i}]']")
        cope_tel_value0 = cope_tel_element.get_attribute("value")
    
    
        # 순서
        cope_order_element = tr_element0.find_element(
            By.XPATH, f"//input[@name='cope_order[0][{i}]']")
        cope_order_value0 = cope_order_element.get_attribute("value")
    
        
        # 명단 관리 데이터 저장
        ListData[0].append([ciop1_title_value0, cope_name_value0, checked_text0, cope_birth_value0, cope_tel_value0])
        
        
        # 편도 명단복사
        actions = ActionChains(vejoaDriver)
        FromListCopyBtn = wait.until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/form/div[2]/table/tbody/tr[1]/td/span[3]/button[3]")))
        FromListCopyBtn.click()
        actions.perform()
        FromListCopyInfo = pyperclip.paste()
        
        
        # 편도일 시 왕복 정보는 공백
        ToListCopyInfo=''
        i += 1

    # 왕복일시 왕복 명단도 출력
    if isRoundTrip:
        
        tbody1_selector = vejoaDriver.find_element(By.ID, "tbody1")
        
        
        # 테이블 태그에서 총 몇명인지 구해서 반복문 돌리는 함수
        tr_elements1 = tbody1_selector.find_elements(By.TAG_NAME, "tr")
        
        
        # 명단관리 출력
        i = 0
        
        
        # 편도
        for tr_element1 in tr_elements1[2:]:
        
        
            # 성별
            checked_radio = tr_element1.find_element(
                By.CSS_SELECTOR, f'input[name="cope_sex[1][{i}]"]:checked')
            checked_value = checked_radio.get_attribute("value")
            if checked_value == "0":
                checked_text1 = "남"
            elif checked_value == "1":
                checked_text1 = "여"
            else:
                checked_text1 = "Unknown"
        
        
            # 분류
            ciop1_title_element = tr_element1.find_element(
                By.XPATH, f".//input[@name='ciop1_title[1][{i}]']")
            ciop1_title_value1 = ciop1_title_element.get_attribute("value")
        
        
            # 이름
            cope_name_element = tr_element1.find_element(
                By.XPATH, f"//input[@name='cope_name[1][{i}]']")
            cope_name_value1 = cope_name_element.get_attribute("value")
        
        
            # 생년월일
            cope_birth_element = tr_element1.find_element(
                By.XPATH, f"//input[@name='cope_birth[1][{i}]']")
            cope_birth_value1 = cope_birth_element.get_attribute("value")
        
        
            # 연락처
            cope_tel_element = tr_element1.find_element(
                By.XPATH, f"//input[@name='cope_tel[1][{i}]']")
            cope_tel_value1 = cope_tel_element.get_attribute("value")
        
        
            # 순서
            cope_order_element = tr_element1.find_element(
                By.XPATH, f"//input[@name='cope_order[1][{i}]']")
            cope_order_value1 = cope_order_element.get_attribute("value")
        
            
            # 명단 관리 데이터 저장
            ListData[1].append([ciop1_title_value1, cope_name_value1, checked_text1, cope_birth_value1, cope_tel_value1])
            
            
            # 왕복 명단복사
            actions = ActionChains(vejoaDriver)
            ToListCopyBtn = wait.until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/form/div[2]/table/tbody[2]/tr[1]/td/span[3]/button[3]")))
            ToListCopyBtn.click()
            actions.perform()
            ToListCopyInfo = pyperclip.paste()
            i += 1
    

    # 차량정보 요소 가져오기
    
    # iframe이 겹치는 이유로 인해 리랜더링
    vejoaDriver.refresh()
    CarsManagementBtn = wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[2]/div[1]/div[1]/span/button[5]")))
    CarsManagementBtn.click()

    
    # iframe 전환
    vejoaDriver.switch_to.default_content()
    frame_id = "iframe_btn"  # 변경해야 할 `iframe`의 ID
    vejoaDriver.switch_to.frame(frame_id)
    tbody0_selector = vejoaDriver.find_element(By.ID, "tbody0")
    
    
    # 테이블 태그에서 총 몇명인지 구해서 반복문 돌리는 함수
    tr_elements = tbody0_selector.find_elements(By.TAG_NAME, "tr")
    tr_count = len(tr_elements)
    
    if tr_count >= 3 :
        isCar = True
    
    
        # 차량관리 출력
        i = 0
        for tr_element in tr_elements[2:]:
    
            # 분류
            ciop1_title_element = tr_element.find_element(
                By.XPATH, f".//input[@name='ciop2_title[0][{i}]']")
            ciop1_title_value0 = ciop1_title_element.get_attribute("value")
    
    
            # 차량명
            cope_name_element = tr_element.find_element(
                By.XPATH, f"//input[@name='coca_name[0][{i}]']")
            cope_name_value0 = cope_name_element.get_attribute("value")
    
    
            # 차량번호
            cope_birth_element = tr_element.find_element(
                By.XPATH, f"//input[@name='coca_number[0][{i}]']")
            cope_birth_value0 = cope_birth_element.get_attribute("value")
    
    
            # 순서
            ciop2_order_element = tr_element.find_element(
                By.XPATH, f"//input[@name='ciop2_order[0][{i}]']")
            ciop2_order_value0 = ciop2_order_element.get_attribute("value")
    
            # 차량 데이터 저장
            CarData[0].append([cope_name_value0, cope_birth_value0])
            i += 1
        
        
        # 왕복일때 왕복 차량 확인 후 출력
        if isRoundTrip:
            try:
                tbody1_selector = vejoaDriver.find_element(By.ID, "tbody1")
        
        
                # 테이블 태그에서 총 몇명인지 구해서 반복문 돌리는 함수
                tr_elements = tbody1_selector.find_elements(By.TAG_NAME, "tr")
                tr_count = len(tr_elements)
        
        
                # 명단관리 출력
                i = 0
                for tr_element in tr_elements[2:]:
        
        
                    # 분류
                    ciop1_title_element = tr_element.find_element(
                        By.XPATH, f".//input[@name='ciop2_title[1][{i}]']")
                    ciop1_title_value1 = ciop1_title_element.get_attribute("value")
        
        
                    # 차량명
                    cope_name_element = tr_element.find_element(
                        By.XPATH, f"//input[@name='coca_name[1][{i}]']")
                    cope_name_value1 = cope_name_element.get_attribute("value")
        
        
                    # 차량번호
                    cope_birth_element = tr_element.find_element(
                        By.XPATH, f"//input[@name='coca_number[1][{i}]']")
                    cope_birth_value1 = cope_birth_element.get_attribute("value")
        
        
                    # 순서
                    ciop2_order_element = tr_element.find_element(
                        By.XPATH, f"//input[@name='ciop2_order[1][{i}]']")
                    ciop2_order_value1 = ciop2_order_element.get_attribute("value")
        

                    # 차량 데이터 저장
                    CarData[1].append([cope_name_value1, cope_birth_value1])
                    i += 1
            except:
                print("왕복이지만, 차량은 없음")
    

    #녹동일 시 리턴할 값들 전부 정리
    if ship == "녹동" :
        is_same = False
        # 값 받아오기
        
        # 명단관리
        if isCar : 
            NK_Car = str(CarData[0][0][0]) + " " + str(CarData[0][0][1])
        else : 
            NK_Car = "차량 없음"
        
        
        # 원래 탭으로 전환
        if isRoundTrip:
            NK_From = [FirstBlockDiv_values[0][2]]
            NK_RoomName = [FirstBlockDiv_values[0][1]]
            NK_Date = [FirstBlockDiv_values[0][3]]
            NK_Time = [FirstBlockDiv_values[0][4]+":"+FirstBlockDiv_values[0][5]]
            NK_From.append(FirstBlockDiv_values[1][2])
            NK_RoomName.append(FirstBlockDiv_values[1][1])
            NK_Date.append(FirstBlockDiv_values[1][3])
            NK_Time.append(FirstBlockDiv_values[1]
                        [4]+":"+FirstBlockDiv_values[1][5])
            for i in range(len(ListData[0])):
                CustomerFromList.append(ListData[0][i][1])
            
            for i in range(len(ListData[1])):
                CustomerToList.append(ListData[1][i][1])
            is_same = set(CustomerFromList) == set(CustomerToList)
        
        
            # 명단 동일하지않을시
            if not is_same:
                NK_CustomerList.append(
                    NK_From[0]+"발"+str(len(CustomerFromList))+"명")
                NK_CustomerList.append(
                    NK_From[1]+"발"+str(len(CustomerToList))+"명")
            
        else:
            NK_From = [FirstBlockDiv_values[0][2]]
            NK_RoomName = [FirstBlockDiv_values[0][1]]
            NK_Date = [FirstBlockDiv_values[0][3]]
            NK_Time = [FirstBlockDiv_values[0][4]+":"+FirstBlockDiv_values[0][5]]
        
        
        vejoaDriver.switch_to.window(vejoaDriver.window_handles[0])
        
        
        # 받아올 변수와 데이터들 리턴
        return(isRoundTrip, is_same, NK_name, NK_PhoneNumber, NK_From, NK_RoomName, NK_Date, NK_Time, NK_CustomerList, FromListCopyInfo, ToListCopyInfo, NK_Car)



    

# 배조아 호출 수정 및 업데이트
def y_vejoaUpdateOrder_nok() :
    
    try:
        # 원래 탭으로 전환
        vejoaDriver.switch_to.window(vejoaDriver.window_handles[1])


        # 호출 금일 날짜 입력
        DateCall = wait.until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[2]/div[1]/form[1]/div[2]/div[2]/input[1]")))
        DateCall.send_keys(str(date.today()))
        

        # 호출 "아리온메일예약중" 입력
        DateCallSecondInputBox = wait.until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[2]/div[1]/form[1]/div[2]/div[2]/input[2]")))
        DateCallSecondInputBox.send_keys("아리온메일예약중")


        # 호출 버튼 클릭
        DateCallBtn = wait.until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[2]/div[1]/form[1]/div[2]/div[2]/button[1]")))
        DateCallBtn.click()

        time.sleep(1)
        

        #호출 완료 시 alert 창 버튼 클릭
        alert = Alert(vejoaDriver)
        alert.accept()
        time.sleep(1)


        #참고사항 입력 후 수정

        # 차량에 따라 입력 사항 변경
        note_text = "아리온메일예약중" if isCar else "차량없음/아리온메일예약중"
        
        
        # 첫번째 참고사항 입력
        enter_customer_note_box(note_text)

        
        # 왕복 시 두번째 참고사항 입력
        if isRoundTrip:
            enter_customer_second_note_box(note_text)

        
        # 녹완 버튼 클릭
        click_nok_complete_button()

        
        if isRoundTrip :
            print(NK_name,"왕복 메일 예약이 완료되었습니다.")
        else :
            print(NK_name,"편도 메일 예약이 완료되었습니다.") 

        # 현재 탭 닫기
        vejoaDriver.close()
        vejoaDriver.switch_to.window(vejoaDriver.window_handles[0])
        time.sleep(1)
        vejoaDriver.refresh()
        time.sleep(1) 
    except :
        print("배조아, 참고사항 및 호출 넣는 도중 오류")
        time.sleep(3)





# 참고 사항 입력 함수 정리 시작
def enter_customer_note_box(note_text):
    CustomerNoteBox = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[1]/form[2]/div[2]/div[2]/div[4]/textarea[1]")))
    CustomerNoteBox.send_keys(note_text)

    CustomerNoteSubmitBtn = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[1]/form[2]/div[2]/div[3]/p[3]/strong/button")))
    CustomerNoteSubmitBtn.click()

def enter_customer_second_note_box(note_text):
    CustomerSecondNoteBox = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[1]/form[3]/div[2]/div[2]/div[4]/textarea[1]")))
    CustomerSecondNoteBox.send_keys(note_text)

    CustomerSecondNoteSubmitBtn = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[1]/form[3]/div[2]/div[3]/p[3]/strong/button")))
    CustomerSecondNoteSubmitBtn.click()
    # 녹완 버튼
def click_nok_complete_button():
    nokCompleteBtn = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[1]/form[1]/div[1]/span[1]/button[7]")))
    nokCompleteBtn.click()
# 참고 사항 입력 함수 정리 끝

