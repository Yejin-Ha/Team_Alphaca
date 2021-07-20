from elasticsearch import Elasticsearch
import pandas as pd
import datetime as dt
# import schedule
import time
import random


es = Elasticsearch(hosts='127.0.0.1:9200', http_compress=True)


def h_singer():
    body = {
        "query": {
            "match_all": {}
        }
    }
    res = es.search(index="hot_singer", body=body)
    # asdf = []
    return res['hits']['hits'][0]['_source']


def h_song():
    body = {
        "query": {
            "match_all": {}
        }
    }
    res = es.search(index="hot_song", body=body)
    return res['hits']['hits'][0]['_source']


def get_new_chart():
    # current = datetime.datetime.now()
    csv_data = []
    chart_details = []
    total_genre_lst = []

    query = {
        "query": {
            "match_all": {}
        }
    }

    res = es.search(index="melon_chart", body=query)
    length = res['hits']['total']['value']

    query = {
        "query": {
            "match_all": {}
        },
        "size": length,
        "sort": [
            {"convert_date": "asc"},
            {"rank": "asc"},
            "_score"
        ]
    }

    res = es.search(index="melon_chart", body=query)
    for i in range(length-100, length):
        row = []
        data = {}

        row.append(str(res['hits']['hits'][i]['_source']['date']))  # 0
        data['date'] = res['hits']['hits'][i]['_source']['date']
        row.append(int(res['hits']['hits'][i]['_source']['rank']))  # 1
        data['rank'] = res['hits']['hits'][i]['_source']['rank']
        row.append(str(res['hits']['hits'][i]['_source']['title']))  # 2
        data['title'] = res['hits']['hits'][i]['_source']['title']
        row.append(str(res['hits']['hits'][i]['_source']['artist']))  # 3
        data['artist'] = res['hits']['hits'][i]['_source']['artist']
        row.append(str(res['hits']['hits'][i]['_source']['album']))  # 4
        data['album'] = res['hits']['hits'][i]['_source']['album']
        row.append(int(res['hits']['hits'][i]['_source']['code']))  # 5
        data['code'] = res['hits']['hits'][i]['_source']['code']
        row.append(str(res['hits']['hits'][i]['_source']['release_date']))  # 6
        data['release_date'] = res['hits']['hits'][i]['_source']['release_date']
        tmp = str(res['hits']['hits'][i]['_source']['genre'])

        genre_lst = []
        if "_ " in tmp:
            genre_lst = tmp.split("_ ")
        else:
            genre_lst.append(tmp)

        for j in genre_lst:
            if j not in total_genre_lst:
                total_genre_lst.append(j)

        tmp.replace("인디음악", "")
        tmp.replace("국내드라마", "")
        tmp.strip(" ")
        tmp.strip("_")
        # print(tmp)
        row.append(tmp)  # 7
        data['genre'] = genre_lst
        row.append(int(res['hits']['hits'][i]['_source']['comment']))  # 8
        data['comment'] = res['hits']['hits'][i]['_source']['comment']
        row.append(int(res['hits']['hits'][i]['_source']['like']))  # 9
        data['like'] = res['hits']['hits'][i]['_source']['like']
        csv_data.append(row)
        # print(data)
        chart_details.append(data)

    headerlist = ["date", "rank", "title", "artist", "album",
                  "code", "release_date", "genre", "comment", "like"]
    # print(csv_data)
    file_name = "hourly_chart.csv"
    df = pd.DataFrame(csv_data)
    df2 = pd.DataFrame(csv_data, columns=headerlist)
    df.to_csv(file_name, index=False, mode='w',
              encoding='utf-8-sig', header=False)
    # print(chart_details)
    # print(total_genre_lst)
    return chart_details, total_genre_lst

