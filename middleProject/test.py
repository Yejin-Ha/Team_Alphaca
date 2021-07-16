from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

class watermelon():

    def newest_list():
        main_url = "https://www.melon.com/"

        driver = webdriver.Chrome("c:/driver/chromedriver.exe")

        driver.get(main_url)
        print('1. Melon 접속 완료')
        time.sleep(3)

        driver.find_element_by_partial_link_text
        remove_ad = driver.find_element_by_css_selector("#mainPop > div > div.wrap_lower > div.fl_right > button")
        remove_ad.click()
        print('2. 광고팝업 제거 완료')
        time.sleep(3)

        newest = driver.find_element_by_link_text("최신 음악")
        newest.click()
        print('3. 최신차트 이동 완료')
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "lxml" )


        try:

            title = soup.select("div.ellipsis.rank01")
            # item = soup.select('div.ellipsis.rank02 > span.checkEllipsis')
            # level = boxitem.find_all("div",{"class": "wrap t_center"})
            # title = item.find("div",{"class":"ellipsis rank01"})
            # print("{}위".format(level))

            print("제목 = ",title)

        except Exception as e:
            print("page error : ", e)


        finally:
            print('크롤링을 종료합니다.')
            driver.close()

if __name__=='__main__':
    watermelon.newest_list()
