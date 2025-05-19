# from selenium import webdriver
# from bs4 import BeautifulSoup
# from selenium.webdriver.common.by import By
# from urllib import parse
# import time
#
# keyword = '감자'
#
# url = "https://cafe.naver.com/tlsxh?iframe_url=/ArticleSearchList.nhn%3Fsearch.clubid=25257486"
#
# driver = webdriver.Chrome()
# driver.get(url)
#
# time.sleep(2)
#
# driver.switch_to.frame(driver.find_element(By.ID, "cafe_main"))
#
# keyinput_element = driver.find_element(By.ID, "queryTop")
# keyinput_element.send_keys(keyword+"\n")
#
# time.sleep(2)
# input()
#
#
#
#
#
#
# from selenium import webdriver
# from bs4 import BeautifulSoup
# from selenium.webdriver.common.by import By
# from urllib import parse
# import time
#
# keyword = '감자'
# url = f"https://cafe.naver.com/ArticleSearchList.nhn?search.clubid=25257486&search.searchBy=0&search.query={keyword}"
#
# url = parse.urlparse(url)
#
# query = parse.parse_qs(url.query)
# result = parse.urlencode(query, doseq=True)
# result = "https://cafe.naver.com/ArticleSearchList.nhn?" + result
# print(result)
# driver = webdriver.Chrome()
# driver.get(result)
#
#
# time.sleep(2)
#
# article_table_element = driver.find_element(By.CLASS_NAME, "article-table")
# title_list = article_table_element.find_element(By.TAG_NAME, "tbody").find_elements(By.CLASS_NAME, "inner_list")
#
# for title_element in title_list:
#     print(title_element.find_element(By.CLASS_NAME, "article").text)
# input()
#
#
#
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time
#
# keyword = '올리브영'
# url = f"https://cafe.naver.com/f-e/cafes/10050813/menus/0?ta=SUBJECT&q={keyword}&page=1"
#
# print(url)
# driver = webdriver.Chrome()
# driver.get(url)
#
# time.sleep(2)
#
# article_table_element = driver.find_element(By.CLASS_NAME, "article-table")
# title_list = article_table_element.find_element(By.TAG_NAME, "tbody").find_elements(By.CLASS_NAME, "inner_list")
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