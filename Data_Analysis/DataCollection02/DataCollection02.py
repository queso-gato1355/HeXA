from selenium import webdriver
from selenium.webdriver.common.by import By

import time
import pandas as pd
import os

driver = webdriver.Chrome("chromedriver.exe")
driver.implicitly_wait(3)

# 상품들 페이지 열기

site = "http://www.yes24.com/24/Category/Display/001001009002"
driver.get(site)
time.sleep(1)

# 상품 페이지의 리스트 부분을 FruitList에 넣기

FruitList = driver.find_element(By.ID, 'clearfix')

FruitList.find_element(By.XPATH, './li['+'1'+']').find_element(By.CLASS_NAME,'baby-product-link').get_attribute("href")

i = 1
links = []
while True:
    try:
        temp = FruitList.find_element(By.XPATH, './li['+str(i)+']')
        link = temp.find_element(By.CLASS_NAME,'baby-product-link').get_attribute("href")
        links.append(link)
        i+=1
    except:
        break

print("전체 저장된 링크의 수 : %d"%len(links))
print("처음에 저장된 링크 : %s"%links[-1])

driver.get(links[0])

driver.find_element(By.NAME, 'review').click()
time.sleep(3)

review = driver.find_element(By.CLASS_NAME, "js_reviewArticleListContainer")

i=0 # i는 현재까지 저장된 리뷰의 수를 의미
j=0 # j는 보여지는 리뷰들의 순서와 관련
data = []
while True:
    i += 1
    j += 1
    try:    # 리뷰 평점 저장
        data.append(review.find_element(By.XPATH, "./article["+str(j)+"]/div[1]/div[3]/div[1]/div").get_attribute("data-rating"))
    except: # 보여지는 리뷰들을 다 불러와서 그 이후의 리뷰가 없어 에러가 나면 실행 - 다음 리뷰들을 띄운다
        j = 0
        page = driver.find_element(By.XPATH, "/html/body/div[2]/section/div[2]/div[7]/ul[2]/li[3]/div/div[6]/section[4]/div[3]")
        p = int(page.get_attribute("data-page"))%10+2
        page.find_element(By.XPATH, "./button["+str(p)+"]").click()
        time.sleep(3)
    if i >= 10:
        break

for i in links:
    driver.get(i)
    time.sleep(2)   # 페이지 이동 시에 완전히 로딩되지 않았음에도 되는 경우 방지용 3초 대기
    
    title = driver.find_element(By.CLASS_NAME, "prod-buy-header__title").text # 상품명 저장
    
    driver.find_element(By.NAME, 'review').click()
    time.sleep(2)
    review = driver.find_element(By.CLASS_NAME, "js_reviewArticleListContainer")

    i=0 # i는 현재까지 저장된 리뷰의 수를 의미
    j=0 # j는 보여지는 리뷰들의 순서와 관련
    score = []

    while True:
        i += 1
        j += 1
        try:    # 리뷰 평점 저장
            score.append(review.find_element(By.XPATH, "./article["+str(j)+"]/div[1]/div[3]/div[1]/div").get_attribute("data-rating"))
        except: # 보여지는 리뷰들을 다 불러와서 그 이후의 리뷰가 없어 에러가 나면 실행 - 다음 리뷰들을 띄운다
            j = 0
            try:
                page = driver.find_element(By.XPATH, "/html/body/div[2]/section/div[2]/div[7]/ul[2]/li[3]/div/div[6]/section[4]/div[3]")
                p = int(page.get_attribute("data-page"))%10+2
                page.find_element(By.XPATH, "./button["+str(p)+"]").click()
                time.sleep(1)
            except:
                break        
        if i >= 10:
            break
        
    dic = {"review-score": score}
    df = pd.DataFrame(dic)
    df.to_csv(os.getcwd()+"\\"+title+'.csv', index=False, encoding='utf-8-sig')
    print(title+" 저장 완료")

driver.quit()