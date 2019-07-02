"""
封装ElasticSearch搜索引擎的SDK(library库)
"""
import requests
import pymysql
from pymysql.cursors import DictCursor
from dao import DB


class ESearch():
    def __init__(self, index):
        self.host = '121.199.63.71'
        self.port = '9204'
        self.index = index

    def create_index(self):
        url = f'http://{self.host}:{self.port}/{self.index}'
        # ES基于json数据进行交互的，所以上传数据必须是json格式的数据
        # resp是请求响应对象， 通过resp.json()获取响应的json数据
        resp = requests.put(url, json={
            "settings": {
                "number_of_shards": 5,
                "number_of_replicas": 1
            }
        })
        resp_data = resp.json()
        print(resp_data)
        if resp_data.get('acknowledged'):
            print('create index %s ok!' % self.index)

    def remove_index(self):
        url = f'http://{self.host}:{self.port}/{self.index}'
        requests.delete(url)


    def add_doc(self, doc_type, id=None, **values):
        url = f'http://{self.host}:{self.port}/{self.index}/{doc_type}/'
        if id:
            url += f"{id}"
        resp = requests.post(url, json=values)
        resp_data = resp.json()
        print(resp_data)
        if resp_data.get('result') == "created":
            print('add doc %s ok!' % values)
        else:
            print('add doc %s error!' % values)

    def query(self, keyword):
        url = f'http://{self.host}:{self.port}/{self.index}/_search?q={keyword}'
        resp = requests.get(url)
        resp_data = resp.json()
        if resp_data.get('hits').get('total') > 0:
            return {
                'code': 200,
                'total': resp_data.get('hits').get('total'),
                'datas': [data.get('_source')
                          for data in resp_data.get('hits').get('hits')
                          ]
            }
        else:
            return {'code': 201, 'msg': '无'}


def init_index():

    # 连接数据库，将doctors表数据添加到索引库中
    db = pymysql.Connect(host="121.199.63.71",
                         port=3306,
                         user='eduadmin',
                         password='edu7654',
                         db='edu_api_db',charset='utf8')
    with db.cursor(cursor=DictCursor) as c:
        c.execute('select course_id, name, img_url, description, degree, price, study_num from courses')

        es_ = ESearch('eduindex')
        es_.create_index()
        for row_data in c.fetchall():
            print(row_data)
            es_.add_doc('doctor', **row_data)

        print('--init add edu doc_type all ok--')


if __name__ == '__main__':
    # init_index()
    search = ESearch('eduindex')
    # search.remove_index()
    print(search.query('python'))