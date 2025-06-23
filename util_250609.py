import mysql.connector
import subprocess
import re

# MySQL 서버 연결 정보
host = '127.0.0.1'
database = 'a'
user = 'root'
password = '1234'

# MySQL 서버에 연결
conn = mysql.connector.connect(host=host, database=database, user=user, password=password)

# 커서 생성
cursor = conn.cursor()

def util_250609_stop_words(_input_data):
    with open(r"C:\Users\305-16\Desktop\coupang_stopwords.txt", encoding='utf8') as fr:
        stopwords = [row.strip() for row in fr.readlines()]
        new_stopwords = stopwords[0].split(',')

    # 입력이 리스트인 경우 그대로 사용, 문자열이면 split()
    if isinstance(_input_data, str):
        _input_data = _input_data.split()

    output_data = [word for word in _input_data if word not in new_stopwords]
    return output_data


def kill_chrome():
    #KILL, TASKKILL / 프로세스를 종료하는 명령을 의미
    subprocess.call("TASKKILL /f /IM CHROME.EXE")
    subprocess.call("TASKKILL /f /IM CHROMEDRIVER.EXE")


def remove_tag(_input_data):
    # input_data = '@with_soooom2주좋아요 1개답글 달기'
    # _input_data = '@with_soooom @dfdfc @dgccgcg 2주좋아요 1개답글 달기'
    p = re.compile('@[a-zA-Z0-9_]+')
    data = p.search(_input_data)
    if data is not None:
        tag_data = p.findall(_input_data)
        output_data = _input_data
        for tag in tag_data:
            output_data = output_data.replace(tag, '')
        return output_data.strip()
    else:
        return _input_data
    #print(output_data)