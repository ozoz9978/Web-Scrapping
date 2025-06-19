import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
from util_250609 import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


kill_chrome()
options = uc.ChromeOptions()

# 팝업 차단을 활성화합니다.
folder_name = r"C:\Users\305-16\AppData\Local\Google\Chrome\User Data"
options.add_argument('--disable-popup-blocking')

# WebDriver 객체 생성
driver = uc.Chrome(options=options,enable_cdp_events=True)
wait = WebDriverWait(driver, 10)

# 대기 시간 설정 =&gt; 대기 시간을 설정하여, html이 렌더링 되는 시간을 벌어줍니다.
driver.implicitly_wait(2)

# 자바스크립트 코드 실행
driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")

url = "https://www.coupang.com"
driver.get(url)
time.sleep(3)

driver.find_element(By.NAME, "q").send_keys("동국제약")
time.sleep(3)
# url = "https://www.coupang.com/vp/products/7809503814?itemId=21179352814&vendorItemId=91178339108"
url= "https://www.coupang.com/vp/products/7809503814?itemId=21417932893&vendorItemId=91309090230"
driver.get(url)

# 스크롤을 전부 내려야 리뷰에 대한 element가 생성
page_index = 1
page_start_no = 1
insert_query = "INSERT INTO donguk_review (review_text, review_headline, review_user, review_score, review_date, review_seller, review_product_name) VALUES (%s, %s, %s, %s, %s, %s, %s)"

for loop_i in range(1, 100):
    review_list = []
    next_page = str(page_index + 1)
    clicked = False

    #루프 시작 시 이전 리뷰 첫줄 저장
    try:
        prev_text = driver.find_element(By.CLASS_NAME, "js_reviewArticleListContainer") \
                          .find_element(By.TAG_NAME, "article").text.strip()
    except:
        prev_text = ""

    # 🔹 페이지 번호 목록 확인
    page_elements = driver.find_elements(By.CLASS_NAME, "sdp-review__article__page__num")
    page_numbers = [elem.text.strip() for elem in page_elements]

    # 🔸 다음 세트로 넘겨야 할 경우
    if next_page not in page_numbers:
        try:
            print(f"🔄 다음 페이지 세트로 넘김 (현재 페이지 {page_index})")
            next_set_btn = driver.find_element(By.CLASS_NAME, "sdp-review__article__page__next--active")
            driver.execute_script("arguments[0].click();", next_set_btn)
            time.sleep(2)
        except:
            print(f"❌ 페이지 {next_page} 번호도 없고, 다음 묶음 버튼도 없음. 종료")
            break

    # 🔹 번호 클릭
    page_elements = driver.find_elements(By.CLASS_NAME, "sdp-review__article__page__num")
    for elem in page_elements:
        if elem.text.strip() == next_page:
            driver.execute_script("arguments[0].click();", elem)
            clicked = True
            break

    if not clicked:
        print(f"❌ 페이지 {next_page} 클릭 실패. 종료")
        break

    # 🔽 스크롤 유도
    try:
        container = driver.find_element(By.CLASS_NAME, "js_reviewArticleListContainer")
        driver.execute_script("arguments[0].scrollIntoView();", container)
    except:
        pass
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    # 리뷰 유무 확인
    item_elements = driver.find_elements(By.TAG_NAME, "article")
    if len(item_elements) == 0:
        print(f"❌ 페이지 {page_index}는 리뷰 없음. 종료")
        break

    # 리뷰 변경 대기
    try:
        wait.until(lambda d: d.find_element(By.CLASS_NAME, "js_reviewArticleListContainer")
                   .find_element(By.TAG_NAME, "article").text.strip() != prev_text)
    except TimeoutException:
        print("⚠️ 리뷰 내용 변경 안됨: 이전 페이지 그대로일 가능성 높음")
        break

    # 리뷰 수집
    item_elements = driver.find_element(By.CLASS_NAME, "js_reviewArticleListContainer").find_elements(By.TAG_NAME,
                                                                                                      "article")
    for review_index, item_element in enumerate(item_elements, start=1):
        try:
            review_text = item_element.find_element(By.CLASS_NAME, "sdp-review__article__list__review__content").text
            review_text_cleaned = " ".join(review_text.split())
        except:
            review_text_cleaned = ""
        try:
            review_head_line = item_element.find_element(By.CLASS_NAME, "sdp-review__article__list__headline").text
            review_head_line_cleaned = " ".join(review_head_line.split())
        except:
            review_head_line_cleaned = ""
        try:
            review_user = item_element.find_element(By.CLASS_NAME, "sdp-review__article__list__info__user__name").text
            review_score = int(item_element.find_element(By.CLASS_NAME,
                                                         "sdp-review__article__list__info__product-info__star-orange").get_attribute(
                "data-rating"))
            review_date = item_element.find_element(By.CLASS_NAME,
                                                    "sdp-review__article__list__info__product-info__reg-date").text
            review_seller = item_element.find_element(By.CLASS_NAME,
                                                      "sdp-review__article__list__info__product-info__seller_name").text
            review_product_name = item_element.find_element(By.CLASS_NAME,
                                                            "sdp-review__article__list__info__product-info__name").text
            print(f'페이지 {page_index}_리뷰 번호 {review_index}', review_text_cleaned[:100], review_user, review_score,
                  review_date, review_seller, review_product_name)
            review_list.append(
                (review_text_cleaned[:600], review_head_line_cleaned[:600], review_user, review_score, review_date,
                 review_seller, review_product_name))
        except Exception as e:
            print("118LINE", str(e))

    # DB 저장
    for review in review_list:
        try:
            cursor.execute(insert_query, review)
        except mysql.connector.errors.IntegrityError:
            print("중복값 제외")

    conn.commit()
    page_index += 1