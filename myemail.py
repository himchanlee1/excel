from selenium import webdriver
from selenium.webdriver.common.by import By
from openpyxl import load_workbook
import time

# webdriver-manager 사용을 위한 추가 import 문
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def slow_type(element, text, delay=0.1):
    """주어진 요소에 텍스트를 천천히 입력합니다."""
    for character in text:
        element.send_keys(character)
        time.sleep(delay)

# webdriver-manager를 사용하여 ChromeDriver의 경로를 자동으로 관리
s = Service(ChromeDriverManager().install())

# 셀레니움 웹드라이버 초기화
driver = webdriver.Chrome(service=s)

# 네이버 로그인 페이지로 이동
driver.get("https://nid.naver.com/nidlogin.login")

# 사용자의 아이디와 비밀번호 천천히 입력
naver_id = "s846464"  # 실제 네이버 ID로 대체해야 합니다.
naver_pw = "dlglacks7!@!"  # 실제 비밀번호로 대체해야 합니다.
id_input = driver.find_element(By.ID, "id")
pw_input = driver.find_element(By.ID, "pw")

slow_type(id_input, naver_id)
slow_type(pw_input, naver_pw)

# 로그인 버튼 클릭
driver.find_element(By.ID, "log.login").click()
time.sleep(2)  # 로그인 처리 대기

# 엑셀 파일에서 픽업날짜 읽기
file_path = 'C:\\Python\\bill\\코반스 픽업요청서 양식.xlsx'
book = load_workbook(file_path)
sheet = book.active
pickup_date = sheet['K5'].value.strftime('%Y-%m-%d')

# 메일 작성 페이지로 이동
driver.find_element(By.CSS_SELECTOR, ".item.button_write").click()
time.sleep(2)  # 페이지 로딩 대기

# 받는 사람 이메일 주소 입력
driver.find_element(By.ID, "recipient_input_element").send_keys("s846464@naver.com")

# 제목 입력 (픽업날짜를 포함하여 제목 생성)
email_subject = f"{pickup_date} 삼성서울병원 픽업 문의드립니다."
driver.find_element(By.ID, "subject_title").send_keys(email_subject)

# 본문 내용 입력
content_area = driver.find_element(By.CSS_SELECTOR, ".workseditor-content")
content_area.click()
content_area.send_keys("연구 진행 위해 픽업 문의드립니다.")

# 이메일 전송 버튼 클릭
driver.find_element(By.CSS_SELECTOR, ".button_write_task").click()
