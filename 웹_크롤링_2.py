# # 구글에서 블루투스 스피커를 검색했을 때 다나와 항목 가져오기
# import requests
# search_word='블루투스 스피커'
# r = requests.get('http://www.google.co.kr/search?q='+search_word)
# print(r.text)
# from selenium import webdriver
# from bs4 import BeautifulSoup
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
#
# driver_filepath='./chromedriver_v78.exe'
# search_word='블루투스 스피커'
# service = Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service)
#
# driver.get('http://www.google.co.kr/search?q='+search_word) #url접속
#
# input('대기')
# soup = BeautifulSoup(driver.page_source, 'lxml') #lxml 컴파일러로 html코드를 분석
# item=soup.find('div',{'class':'MjjYud'})
# print(item.text)
# driver.quit()

# 네이버로 접속해서 검색결과 안의 세부 링크로 접속해 안의 내용 가져오기
# from selenium import webdriver
# from bs4 import BeautifulSoup
# search_word='블루투스 스피커'
# # keyword_list=['화장품','감자','고구마']
#
# driver=webdriver.Chrome()
# driver.get(f"https://search.naver.com/search.naver?query={search_word}&ssc=tab.blog.all")
#
# soup = BeautifulSoup(driver.page_source, 'lxml') #lxml 컴파일러로 html코드를 분석
# list_view_item=soup.find("div","api_subject_bx").find("ul","lst_view")
# item=list_view_item.find('div','view_wrap').find('div','title_area').find('a')
# print(item['href'])

# # 네이버로 접속해서 검색결과 안의 모든 링크 가져오기
# from selenium import webdriver
# from bs4 import BeautifulSoup
#
# search_word='블루투스 스피커'
# # keyword_list=['화장품','감자','고구마']
#
# driver=webdriver.Chrome()
# driver.get(f"https://search.naver.com/search.naver?query={search_word}&ssc=tab.blog.all")
#
# soup = BeautifulSoup(driver.page_source, 'lxml') #lxml 컴파일러로 html코드를 분석
#
# lst_view_item = soup.find("ul", "lst_view") #class
# item = lst_view_item.find_all("div", "view_wrap")
# print(len(item))
# for row in item:
#     link = row.find("div", "title_area").find("a")['href']
#     print(link)


# 네이버로 접속해서 검색결과 안의 모든 내용 가져오고 csv 파일로 저장하기
# from selenium import webdriver
# from bs4 import BeautifulSoup
# from selenium.webdriver.common.by import By
#
# search_word='블루투스 스피커'
# # keyword_list=['화장품','감자','고구마']
#
# driver=webdriver.Chrome()
# driver.get(f"https://search.naver.com/search.naver?query={search_word}&ssc=tab.blog.all")
#
# soup = BeautifulSoup(driver.page_source, 'lxml') #lxml 컴파일러로 html코드를 분석
# lst_view_item = soup.find("ul", "lst_view") #class
# item = lst_view_item.find_all("div", "view_wrap")
# # print(len(item))
# link_list = []
#
# for row in item:
#     link = row.find("div", "title_area").find("a")['href']
#     #print(link)블루투스스피커
#     link_list.append(link)
#
# link_i = 1
# blog_content_list = []
#
# for link in link_list:
#     driver.get(link)
#     driver.switch_to.frame(driver.find_element(By.TAG_NAME, "iframe"))
#     blog_content = driver.find_element(By.CLASS_NAME, "se-main-container").text
#     blog_content = blog_content.replace("\n", "").replace(",", "")
#     link_i += 1
#     blog_content_list.append(blog_content)
#     if link_i > 5:
#         print("5회까지만 수집 ")
#         break
#
# #cp949
# with open(f"{search_word}.csv", 'w', newline='', encoding='utf8') as csvfile:
#     for blog_content in blog_content_list:
#         try:
#             csvfile.write(blog_content+"\n")
#         except Exception as e:
#             print("38", str(e))

# # 네이버 카페의 특정 게시물에 있는 글을 크롤링하라, 그리고 저장까지 해보기
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time
#
# keyword="올리브영"
# url = f"https://cafe.naver.com/f-e/cafes/10050813/menus/0?viewType=L&ta=SUBJECT&q={keyword}&page=1"
#
# print(url)
# driver = webdriver.Chrome()
# driver.get(url)
# time.sleep(2)
#
# ##
# article_table_element = driver.find_element(By.CLASS_NAME,"article-table")
# title_list=article_table_element.find_element(By.TAG_NAME,"tbody").find_elements(By.CLASS_NAME,"inner_list")
#
# csv_title_list = []
# for title_element in title_list:
#     title = title_element.find_element(By.CLASS_NAME, "article").text
#     csv_title_list.append(title)
#
# with open("title.csv", "w") as fw: #w: write.
#     for csv_title in csv_title_list:
#         try:
#             fw.write(csv_title + "\n")
#         except:
#             print("ERROR code-27LINE", csv_title)

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

keyword="미국"
url=f'https://cafe.naver.com/f-e/cafes/17178299/menus/0?viewType=L&page=1&ta=SUBJECT&q={keyword}'
print(url)

driver= webdriver.Chrome()
driver.get(url)
time.sleep(2)

article_row=driver.find_element(By.CLASS_NAME,"article-table") #큰 글 통 찾고
article_list=article_row.find_element(By.TAG_NAME,"tbody").find_elements(By.CLASS_NAME,"inner_list") # 반복되는 줄 통 찾고

csv_file=[]
for article in article_list: #실제 내용있는 걸 찍자
    article1=article.find_element(By.CLASS_NAME,"article").text
    csv_file.append(article1)
with open("title.csv", "w") as fw: #w: write.
    for csv1 in csv_file:
        try:
            fw.write(csv1 + "\n")
        except:
            print("ERROR code-27LINE", csv1)
