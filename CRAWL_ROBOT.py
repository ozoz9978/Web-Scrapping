from selenium import webdriver
import time
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

# keyword = '화장품'
keyword = '화장품'

options = webdriver.ChromeOptions()
options.add_argument(r"--user-data-dir=C:\250529_NEW")
options.add_argument('--profile-directory=Default')
#user-data-dir > 구글에서 로봇방지문자가 안뜨게 됨 (CAPTCHA)

driver = webdriver.Chrome(options=options)

driver.get(f"https://www.google.com/search?q={keyword}")
time.sleep(2) # 3초 정도 대기

for scroll_i in range(1, 5):
    # driver.execute_script("window.scrollTo(0, 100)")
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
    time.sleep(0.5)

item_elements = driver.find_elements(By.CLASS_NAME, "MjjYud")[1:]
for item_index, item in enumerate(item_elements):
    try:
        if item.find_element(By.CLASS_NAME, "YzSd").text == '장소':
            continue
    except:
        pass
    try:
        if item.find_element(By.CLASS_NAME, "mgAbYb").text in ['관련 검색어', '이미지']:
            continue
    except:
        pass
    print(item_index, item.text)
input() #종료를 방지