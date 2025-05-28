import os
import mysql.connector
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from nltk import Text, FreqDist
from nltk import RegexpTokenizer
from nltk.tag import pos_tag
import nltk
from scipy.signal import freqs
from konlpy.tag import Komoran

komoran = Komoran(userdic='my_dict.txt')
# MySQL 서버 연결 정보
# komoran = Komoran()
host = '127.0.0.1'
database = 'a'
user = 'root'
password = '1234'

# MySQL 서버에 연결
conn = mysql.connector.connect(host=host, database=database, user=user, password=password)

# 커서 생성
cursor = conn.cursor()

# 데이터 삽입 쿼리 작성
query = "SELECT comment FROM you_tube"

cursor.execute(query)

rows = cursor.fetchall()
# print(rows)     # 전체 rows

content = ''

noun_value_list=[]

for row in rows:
    try :
        nouns = komoran.nouns(row[0])
        noun_value_list.extend(nouns)
        # noun_value = komoran.nouns(content)

    except Exception as e:
        print(str(e),row[0])
        pass

# noun_value=komoran.nouns(content)


# emma_raw = content
# retokenize = RegexpTokenizer(r'\w+')
#
# emma_tokens = pos_tag(retokenize.tokenize(emma_raw))
with open(r"C:\Users\305-16\Desktop\youtube_stopwords.txt", encoding='utf8') as fr:
    stopwords = [row.strip() for row in fr.readlines()]
    new_stopwords = stopwords[0].split(',')
#
# stop_words = ['카드','신용카드','카드는','카드를','신용카드는','카드가','카드를','카드로','입니다','수','다','그리고','있습니다','ㅎㅎ','ㅋㅋ','이','그','안','ㅠㅠ','더','그냥']

# names_list = [t[0] for t in emma_tokens if t[1]=="NNP" and t[0] not in stopwords]


for noun in noun_value_list:
    noun=noun.replace("신용카드",'신카')
    noun_value_list.append(noun)
    if noun in new_stopwords:
        noun_value_list.remove(noun)

fd_names=FreqDist(noun_value_list)
# # check_word = "의사"
# print("분석 단어 개수", fd_names.N())
# # print(f"단어 출현 횟수 {fd_names[check_word]}")
# # print(f"단어 확률 {fd_names.freq(check_word)}")
print("빈도수 많은 단어 순위",fd_names.most_common(50))


plt.rcParams['font.family'] ='Malgun Gothic'
text = Text(noun_value_list)
text.plot(20)

# plt.xticks(rotation=0)

plt.show()



from wordcloud import WordCloud
# image_mask=np.array(Image.open("hana1.png"))
wc = WordCloud(font_path=r'C:\Users\305-16\NanumGothicCoding.ttf',width=1000, height=600,background_color="white",random_state=0,max_words=50)
plt.figure(figsize=(15,15))
plt.imshow(wc.generate_from_frequencies(fd_names))
plt.axis("off")
plt.show()