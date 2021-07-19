from os import name
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

def newest_list():
    main_url = "https://www.melon.com/chart/week/index.htm"
    driver = webdriver.Chrome("c:/driver/chromedriver.exe")
    driver.get(main_url)
    print('1. Melon 주간 차트 접속 완료')
    time.sleep(1)

    try:
        btn = driver.find_element_by_xpath('/html/body/div/div[3]/div/div/div[3]/div/button')
        btn.click()

        test = BeautifulSoup(driver.page_source, "lxml")
        weeks = test.find(class_="time_layer").div.dl.dd.table.tbody.find_all('tr')
        
        for week in weeks:
            print(week.attrs['class'])
            # week.attrs['class']
            if week.attrs['class'][0] != 'end':
                bt = week.select("td")[4]
                bt.click()
                time.sleep(1)

    except Exception as e:
        print("page error : ", e)
    finally:
        print('크롤링을 종료합니다.')
        driver.close()

if __name__ == '__main__':
    newest_list()


'''
날짜 두 개는 힘들듯

주제 : 
'''