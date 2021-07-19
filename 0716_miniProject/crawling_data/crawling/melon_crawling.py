from selenium import webdriver
from bs4 import BeautifulSoup
import csv, requests
import pandas as pd
import time
import os

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

    csv_data = []
    today_date = time.strftime('%Y-%m-%d-%H', time.localtime(time.time()))
    
    try:
        boxitems = mainsoup.find("tbody").find_all("tr")
        for boxitem in boxitems:
            row = []

            rank = boxitems.index(boxitem) + 1
            title = boxitem.select("td")[3].div.div.select("div")[0].a.text
            title = title.replace(",", "")
            print(title, type(title))
            artist = boxitem.select("td")[3].div.div.select("div")[1].a.text
            artist = artist.replace(",", "")
            album = boxitem.select("td")[4].div.div.select("div")[0].a.text
            album = album.replace(",", "")
            song_info = boxitem.attrs["data-song-no"]
            img_addr = boxitem.select("td")[1].div.a.img["src"]
            info_url = "https://www.melon.com/song/detail.htm?songId=" + \
                str(song_info)
            driver.get(info_url)
            time.sleep(3)
            detailsoup = BeautifulSoup(driver.page_source, "lxml")
            detail_info = detailsoup.find(class_="meta")
            # 세부정보
            date = detail_info.dl.select("dd")[1].text
            genre = detail_info.dl.select("dd")[2].text
            genre = genre.replace(",", '_')
            
            comment_info = detailsoup.find(class_="share").find("dl")
            comment = comment_info.dd.find("span").text
            comment = comment.replace(",", "")
            comment = comment.replace("개","")
            # print(comment)

            like = boxitem.select("td")[5].div.button.find(class_='cnt').get_text(strip=True)[3:]
            like = like.replace(",", "")
            # print(like)

            row.append(today_date)
            row.append(int(rank))
            row.append(str(title))
            row.append(str(artist))
            row.append(str(album))
            row.append(int(song_info))
            row.append(date)
            row.append(str(genre))
            row.append(int(comment))
            row.append(int(like))
            driver.back()

            print(row)
            csv_data.append(row)

    except Exception as e:
        print("page error : ", e)
    
    finally:
        print('크롤링을 종료합니다.')
        driver.close()

    file_name = "24hit_chart.csv"
    headerlist = ["date", "rank", "title", "artist", "album", "code", "release_date", "genre", "comment", "like"]
    
    
    if not os.path.exists(file_name):
        # df = pd.DataFrame(csv_data, columns=headerlist)
        df = pd.DataFrame(csv_data)
        # df.to_csv(file_name, index=False, mode='w', encoding='utf-8-sig', header=True)
        df.to_csv(file_name, index=False, mode='w', encoding='utf-8-sig', header=False)
        
    else:
        df = pd.DataFrame(csv_data)
        df.to_csv(file_name, index=False, mode='a', encoding='utf-8-sig', header=False)

if __name__ == '__main__':
    newest_list()