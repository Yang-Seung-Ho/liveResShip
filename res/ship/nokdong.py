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

#가변 정보들
NK_NateId='ysh5979'
NK_NatePassWord='hj748159'
NK_VejoaId='ju5979'
NK_VejoaPassWord='hj748159'
NK_Email1='tmdgh5979@naver.com'
NK_Email2='ysh5979@nate.com'

try :
    driver1 = webdriver.Chrome()
    driver1.maximize_window()
    driver1.get("https://www.vejoa.com/admin")
    wait = WebDriverWait(driver1, 10)  # 최대 10초까지 기다립니다.
    #네이트
    nate = webdriver.Chrome()
    nate.maximize_window()
    nate.get("https://www.nate.com/")
    wait_nate = WebDriverWait(nate, 10)  # 최대 10초까지 기다립니다.

    # 네이트 로그인
    IdInputBox = wait_nate.until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[1]/form/fieldset/input[1]")))
    IdInputBox.send_keys(NK_NateId)  # id 입력
    PassWordInputBox = wait_nate.until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[1]/form/fieldset/input[2]")))
    PassWordInputBox.send_keys(NK_NatePassWord)  # 비밀번호 입력
    time.sleep(1)
    ToLoginBtn = wait_nate.until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[1]/form/fieldset/input[4]")))
    ToLoginBtn.click()
    time.sleep(1)
    nate.get("https://mail3.nate.com/#write/?act=new")
    # 아이디 비밀번호 입력
    InputId = wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[3]/div[2]/div/div/div/div/div[2]/form/div[1]/div/input")))
    InputPd = wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[3]/div[2]/div/div/div/div/div[2]/form/div[2]/div/input")))
    LoginBtn = wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[3]/div[2]/div/div/div/div/div[2]/form/div[3]/div[1]/button")))
    InputId.send_keys(NK_VejoaId)
    InputPd.send_keys(NK_VejoaPassWord)
    LoginBtn.click()
    # 로그인 완료
    # 주문내역 접속 (admin로그인이 되면 확인 주소값으로 확인 후 주문내역 주소로 이동)
    current_url = driver1.current_url
    if current_url == "https://www.vejoa.com/admin":
        driver1.get("https://www.vejoa.com/admin/cmall/cmallorder")
    time.sleep(1)
except :
    print("사이트 로그인 오류입니다")

