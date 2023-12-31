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
import common
import vcommon

# 전역 변수로 드라이버와 대기 객체 선언
nateDriver = None
wait_nate = None




# 네이트 로그인
def y_nateLogin(NateID, NatePD) :
    
    # 전역 변수로 선언
    global nateDriver, wait_nate


    # 네이트 접속 및 로그인 오류 시 창 닫기 후 반복
    while True :
          try :
                # 네이트 접속
            nateDriver = webdriver.Chrome()
            nateDriver.maximize_window()
            nateDriver.get("https://www.nate.com/")
            wait_nate = WebDriverWait(nateDriver, 10)  # 최대 10초까지 기다립니다.


            # 네이트 아이디 입력
            IdInputBox = wait_nate.until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[1]/form/fieldset/input[1]")))
            IdInputBox.send_keys(NateID)  


            # 네이트 비밀번호 입력
            PassWordInputBox = wait_nate.until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[1]/form/fieldset/input[2]")))
            PassWordInputBox.send_keys(NatePD)  
            time.sleep(1)


            # 네이트 로그인 버튼 클릭
            ToLoginBtn = wait_nate.until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[1]/form/fieldset/input[4]")))
            ToLoginBtn.click()
            time.sleep(1)
            break
          except:
            time.sleep(1)
            nateDriver.close()
            time.sleep(1)
            continue
    



# 네이트 메일 내용 정리
def y_nateEmailMsg():

    # 배조아 사이트에서 필요한 정보 가져오기
    isRoundTrip, is_same, NK_name, NK_PhoneNumber, NK_From, NK_RoomName, NK_Date, NK_Time, NK_CustomerList, FromListCopyInfo, ToListCopyInfo, NK_Car = vcommon.y_data("녹동")


    # 메일 제목 내용
    EmailSubject = f'{NK_name} 님 예약요청건 입니다(헬로우/제주지사)'

    # 예약요청 메시지 생성
    EmailMsg = f'''
[예약요청]
1. 성함 : {NK_name}

2. 연락처 : {NK_PhoneNumber}

'''
        
    # 편도일 때
    if not isRoundTrip:  
            EmailMsg += f'''
3. 스케줄&등급
{str(NK_From[0])} {str(NK_RoomName[0])} {str(NK_Date[0])} {str(NK_Time[0])}

        '''
        

    # 왕복일 때
    elif isRoundTrip:  
            EmailMsg += f'''
3. 스케줄&등급
{str(NK_From[0])} {str(NK_RoomName[0])} {str(NK_Date[0])} {str(NK_Time[0])}
{str(NK_From[1])} {str(NK_RoomName[1])} {str(NK_Date[1])} {str(NK_Time[1])}

        '''


    # 왕복이고 명단 동일하지 않을 때
    if isRoundTrip and not is_same:  
            EmailMsg += f'''
4. 명단
{NK_CustomerList[0]}
{FromListCopyInfo}
{NK_CustomerList[1]}
{ToListCopyInfo}

        '''
            
    # 왕복이고 동일 명단 일 때
    elif isRoundTrip and is_same:  
            EmailMsg += f'''
4. 명단
{FromListCopyInfo}

        '''
        
    EmailMsg += f'''
5. 차량
{NK_Car}

{'왕복예약' if isRoundTrip else '편도예약'} 부탁드립니다
감사합니다.
        '''

    return EmailSubject, EmailMsg






# 네이트 메일 보내기 접속, 메일 전송
def y_nateEmailSend(SendEmail1, SendEmail2):
    EmailSubject, EmailMsg = y_nateEmailMsg()
    while True :
        try :
            # 메일 보내기 접속
            nateDriver.get("https://mail3.nate.com/#write/?act=new")
            time.sleep(3)
            # 상대 이메일 주소 입력
            EmailAddressBox = wait_nate.until(EC.presence_of_element_located(
                (By.ID, "textArea__to")))
            EmailAddressBox.clear()  # 기존 값 삭제
            EmailAddressBox.send_keys(SendEmail1)
            EmailAddressBox.send_keys(Keys.ENTER)
            time.sleep(1)
            EmailAddressBox.send_keys(SendEmail2)
            EmailAddressBox.send_keys(Keys.ENTER)


            # 제목 입력
            MailSubjectBox = wait_nate.until(EC.presence_of_element_located(
                (By.ID, "mail_subject")))
            MailSubjectBox.send_keys(EmailSubject)


            # iframe 전환
            iframe = nateDriver.find_element(By.ID, "editor_iframe")
            nateDriver.switch_to.frame(iframe)


            # 예약요청 입력 시작
            InfoBox = nateDriver.find_element(By.XPATH, "/html/body/div/div/div[1]/div[3]/div[3]")
            InfoBox.clear()
            InfoBox.send_keys(Keys.CONTROL, 'a')  # 텍스트 전체 선택


            # 예약 메시지 입력 후 iframe 기본 전환
            InfoBox.send_keys(EmailMsg)
            time.sleep(1)
            nateDriver.switch_to.default_content()
            EmailAddressBox.click()
            
            
            # 메일 검토
            answer = input("메일 검토 _메일 전송 a, 재시도 b, 종료할거면 c")
            if  answer == 'a':


                # 메일 보내기 버튼 클릭
                sendButton = nateDriver.find_element(By.XPATH, '/html/body/div[11]/div[4]/div/div/div[1]/div[2]/div[5]/div[2]/div/div[1]/div[1]/div[1]/button')
                sendButton.click()
                time.sleep(3)
                break        
            elif answer == 'b' :
                continue
            
            elif answer == 'c' :
                quit()
        except :
            print("네이트 메일 보내던 중 오류")
            common.printErrMsg()
            time.sleep(3)
            
        
        
        