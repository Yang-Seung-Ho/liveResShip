import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains

driver1 = webdriver.Chrome()
driver1.get("https://www.vejoa.com/admin")
driver2 = webdriver.Chrome()
driver2.get("https://n.lrl.kr/")
wait2 = WebDriverWait(driver2, 10)  # 최대 10초까지 기다립니다.

InputId2 = wait2.until(EC.presence_of_element_located(
    (By.XPATH, "/html/body/main/div[3]/div[3]/div[3]/p")))

wait = WebDriverWait(driver1, 10)  # 최대 10초까지 기다립니다.
# 아이디 비밀번호 입력
InputId = wait.until(EC.presence_of_element_located(
    (By.XPATH, "/html/body/div[3]/div[2]/div/div/div/div/div[2]/form/div[1]/div/input")))
InputPd = wait.until(EC.presence_of_element_located(
    (By.XPATH, "/html/body/div[3]/div[2]/div/div/div/div/div[2]/form/div[2]/div/input")))
LoginBtn = wait.until(EC.presence_of_element_located(
    (By.XPATH, "/html/body/div[3]/div[2]/div/div/div/div/div[2]/form/div[3]/div[1]/button")))
InputId.send_keys("ju5979")
InputPd.send_keys("hj748159")
LoginBtn.click()
# 로그인 완료
# 주문내역 접속 (admin로그인이 되면 확인 주소값으로 확인 후 주문내역 주소로 이동)
current_url = driver1.current_url
if current_url == "https://www.vejoa.com/admin":
    driver1.get("https://www.vejoa.com/admin/cmall/cmallorder")
# 가장 상위 등록 버튼 클릭
# <a> 태그 요소 선택
RegisterBtn = wait.until(EC.presence_of_element_located(
    (By.XPATH, "/html/body/div[3]/div[3]/div/div/form/div[3]/table/tbody/tr[1]/td[5]/a")))
# 링크 주소 가져오기
link = RegisterBtn.get_attribute("href")
# 새로운 탭 열기
driver1.execute_script("window.open('about:blank', '_blank');")
# 탭 전환
driver1.switch_to.window(driver1.window_handles[-1])

# 새로운 탭에서 링크 주소로 이동
driver1.get(link)
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

print(isOneway, isRoundTrip)


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
#


# # 명단관리 요소 가져오기
# # 명단관리 버튼 클릭
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

# 왕복일시 왕복 명단도 출력
if isRoundTrip:
    tbody1_selector = driver1.find_element(By.ID, "tbody1")
    # # 테이블 태그에서 총 몇명인지 구해서 반복문 돌리는 함수
    tr_elements1 = tbody1_selector.find_elements(By.TAG_NAME, "tr")
    # # 명단관리 출력
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
        i += 1


# 차량정보 요소 가져오기
# iframe이 겹치는 이유로 인해 리랜더링
driver1.refresh()
CarsManagementBtn = wait.until(EC.presence_of_element_located(
    (By.XPATH, "/html/body/div[2]/div[1]/div[1]/span/button[5]")))
CarsManagementBtn.click()

driver1.switch_to.default_content()
frame_id = "iframe_btn"  # 변경해야 할 `iframe`의 ID
driver1.switch_to.frame(frame_id)
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
# 왕복일때 왕복 차량 확인 후 출력
if isRoundTrip:
    try:
        tbody1_selector = driver1.find_element(By.ID, "tbody1")
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
            i += 1
    except:
        print("왕복이지만, 차량은 없음")
        # 성공시 추가적인 코드가 있으면 작성


time.sleep(3)
# 현재 탭 닫기
# driver1.close()
# 원래 탭으로 전환
driver1.switch_to.window(driver1.window_handles[0])
time.sleep(100)
