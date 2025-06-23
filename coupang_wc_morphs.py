from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from nltk import Text, FreqDist
from konlpy.tag import Komoran
from util_250609 import *
from PIL import Image

###word cloud###
# 형태소 분석은 불용어처리하지 않기

plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

komoran = Komoran(userdic='./coupang_my_dict.txt')

# query = "SELECT * FROM donguk_review"
wc_max_words = 20
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
        noun_value1 = komoran.pos(row[0])
        content_one += row[0] + ''
    except Exception as e:        ## 인코딩 관련 에러 발생시 에러이유 및 댓글 print
        print(str(e), row[0])

#content_row1
morph_list = komoran.pos(content_one)
morph_dict = {"MM": [], "NNP": [], "NNG": [], "JKB": [], "VA": [], "SN": [], "VV": [],
              "EC": [], "MAG": [], "ETM": [], "EP": [], "EF": [], "SF": [], "JX": [],
              "JKO": [], "NNB": [], "XSV": [], "JKG": [], "XSN": [], "JKS": [], "NP": [],
              "SW": [], "JC": [], "VCP": [], "VX": [], "MAJ": [], "VCN": [], "XR": [],
              "XSA": [], "ETN": [], "SP": [], "NR": [], "SL": [], "XPN": [], "NA": [],
              "SS": [], "SO": [], "JKQ": [], "IC": [], "SE": []}

for row in morph_list:
    try:
        morph_dict[row[1]].append(row[0])
    except Exception as e:
        print(str(e))


#동일한 설정들을 반복해서 쓰고 싶을 때 딕셔너리에 담아두고 **를 사용
image_mask = np.array(Image.open('images (2).jpg'))
wc_config = dict(font_path=r'C:\Users\305-16\NanumGothicCoding.ttf',
width=600, height=300, background_color="white",colormap="Wistia",
               random_state=0, max_words=wc_max_words, mask=image_mask
            )

wc_1 = WordCloud(wc_config)

fig, axes = plt.subplots(5, 8, figsize=(20, 10)) # 1행 3열로 워드클라우드 배치, 전체 그림 크기 지정

index = 0
row = 0
for key, value in morph_dict.items():
    fd_names1 = FreqDist(value)

    try:
        axes[row][index].imshow(wc_1.generate_from_frequencies(fd_names1), interpolation='bilinear')
    except Exception as e:
        print(str(e))
    axes[row][index].set_title(f'[{key}] CNT {data_count} WORDS: {wc_max_words}')
    axes[row][index].axis("off") # 축 표시 끄기
    index += 1
    if index > 7:
        row += 1
        index = 0


### 빈도를 설정해서 워드클라우드로 보여주는 코드
plt.tight_layout() # 제목이나 라벨이 겹치지 않도록 레이아웃 자동 조정
plt.show()