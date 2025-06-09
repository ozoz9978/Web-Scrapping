from selenium import webdriver
from selenium.webdriver.common.by import By
from util_250609 import *
import time
import re

kill_chrome()
### 크롬창이 전부 닫히기 때문에 주의 ###
### CTRL + SHIFT + T > 닫힌 창을 복구하는 명령어

account = "sinsaimdang.official"

url = f"https://www.instagram.com/{account}/reels"
folder_name = r"C:\250604_INSTAGRAM"

options = webdriver.ChromeOptions()
options.add_argument(r"--user-data-dir=" + folder_name)
options.add_argument('--profile-directory=Default')

driver = webdriver.Chrome(options=options)
driver.get(url)

time.sleep(5)

###############################

a_tag_elements = driver.find_elements(By.TAG_NAME, "a")

p = re.compile("https://www.instagram.com/sinsaimdang.official/reel/[a-zA-Z0-9-_]+/")

for a_tag in a_tag_elements:
    link = a_tag.get_attribute('href')
    if p.match(link) is not None:
        print(link)
    # if link == "https://www.instagram.com/sinsaimdang.official/reel/DKD1WIOPVsR/":
    #     a_tag.click()
    #     time.sleep(5)
    #     break

driver.get("https://www.instagram.com/sinsaimdang.official/reel/DKD1WIOPVsR/")
time.sleep(5) #5초 정도 웹페이지가 로딩되는 시간을 기다림

try:
    comment_elements = driver.find_element(By.CLASS_NAME, "_a9z6")
except Exception as e44:
    print(str(e44))
    #NoSuchElementException / 특정 element(요소)를 찾지 못해서 생기는 에러

# print(comment_elements.text)
#DEBUG Variables / driver.find_element(By.CLASS_NAME, "_aasi").find_element(By.XPATH, '..').text

review_element = comment_elements.find_elements(By.CLASS_NAME, "_a9zr")

review_list = []
for review_index, review in enumerate(review_element):
    date_time = review.find_element(By.TAG_NAME, "time").get_attribute("datetime")[:-5]
    writer = review.find_element(By.CLASS_NAME, "xjp7ctv").text
    print(review_index+1, review.text+"\n\n")
    review_text = review.text.strip()[:500]
    review_text = review_text.replace(writer, "").strip().replace("\n", "")
    review_text = remove_tag(review_text)
    #remove_tag() > 사용자가 직접 정의한 함수
    insert_tuple = (review_text, writer, date_time)
    review_list.append(insert_tuple)

query = "INSERT INTO instagram_table (comment, writer, date) VALUES (%s, %s, %s)"

for review_tuple in review_list:
    # insert_data = (review_text[:500],)
    try:
        cursor.execute(query, review_tuple)
    except mysql.connector.errors.IntegrityError:
        print("중복값 제외")

# 변경 사항 커밋
conn.commit()