#반복 시작
while True:
    NK_name = ''
    NK_PhoneNumber = ''
    NK_From = []
    NK_RoomName = []
    NK_Date = []
    NK_Time = []
    # 명단관리
    NK_CustomerList = []
    NK_Car = ''
    ToListCopyInfo = ''
    FromListCopyInfo = ''
    try:
        #녹동 상태 클릭
        StatusSelect = Select(wait.until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[3]/div[3]/div/div/form/div[1]/div[1]/select[1]"))))
        StatusSelect.select_by_visible_text("녹동")
        StatusSearchBtn = wait.until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[3]/div[3]/div/div/form/div[1]/div[1]/button[2]")))
        StatusSearchBtn.click()
        #테이블 가장 하단 주문내역 접속 있을때까지 새로고침 하며 찾기
        while True:
            try:
                driver1.refresh()
                tr_elements = driver1.find_elements(By.XPATH, "//tbody/tr")
                last_tr_element = tr_elements[-1]
                a_element = last_tr_element.find_element(By.XPATH, ".//a")
                href_value = a_element.get_attribute("href")
                break  # 예외가 발생하지 않았을 경우 반복문 종료
            except Exception:
                print("주문 내역이 없습니다")
                #몇 초 마다 새로고침할지
                time.sleep(10)
                driver1.refresh()
                continue
        # 새로운 탭 열기
        driver1.execute_script("window.open('about:blank', '_blank');")
        # 탭 전환
        driver1.switch_to.window(driver1.window_handles[-1])
        # 새로운 탭에서 링크 주소로 이동
        driver1.get(href_value)
        # 기본 요소 가져오기
        # 편도인지 왕복인지
        try:
            RoundTrip = WebDriverWait(driver1, 3).until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[2]/div[1]/form[3]/div[2]")))
            isOneway = False
            isRoundTrip = True
        except:
            isOneway = True
            isRoundTrip = False
        # 배조아 사이트 정보가져오기
        try:
            # 예약자 이름, 전화번호
            NameValue = wait.until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[2]/div[1]/form[1]/div[5]/div[2]/input[1]"))).get_attribute('value')
            NK_name = NameValue
            
            PhoneNumberValue = wait.until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[2]/div[1]/form[1]/div[5]/div[2]/input[2]"))).get_attribute('value')
            NK_PhoneNumber = PhoneNumberValue

            # 첫 블록<div>
            # 왕복일때
            if isRoundTrip:
                FirstBlockDiv_values = []
                SecondBlockDiv_text = []
                ThirdBlockDiv_values = []
                a = 2  # 편도는 form[2] 왕복은 form[3]
                for i in range(2):
                    FirstBlockDiv = wait.until(EC.presence_of_element_located(
                        (By.XPATH, f"/html/body/div[2]/div[1]/form[{a}]/div[2]/div[2]/div[1]")))
                    # <div> 요소 안에 있는 텍스트들 가져오기, text_values[] 배열 순서대로 차례대로 인풋값들 저장
                    FirstBlockDiv_inputs = FirstBlockDiv.find_elements(
                        By.XPATH, ".//input[@type='text']")
                    FirstBlockDiv_values.append([input_element.get_attribute(
                        "value") for input_element in FirstBlockDiv_inputs])
                    # 두번째 블록
                    SecondBlockDiv = wait.until(EC.presence_of_element_located(
                        (By.XPATH, f"/html/body/div[2]/div[1]/form[{a}]/div[2]/div[2]/div[2]")))
                    SecondBlockDiv_text.append(SecondBlockDiv.text)
                    # 세번째 블록
                    ThirdBlockDiv = wait.until(EC.presence_of_element_located(
                        (By.XPATH, f"/html/body/div[2]/div[1]/form[{a}]/div[2]/div[2]/div[3]")))
                    ThirdBlockDiv_inputs = ThirdBlockDiv.find_elements(
                        By.XPATH, ".//input[@type='text']")
                    ThirdBlockDiv_values.append([input_element.get_attribute(
                        "value") for input_element in ThirdBlockDiv_inputs])
                    a += 1
            # 편도일때
            else:
                FirstBlockDiv_values = []
                SecondBlockDiv_text = []
                ThirdBlockDiv_values = []
                FirstBlockDiv = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[2]/div[1]/form[2]/div[2]/div[2]/div[1]")))
                FirstBlockDiv_inputs = FirstBlockDiv.find_elements(
                    By.XPATH, ".//input[@type='text']")
                FirstBlockDiv_values.append([input_element.get_attribute(
                    "value") for input_element in FirstBlockDiv_inputs])

                SecondBlockDiv = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[2]/div[1]/form[2]/div[2]/div[2]/div[2]")))
                SecondBlockDiv_text.append(SecondBlockDiv.text)

                ThirdBlockDiv = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[2]/div[1]/form[2]/div[2]/div[2]/div[3]")))
                ThirdBlockDiv_inputs = ThirdBlockDiv.find_elements(
                    By.XPATH, ".//input[@type='text']")
                ThirdBlockDiv_values.append([input_element.get_attribute(
                    "value") for input_element in ThirdBlockDiv_inputs])
            

            # 명단관리 요소 가져오기
            # 명단관리 버튼 클릭
            ListManagementBtn = wait.until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[2]/div[1]/div[1]/span/button[4]")))
            ListManagementBtn.click()
            # # iframe 이 계속 전환되기에 그에 맞는 함수 작성
            driver1.switch_to.default_content()
            frame_id = "iframe_btn"  # 변경해야 할 `iframe`의 ID
            driver1.switch_to.frame(frame_id)

            # 편도는 무조건 출력
            tbody0_selector = driver1.find_element(By.ID, "tbody0")
            tr_elements0 = tbody0_selector.find_elements(By.TAG_NAME, "tr")
            tr_count = len(tr_elements0)

            # 명단 일치 불일치 확인
            CustomerFromList = []
            CustomerToList = []

            # # 명단관리 출력
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
                CustomerFromList.append(cope_name_value0)
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
                i += 1
                # 편도 명단복사
                actions = ActionChains(driver1)
                FromListCopyBtn = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "/html/body/form/div[2]/table/tbody[1]/tr[1]/td/span[3]/button[3]")))
                FromListCopyBtn.click()
                actions.perform()
                FromListCopyInfo = pyperclip.paste()
            # 왕복일시 왕복 명단도 출력
            if isRoundTrip:
                tbody1_selector = driver1.find_element(By.ID, "tbody1")
                # 테이블 태그에서 총 몇명인지 구해서 반복문 돌리는 함수
                tr_elements1 = tbody1_selector.find_elements(By.TAG_NAME, "tr")
                # 명단관리 출력
                i = 0

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
                    CustomerToList.append(cope_name_value1)
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
                    i += 1
                    actions = ActionChains(driver1)
                    ToListCopyBtn = wait.until(EC.presence_of_element_located(
                        (By.XPATH, "/html/body/form/div[2]/table/tbody[2]/tr[1]/td/span[3]/button[3]")))
                    ToListCopyBtn.click()
                    actions.perform()
                    ToListCopyInfo = pyperclip.paste()
            # 명단 불일치 확인 2 (순서상관없이 동일한지) 동일하면 트루 아님 펄스
            is_same = set(CustomerFromList) == set(CustomerToList)

            # 차량정보 요소 가져오기
            # iframe이 겹치는 이유로 인해 리랜더링
            driver1.refresh()
            CarsManagementBtn = wait.until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[2]/div[1]/div[1]/span/button[5]")))
            CarsManagementBtn.click()

            driver1.switch_to.default_content()
            frame_id = "iframe_btn"  # 변경해야 할 `iframe`의 ID
            driver1.switch_to.frame(frame_id)
            try:
                tbody0_selector = driver1.find_element(By.ID, "tbody0")
                # 테이블 태그에서 총 몇명인지 구해서 반복문 돌리는 함수
                tr_elements = tbody0_selector.find_elements(By.TAG_NAME, "tr")
                tr_count = len(tr_elements)
                # 명단관리 출력
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
                    i += 1
                    NK_Car = cope_name_value0+" "+cope_birth_value0
            except:
                NK_Car = "차량 없음"
            # 왕복일때, 편도일때
            if NK_Car == '':
                NK_Car = "차량 없음"
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
            # 보내는 내용 총정리
            # 제목
            # 보낼 이메일 주소 입력
            time.sleep(3)
            #데이터를 가져오는 도중 문제가 없었다면 네이트 메일을 보내는 도중 예외처리가 됐을 땐 서버로딩이나 네이트 메일 오류이기에
            #반복해서 진행하도록 함
            while True :
                try :
                    EmailAddressBox = wait_nate.until(EC.presence_of_element_located(
                        (By.ID, "textArea__to")))
                    EmailAddressBox.clear()  # 기존 값 삭제
                    EmailAddressBox.send_keys(NK_Email1)
                    EmailAddressBox.send_keys(Keys.ENTER)
                    time.sleep(1)
                    EmailAddressBox.send_keys(NK_Email2)
                    EmailAddressBox.send_keys(Keys.ENTER)
                    # 제목 입력
                    MailSubjectBox = wait_nate.until(EC.presence_of_element_located(
                        (By.ID, "mail_subject")))
                    MailSubjectBox.send_keys(f'{NK_name} 님 예약요청건 입니다(헬로우/제주지사)')

                    # 내용
                    if isRoundTrip:
                        # iframe으로 전환
                        iframe = nate.find_element(By.ID, "editor_iframe")
                        nate.switch_to.frame(iframe)
                        InfoBox = nate.find_element(
                            By.XPATH, "/html/body/div/div/div[1]/div[3]/div[2]")
                        # 값 입력
                        InfoBox.clear()
                        InfoBox.send_keys(Keys.CONTROL, 'a')  # 텍스트 전체 선택
                    
                        if is_same:  # 왕복이고 동일 명단
                            InfoBox.send_keys(f'''
[예약요청]
1. 성함 : {NK_name}

2. 연락처 : {NK_PhoneNumber}

3. 스케줄&등급
{str(NK_From[0])} {str(NK_RoomName[0])} {str(NK_Date[0])} {str(NK_Time[0])}
{str(NK_From[1])} {str(NK_RoomName[1])} {str(NK_Date[1])} {str(NK_Time[1])}

4. 명단
{FromListCopyInfo}

5. 차량
{NK_Car}

왕복예약 부탁드립니다
감사합니다.
                                ''')
                        else:  # 왕복에 명단 동일하지 않을 때
                            InfoBox.send_keys(f'''
[예약요청]
1. 성함 : {NK_name}

2. 연락처 : {NK_PhoneNumber}

3. 스케줄&등급
{str(NK_From[0])} {str(NK_RoomName[0])} {str(NK_Date[0])} {str(NK_Time[0])}
{str(NK_From[1])} {str(NK_RoomName[1])} {str(NK_Date[1])} {str(NK_Time[1])}


4. 명단
{NK_CustomerList[0]}
{FromListCopyInfo}
{NK_CustomerList[1]}
{ToListCopyInfo}

5. 차량
{NK_Car}

왕복예약 부탁드립니다
감사합니다.
                                ''')
                    else:  # 편도일 때
                        # iframe으로 전환
                        iframe = nate.find_element(By.ID, "editor_iframe")
                        nate.switch_to.frame(iframe)
                        InfoBox = nate.find_element(
                            By.XPATH, "/html/body/div/div/div[1]/div[3]/div[2]")
                        # MailInfoBox = wait.until(EC.presence_of_element_located(
                        #     (By.ID, "wc_pc")))
                        # 값 입력
                        InfoBox.clear()
                        InfoBox.send_keys(Keys.CONTROL, 'a')  # 텍스트 전체 선택
                    
                        InfoBox.send_keys(f'''
[예약요청]
1. 성함 : {NK_name}

2. 연락처 : {NK_PhoneNumber}

3. 스케줄&등급
{str(NK_From[0])} {str(NK_RoomName[0])} {str(NK_Date[0])} {str(NK_Time[0])}

4. 명단
{FromListCopyInfo}

5. 차량
{NK_Car}

편도예약 부탁드립니다
감사합니다.
                                ''')
                    #메일 발송!
                    time.sleep(1)
                    nate.switch_to.default_content()
                    EmailAddressBox.click()
                    sendButton = nate.find_element(By.XPATH, '/html/body/div[11]/div[4]/div/div/div[1]/div[2]/div[5]/div[2]/div/div[1]/div[1]/div[1]/button')
                    sendButton.click()
                    time.sleep(3)
                    nate.get("https://mail3.nate.com/#write/?act=new")
                    break
                except :
                    print("네이트 메일 보내던 중 오류")
                    nate.get("https://mail3.nate.com/#write/?act=new")
                    time.sleep(3)
                    continue
            while True:
                try:
                    # 원래 탭으로 전환
                    driver1.switch_to.window(driver1.window_handles[1])
                    #호출 날짜 및 "아리온메일예약중" 입력
                    DateCall = wait.until(EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[2]/div[1]/form[1]/div[2]/div[2]/input[1]")))
                    DateCall.send_keys(str(date.today()))
                    DateCallSecondInputBox = wait.until(EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[2]/div[1]/form[1]/div[2]/div[2]/input[2]")))
                    DateCallSecondInputBox.clear()
                    DateCallSecondInputBox.send_keys("아리온메일예약중")
                    DateCallBtn = wait.until(EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[2]/div[1]/form[1]/div[2]/div[2]/button[1]")))
                    DateCallBtn.click()
                    time.sleep(1)
                    #호출 완료 버튼 클릭 (Alert)
                    alert = Alert(driver1)
                    alert.accept()
                    #참고사항 입력 후 수정
                    time.sleep(1)
                    noteTextAreaBox = wait.until(EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[2]/div[1]/form[2]/div[2]/div[2]/div[4]/textarea[1]")))
                    noteTextAreaReviseBtn = wait.until(EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[2]/div[1]/form[2]/div[2]/div[3]/p[3]/strong/button")))
                    noteTextAreaBox.clear()  # 기존 텍스트 삭제
                    if NK_Car == '' :
                        noteTextAreaBox.send_keys("차량없음/아리온메일예약중")
                    else : 
                        noteTextAreaBox.send_keys("아리온메일예약중")
                    #수정버튼 클릭
                    noteTextAreaReviseBtn.click()
                    #왕복시 아래 참고사항까지 입력 후 수정
                    if isRoundTrip : 
                        noteSecondTextAreaBox = wait.until(EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[2]/div[1]/form[3]/div[2]/div[2]/div[4]/textarea[1]")))
                        noteSecondTextAreaReviseBtn = wait.until(EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[2]/div[1]/form[3]/div[2]/div[3]/p[3]/strong/button")))
                        noteSecondTextAreaBox.clear()  # 기존 텍스트 삭제
                        noteSecondTextAreaBox.send_keys("아리온메일예약중")
                        noteSecondTextAreaReviseBtn.click()
                    #마무리됐으면 녹완 버튼 클릭
                    nokCompleteBtn = wait.until(EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[2]/div[1]/form[1]/div[1]/span[1]/button[7]")))
                    nokCompleteBtn.click()

                    if isRoundTrip :
                        print(NK_name,"왕복 메일 예약이 완료되었습니다.")
                    else :
                        print(NK_name,"편도 메일 예약이 완료되었습니다.") 
                    # 현재 탭 닫기
                    driver1.close()
                    driver1.switch_to.window(driver1.window_handles[0])
                    time.sleep(1)
                    driver1.refresh()
                    time.sleep(1) 
                    break  # 예외가 발생하지 않았을 경우 반복문 종료
                except :
                    print("배조아, 참고사항 및 호출 넣는 도중 오류")
                    time.sleep(3)
                    continue
        except :
            print("배조아 사이트에서 데이터를 가져오던 중 오류 발생")
            driver1.close()
            driver1.switch_to.window(driver1.window_handles[0])
            time.sleep(1)
            driver1.refresh()
            time.sleep(1)            
    except:
        print("오류가 났어요")
        err_msg = traceback.format_exc()
        print(err_msg)
        time.sleep(5)
        break
