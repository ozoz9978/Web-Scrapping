#유튜브 댓글을 크롤링 하기
import mysql.connector
import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver

# # MySQL 서버 연결 정보
host = '127.0.0.1'
database = 'a'
user = 'root'
password = '1234'
#
# # MySQL 서버에 연결
conn = mysql.connector.connect(host=host, database=database, user=user, password=password)

# 커서 생성
cursor = conn.cursor()
#
# 데이터 삽입 쿼리 작성
query = ("INSERT INTO you_tube (comment,url) VALUES (%s, %s)" )

with open(r"C:\Users\305-16\Desktop\youtube_link.txt") as fr:
    url_list = [row.strip() for row in fr.readlines()]

# url_list=['https://www.youtube.com/shorts/33yjhnLGewo']
for url in url_list:

    driver=webdriver.Chrome()
    driver.get(url)

    #웹페이지가 다 로딩될 수 있도록 기다리기
    time.sleep(1)

    # driver.find_element(By.CLASS_NAME,"yt-spec-button-shape-next").click()
    element=driver.find_element(By.ID,"comments-button").find_element(By.CLASS_NAME,"yt-spec-button-shape-next")
    driver.execute_script("arguments[0].click();", element)
    time.sleep(1)
    comment_elements=driver.find_elements(By.ID,"contents")[1]

    #화면 끝까지 스크롤하기
    for i in range(1,80):
        comment_elements.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)

    comment_text_list=[]

    comment_elements=comment_elements.find_elements(By.ID,"content-text")
    for comment_element in comment_elements:
        comment=comment_element.text
        comment_text_list.append(comment)

        insert_data = (comment,url)
        try:
            cursor.execute(query, insert_data)
        except mysql.connector.errors.IntegrityError:
            print("중복값 제외")


# 변경 사항 커밋
conn.commit()
# 연결 종료
conn.close()