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

def kill_chrome():
    #KILL, TASKKILL / 프로세스를 종료하는 명령을 의미
    subprocess.call("TASKKILL /f /IM CHROME.EXE")
    subprocess.call("TASKKILL /f /IM CHROMEDRIVER.EXE")


def remove_tag(_input_data):
    # input_data = '@with_soooom2주좋아요 1개답글 달기'
    p = re.compile('@[a-zA-Z_]+')
    data = p.search(_input_data)
    if data is not None:
        tag_data = p.search(_input_data).group()
        output_data = _input_data.replace(tag_data, '')
        return output_data
    else:
        return _input_data
    #print(output_data)