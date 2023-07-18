import sys
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


# a 입력 시 진행
def gostop_quit(msg) :
    answer = input(msg)
    if not answer == 'a':
        quit()


# a 입력 시 진행 아니면 예외처리 및 종료
def gostop_exit(msg) :
    answer = input(msg)
    if not answer == 'a':
        return False


        





# 에러 메세지 출력
def printErrMsg() :
    err_msg = traceback.format_exc()
    print(err_msg)
    quit()


        