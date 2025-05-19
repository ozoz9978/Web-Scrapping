# 1. 웹 페이지에 있는 html 소스 코드 읽어오기
# 웹 페이지의 소스코드 ctrl u
import requests
r=requests.get("http://ip.pe.kr/")
html_code=r.text
print(r.text)
#html코드 가져오는 간단화 코드 1
html_code_list=html_code.split("\n") #띄어쓰기를 기준으로 잘라 list 형태로 웹페이지 소스코드 저장
i = 1
for line in html_code_list:
    print(i, line)
    i += 1
    if line.find("<h1 class=\"cover-heading\">") >= 0:
        found_line = line.strip()
        break

print("found_line", found_line)

# 원래 코드
for line in html_code_list:
   if line.find("<h1 class=\"cover-heading\">") >= 0:
       found_line=line.strip()
       break
found_line2=found_line[found_line.find(">")+1:]
print(found_line2)
found_line3=found_line2[:found_line2.find("<")]
print(found_line3)

# request와 beautifulsoup html, xml 활용해서 가져오기
import requests
from bs4 import BeautifulSoup
r=requests.get("http://ip.pe.kr/")
html_code=r.text

soup=BeautifulSoup(html_code, "lxml")#lxml 파서로 soup에 저장
ip_tag=soup.find("h1",{"class":"cover-heading"})
print(ip_tag.text)

# 중복되는 태그가 있을 때 구별해서 가져오는 법
import requests
from bs4 import BeautifulSoup
r=requests.get("http://ip.pe.kr/")
html_code=r.text
print(html_code)

soup=BeautifulSoup(html_code, "lxml")#lxml 파서로 soup에 저장
ip_tag=soup.find_all("a",{"class":"nav-link"})
print(ip_tag)
print(ip_tag[3].text)
