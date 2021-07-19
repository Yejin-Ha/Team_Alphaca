from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import csv, requests
import pandas as pd

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
    try:
        boxitems = mainsoup.find("tbody").find_all("tr")
        for boxitem in boxitems:
            rank = boxitems.index(boxitem) + 1
            title = boxitem.select("td")[3].div.div.select("div")[0].a.text
            artist = boxitem.select("td")[3].div.div.select("div")[1].a.text
            album = boxitem.select("td")[4].div.div.select("div")[0].a.text
            like = boxitem.select("td")[5].div.button.find(class_='cnt').get_text(strip=True)[3:]
            song_info = boxitem.attrs["data-song-no"]
            img_addr = boxitem.select("td")[1].div.a.img["src"]

            info_url = "https://www.melon.com/song/detail.htm?songId=" + \
                str(song_info)

            driver.get(info_url)

            time.sleep(2)

            detailsoup = BeautifulSoup(driver.page_source, "lxml")
            detail_info = detailsoup.find(class_="meta")

            # 세부정보
            date = detail_info.dl.select("dd")[1].text
            genre = detail_info.dl.select("dd")[2].text
            driver.back()

            print('-' * 60)
            print("순위 : {}위".format(rank))
            print("곡 제목 : ", title)
            print("아티스트 : ", artist)
            print('앨범명 : ', album)
            print("발매일 : ", date)
            print("장르 : ", genre)
            print("좋아요 수 : ", like)
            print("고유번호 : ", song_info)
            print("이미지 주소 : ", img_addr)
            
    except Exception as e:
        print("page error : ", e)
    finally:
        print('크롤링을 종료합니다.')
        driver.close()


if __name__ == '__main__':
    newest_list()
    