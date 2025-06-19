import re
import mysql.connector
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np
from nltk import Text, FreqDist
from konlpy.tag import Komoran
from util_250609 import *
from PIL import Image

komoran = Komoran(userdic='./coupang_my_dict.txt')

# MySQL 서버 연결 정보
host = '127.0.0.1'
database = 'a'
user = 'root'
password = '1234'

# MySQL 서버에 연결
conn = mysql.connector.connect(host=host, database=database, user=user, password=password)

# 커서 생성
cursor = conn.cursor()

wc_max_words = 50
data_count = 500
query = f"SELECT review_text, review_headline FROM donguk_review LIMIT {data_count}"

cursor.execute(query)
rows = cursor.fetchall()

content_one = ''
content_two = ''
content_combine = ''
content_combine_wc4 = ''

for row in rows:
    try:
        noun_value1 = komoran.nouns(row[0])
        content_one += row[0] + ''

        noun_value2 = komoran.nouns(row[1])
        content_two += row[1] + ''

        text_combine = str(row[0]) + '' + str(row[1])
        noun_value3 = komoran.nouns(text_combine)
        content_combine += text_combine + ''

        #wc4 / morphs
        noun_value4 = komoran.morphs(text_combine)
        content_combine_wc4 += text_combine + ''
    except Exception as e:        ## 인코딩 관련 에러 발생시 에러이유 및 댓글 print
        print(str(e), text_combine)

def clean_text(text):
    # 이모지 및 특수 유니코드 제거
    emoji_pattern = re.compile(
        "[" 
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        u"\U00002700-\U000027BF"
        u"\U0000FE00-\U0000FE0F"
        u"\U0001F900-\U0001F9FF"
        u"\U0001FA70-\U0001FAFF"
        u"\U0001F3FB-\U0001F3FF"
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub('', text)

def strip_invalid_chars(text):
    # 인코딩 오류 발생할 수 있는 문자 제거
    return text.encode("utf-8", "ignore").decode("utf-8", "ignore")

# 이모지 및 깨진 문자 제거
content_one = clean_text(content_one)
content_one = strip_invalid_chars(content_one)
noun_value_list1 = komoran.nouns(content_one)

content_two = clean_text(content_two)
content_two = strip_invalid_chars(content_two)
noun_value_list2 = komoran.nouns(content_two)

content_combine = clean_text(content_combine)
content_combine = strip_invalid_chars(content_combine)
noun_value_list3 = komoran.nouns(content_combine)

content_combine_wc4 = clean_text(content_combine_wc4)
content_combine_wc4 = strip_invalid_chars(content_combine_wc4)
noun_value_list4 = komoran.morphs(content_combine_wc4)

#content_row1
noun_value1 = komoran.nouns(content_one)
noun_value1 = util_250609_stop_words(noun_value1)
fd_names1 = FreqDist(noun_value1)
print("분석 단어 개수", fd_names1.N())
print("빈도수 많은 단어 순위",fd_names1.most_common(50))

#content_row2

noun_value2 = komoran.nouns(content_two)
noun_value2 = util_250609_stop_words(noun_value2)
fd_names2 = FreqDist(noun_value2)
print("분석 단어 개수", fd_names2.N())
print("빈도수 많은 단어 순위",fd_names2.most_common(50))

#content combine
noun_value3 = komoran.nouns(content_combine)
noun_value3 = util_250609_stop_words(noun_value3)
fd_names3 = FreqDist(noun_value3)
print("분석 단어 개수", fd_names3.N())
print("빈도수 많은 단어 순위",fd_names3.most_common(50))

#content combine / MORPHS
noun_value4 = komoran.morphs(content_combine_wc4)
noun_value4 = util_250609_stop_words(noun_value4)
fd_names4 = FreqDist(noun_value4)
print("분석 단어 개수", fd_names4.N())
print("빈도수 많은 단어 순위",fd_names4.most_common(50))


#동일한 설정들을 반복해서 쓰고 싶을 때 딕셔너리에 담아두고 **를 사용
image_mask = np.array(Image.open('images (2).jpg'))
wc_config = dict(font_path=r'C:\Users\305-16\NanumGothicCoding.ttf',
width=600, height=300, background_color="white",colormap="Wistia",
               random_state=0, max_words=wc_max_words, mask=image_mask
            )

# 워드클라우드 생성
wc = WordCloud(**wc_config)
wordcloud_img = wc.generate_from_frequencies(fd_names1)

# 각 워드클라우드에 사용할 FreqDist와 제목 목록
fd_list = [fd_names1, fd_names2, fd_names3, fd_names4]
titles = [
    f'[NOUN] REVIEW HEADLINE DATA CNT: {data_count} / W: {wc_max_words}',
    f'[NOUN] REVIEW TEXT DATA CNT: {data_count} / W: {wc_max_words}',
    f'[NOUN] HEADLINE + REVIEW DATA CNT: {data_count} / W: {wc_max_words}',
    f'[MORPHS] HEADLINE + REVIEW DATA CNT: {data_count} / W: {wc_max_words}'
]

# 워드클라우드 루프 출력
for i in range(4):
    wc = WordCloud(**wc_config)
    wordcloud_img = wc.generate_from_frequencies(fd_list[i])

    plt.figure(figsize=(50, 10))
    plt.imshow(wordcloud_img, interpolation='bilinear')
    plt.axis("off")
    plt.title(titles[i], fontsize=14)
    plt.show()