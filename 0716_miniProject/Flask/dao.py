from datetime import datetime
from elasticsearch import Elasticsearch
import pandas as pd

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
    es = Elasticsearch(hosts='127.0.0.1:9200', http_compress=True)

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


if __name__ == '__main__':
    # print(get_new_chart())
    print(h_song())
