from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

class watermelon():

    def test():
        main_url = "https://www.melon.com/"
        results = []

        driver = webdriver.Chrome("c:/driver/chromedriver.exe")

        driver.get(main_url)
        time.sleep(3)
        driver.implicitly_wait(2)

        new = driver.find_element_by_class_name("menu_bg menu02 ")
        superchat = driver.find_element_by_link_text("최다 조회 영상")
        superchat.click()
        time.sleep(3)
        driver.implicitly_wait(2)
        print("-----스크롤 페이지 이동-----")


        # scroll 쭉 내리기, scroll 기다리는 시간 지정
        SCROLL_PAUSE_TIME = 0.7

        # Get scroll height : 브라우저의 높이를 찾아서 자바스크립트에 저장 후 last_height로 지정
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom : 브라우저 끝까지 스크롤을 내림
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # 스크롤 내려갈때까지 기다림
            time.sleep(SCROLL_PAUSE_TIME)

            # 스크롤이 끝까지 내려가면 break로 빠져나가고 아니면 while문 무한 반복
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height


            '''
            boxitems = soup.find("tbody").find_all("tr")
            for boxitem in boxitems:

                title = boxitem.select("td")[4].div.div.select('div')[0].a.text
                artist = boxitem.select("td")[4].div.div.select('div')[1].a.text
                img_title = boxitem.select("td")[2].div.a.attrs['title']
                print('곡 제목: ',title, ", 가수: ",artist)
                print("--" * 10)
            '''


        print("-----화면 제일 하단 스크롤 로딩 완료----")

        soup = BeautifulSoup(driver.page_source, "lxml" )

        # 정보박스 찾기
        boxitem = soup.select("tbody > .chart__row")
        # print(boxitem)
        print("-----스크롤 박스 찾기 완료-----")
        time.sleep(3)


        # 정보 가져오기
        try:
            # 광고는 text가 없어서 광고 없애려고 for문 씀
            for item in boxitem:
                noads = item.text

                if noads != "":
                    prolevel = item.find("div", {"class":"current"}).text
                    protitle = item.find("img")['alt']
                    protag = item.find("ul", {"class":"title__tags ttags"})
                    superchat = item.find("span", {"class":"fluc-label fluc-label--mono-font fluc-label--ko fluc-label--symbol-math up"}).text


                    protag = str(protag)
                    exp = re.compile('#\w+')
                    protag = exp.findall(protag)
                    tag = ", ".join(protag)

                    data = [prolevel, protitle, tag, superchat]
                    results.append(data)

                    print("No_{}".format(prolevel))
                    print("채널명 = ", protitle)
                    # for tag in protag:
                    print("태그 = ", tag)
                    print("조회수 = ", superchat)
                    # print("슈퍼챗 개수 = ", superchat_num)
                    print("=" * 100)


        except Exception as e:
            print("페이지 파싱 에러", e)

        finally:
            time.sleep(3)
            print("크롤링을 종료합니다.")
            driver.close()

            df = pd.DataFrame(results)
            df.columns = ['순위', '채널명', '태그', '조회수']

            # df.to_excel('C:/202105_lab/TEAM_ALPHACA/middleProject/dataset/test.xlsx', index = False)
            df.to_csv('C:/202105_lab/TEAM_ALPHACA/middleProject/dataset/test.xlsx', index = False)
            print("---------crawling file save 완료------------")

if __name__=='__main__':
    watermelon.test()