def get_hot(self): # singer : 100개, song : 2400개
    
    current = dt.datetime.now()
    csv_data = []
    query = {
        "query": {
            "match_all": {}
        }
    }

    res = es.search(index="melon_chart", body=query)
    length = res['hits']['total']['value']

    query = {
        "query": {
            "match_all": {}
        },

        "size": length,

        "sort": [
            {"convert_date": "asc"},
            {"rank": "asc"},
            "_score"
        ]
    }

    res = es.search(index="melon_chart", body=query)
    for i in range(length-2500, length):
        row = []

        row.append(str(res['hits']['hits'][i]['_source']['date']))  # 0
        row.append(int(res['hits']['hits'][i]['_source']['rank']))  # 1
        row.append(str(res['hits']['hits'][i]['_source']['title']))  # 2
        row.append(str(res['hits']['hits'][i]['_source']['artist']))  # 3
        row.append(str(res['hits']['hits'][i]['_source']['album']))  # 4
        row.append(int(res['hits']['hits'][i]['_source']['code']))  # 5
        row.append(str(res['hits']['hits'][i]['_source']['release_date']))  # 6
        row.append(str(res['hits']['hits'][i]['_source']['genre'])) # 7
        row.append(int(res['hits']['hits'][i]['_source']['comment']))  # 8
        row.append(int(res['hits']['hits'][i]['_source']['like']))  # 9
        csv_data.append(row)
        # print(data)
    
    # print(len(csv_data)) # 2400개 

    headerlist = ["date", "rank", "title", "artist", "album",
                "code", "release_date", "genre", "comment", "like"]
    # print(csv_data)

    file_name = "hourly_chart.csv"

    df = pd.DataFrame(csv_data, columns=headerlist)
    df['date'] = pd.to_datetime(df.date, format='%Y-%m-%d-%H', errors='raise')
    df['release_date'] = pd.to_datetime(df.release_date, format='%Y.%m.%d', errors='raise')
    df['comment_1h_before'] = df.groupby('code').comment.shift().fillna(df.comment).astype('int')
    df['comment_1d_before'] = df.groupby('code').comment.shift(24).fillna(df.comment).astype('int')
    df['comment_1h_diff'] = (df.comment - df.comment_1h_before).astype('int')
    df['comment_1d_diff'] = (df.comment - df.comment_1d_before).astype('int')
    df['like_1h_before'] = (df.groupby('code').like.shift().fillna(df.like)).astype('int')
    df['like_1d_before'] = (df.groupby('code').like.shift(24).fillna(df.like)).astype('int')
    df['like_1h_diff'] = (df.like - df.like_1h_before).astype('int')
    df['like_1d_diff'] = (df.like - df.like_1d_before).astype('int')
    df['rank_1h_before'] = (df.groupby('code')['rank'].shift().fillna(df['rank'])).astype('int')
    df['rank_1d_before'] = (df.groupby('code')['rank'].shift(24).fillna(df['rank'])).astype('int')
    df['rank_1h_diff'] = (df['rank'] - df.rank_1h_before).astype('int')
    df['rank_1d_diff'] = (df['rank'] - df.rank_1d_before).astype('int')


    # 가장 최근의 날짜 (시간 포함) 데이터를 가져옴
    recent_date = df.date.max()
    # 최근 순위 100개의 데이터만 df로 생성
    data_recent = (
        df[df.date == recent_date]
    )
    # 오늘의 날짜를 받아와서 변수에 저장
    today = pd.to_datetime(dt.datetime.today()).strftime('%Y-%m-%d')
    # print((pd.to_datetime(today, format='%Y-%m-%d') - data_recent.release_date).apply(lambda x: x.components.days))
    data_recent.loc[:, 'duration'] = (
        (pd.to_datetime(today, format='%Y-%m-%d') - data_recent.release_date)
        .apply(lambda x: x.components.days)
    )

    # 인디음악을 컬럼으로 추가
    data_recent['indie'] = (
        data_recent['genre']
        .str
        .contains('인디음악')
    )
    # 국내드라마를 컬럼으로 추가
    data_recent['ko_drama'] = (
        data_recent['genre']
        .str
        .contains('국내드라마')
    )
    # replace
    data_recent.genre = (
        data_recent
        .genre
        .replace(['인디음악_', '_ 인디음악', '국내드라마_', '_ 국내드라마', ' '], '', regex=True)
    )
    genre = data_recent.groupby('genre').title.count().sort_values(ascending=False)
    genre_others = {'genre': '기타', 'title': genre[set(genre.index) - set(genre.head(5).index)].sum()}
    genre = genre[genre.head(5).index].to_frame().reset_index().append(genre_others, ignore_index=True).set_index('genre')

    # hot_song
    # print(data_recent[data_recent.like_1d_diff > 0])
    data_recent[data_recent.comment_1d_diff > 0][['title', 'artist', 'rank', 'rank_1d_before', 'rank_1d_diff', 'like', 'like_1d_before', 'like_1d_diff', 'comment', 'comment_1d_before', 'comment_1d_diff']].sort_values('comment_1d_diff', ascending=False).reset_index(drop=True).to_csv('./song/hot_song.csv', index=False, header=False)
    # hot_singer
    data_recent.artist.value_counts().reset_index().rename(columns = {'index' : 'artist', 'artist': 'count'}).to_csv('./singer/hot_singer.csv', index=False, header=False)
    # genre
    genre = data_recent.groupby('genre').title.count().sort_values(ascending=False)
    genre_others = {'genre': '기타', 'title': genre[set(genre.index) - set(genre.head(5).index)].sum()}
    genre = genre[genre.head(5).index].to_frame().reset_index().append(genre_others, ignore_index=True).set_index('genre')
    # data_recent.groupby('genre').title.count().to_csv('./genre_all.csv')
    # genre.to_csv('./genre.csv')
    # oldest
    oldest = data_recent[(data_recent.duration >= 730)].sort_values(by="duration")[['artist', 'title', 'duration']].reset_index(drop=True)
    oldest_result = oldest.iloc[random.choice(list(oldest.index))].to_dict()
    
    return oldest_result

if __name__ == '__main__':
    # print(get_new_chart())
    print(h_song())
