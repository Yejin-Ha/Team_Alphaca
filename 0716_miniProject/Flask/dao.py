from datetime import datetime
from elasticsearch import Elasticsearch

# es = Elasticsearch()


def bank_get2():
    es = Elasticsearch()

    res = es.search(index="bank", body={"query": { "match": { "bank": "국민은행" }}, "size": 0, "aggs": { "b_1": {"terms": { "field": "customers"}}}})
    datas = res['aggregations']['b_1']['buckets']
    return datas

    