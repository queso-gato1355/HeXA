from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json


GETRESTNUM = 10

driver=webdriver.Chrome("./chromedriver.exe")
driver.implicitly_wait(10)
wait = WebDriverWait(driver, 5)

address = '울산광역시 울주군 언양읍 반연리 378'
url = 'https://www.yogiyo.co.kr/mobile/#/'

driver.get(url)
action = ActionChains(driver)

time.sleep(2)
elem = driver.find_element(By.NAME, "address_input")
elem.click()
elem.send_keys(Keys.CONTROL + "A")
elem.send_keys(address)

wait = WebDriverWait(driver, 5)

current_URL = driver.current_url
while current_URL == url:
    driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div/div[2]/div/span[2]/button[2]').click()
    current_URL = driver.current_url

base_url = driver.current_url

restaurant_num = 1
gether_restarurant = []

# 리뷰 수집
while True:
    
    if len(gether_restarurant) == GETRESTNUM:
        break
    try:
        print("==================================================================")
        time.sleep(1)
        current_url = driver.current_url
        each_restaurant = driver.find_element(By.XPATH, '/html/body/div[6]/div/div[4]/div/div[2]/div[{}]/div/table/tbody/tr/td[2]/div/div[1]'.format(restaurant_num))
        restaurant_name = each_restaurant.get_attribute("title")
        
        each_restaurant.click()
        
        time.sleep(1)
        
        review_num = int(driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/div[1]/ul/li[2]/a/span').text)
        
        print("trial", restaurant_num, " - ", restaurant_name, " -> ", review_num, "개")
        
        driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/div[1]/ul/li[2]/a').click()
        
        time.sleep(0.5)
        
        if review_num > 10:
            
            buffer = {"restaurant_name" : restaurant_name, "restaurant_review" : []}
            print("조건 부합 -> 10개 이상의 리뷰")
            
            for r_num in range(1, review_num + 1 if review_num <= 100 else 101):
                print("|", end = '')
                time.sleep(0.2)
                review_content = driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/div[1]/div[5]/ul/li[{}]'.format(r_num + 1))
                try:
                    next_button = review_content.find_element(By.XPATH, "./a/span")
                    next_button.click()
                    time.sleep(0.5)
                    review_content = driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/div[1]/div[5]/ul/li[{}]'.format(r_num + 1))
                except:
                    pass
                
                try:
                    who_rated = review_content.find_element(By.XPATH, './div[1]/span[1]').text
                    who_rated = who_rated[:len(who_rated) - 1]
                except:
                    who_rated = "Anomynous"
                
                try:
                    taste_rating = int(review_content.find_element(By.XPATH, './div[2]/div/span[2]/span[3]').text)
                except:
                    taste_rating = None
                
                try:
                    quantity_rating = int(review_content.find_element(By.XPATH, './div[2]/div/span[2]/span[6]').text)
                except:
                    quantity_rating = None
                
                try:
                    delivery_rating = int(review_content.find_element(By.XPATH, './div[2]/div/span[2]/span[9]').text)
                except:
                    delivery_rating = None
                    
                try:
                    what_ordered = review_content.find_element(By.XPATH, './div[3]').text
                except:
                    what_ordered = None
                
                try:
                    what_said = review_content.find_element(By.XPATH, './p').text
                except:
                    what_said = None

                buffer["restaurant_review"].append({"taste_rating" : taste_rating,
                                                    "quantity_rating" : quantity_rating,
                                                    "delivery_rating" : delivery_rating,
                                                    "user_name" : who_rated,
                                                    "menu_ordered" : what_ordered,
                                                    "review_content" : what_said})
                    
            gether_restarurant.append(buffer)
            print("")
        else:
            print("조건 미부합 -> 10개 미만의 리뷰")
        driver.back()
    
    except:
        print(f"trial {restaurant_num} : {restaurant_name} - 식당 정보를 찾을 수 없음.")
        driver.get(base_url)
        print("넘어갑니다.")
        time.sleep(1)
        
    restaurant_num += 1
        
        
with open("ulju_review.json", 'w') as f:
    json.dump(gether_restarurant, f, indent = 4)