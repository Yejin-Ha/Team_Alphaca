from selenium import webdriver
from bs4 import BeautifulSoup
import csv, requests
import pandas as pd
import time
import os
import re

def newest_list():
    main_url = "https://www.melon.com/"
    driver = webdriver.Chrome("c:/driver/chromedriver.exe")
    driver.get(main_url)
    print('1. Melon 접속 완료')
    time.sleep(3)
    remove_ad = driver.find_element_by_css_selector(
        "#mainPop > div > div.wrap_lower > div.fl_right > button")
    remove_ad.click()
    print('2. 광고팝업 제거 완료')
    time.sleep(3)
    newest = driver.find_element_by_link_text("멜론차트")
    newest.click()
    print('3. 멜론차트 이동 완료')
    time.sleep(2)
    mainsoup = BeautifulSoup(driver.page_source, "lxml")

    today_date = time.strftime('%Y-%m-%d-%H', time.localtime(time.time()))
    
    try:
        boxitems = mainsoup.find("tbody").find_all("tr")
        all_lyrics = []
        for boxitem in boxitems:

            song_info = boxitem.attrs["data-song-no"]
            info_url = "https://www.melon.com/song/detail.htm?songId=" + \
                str(song_info)
            driver.get(info_url)
            time.sleep(1)
            open = driver.find_element_by_css_selector("#lyricArea > button")
            open.click()
            time.sleep(3)

            detailsoup = BeautifulSoup(driver.page_source, "lxml")

            lyrics = detailsoup.find(class_="lyric on")
            lyrics = str(lyrics)
            lyrics = lyrics.replace('<br/>', ' ')
            lyrics = re.sub(r'<.*?>', '', lyrics)
            lyrics = lyrics.replace('\t', '')
            lyrics = lyrics.replace(',', '')

            driver.back()

            lyrics = str(lyrics)
            lyrics = lyrics.strip()
            all_lyrics.append(lyrics)

    except Exception as e:
        print("page error : ", e)
    
    finally:
        print('크롤링을 종료합니다.')
        driver.close()

        lyric_file = "24hit_lyrics.csv"
        df = pd.DataFrame(all_lyrics)
        df.to_csv('C:/Team_Alphaca/0716_miniProject/crawling_data/datasets/{}'.format(lyric_file), index=False, encoding='utf-8-sig', header=False)
    
if __name__ == '__main__':
    newest_list()