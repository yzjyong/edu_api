# 封装ElasticSearch搜索引擎的库
import requests


class ESearch():
    def __init__(self,index):
        self.host = 'localhost'
        self.port = '9200'
        self.index = index

    def create_index(self):
        url = f'http://{self.host}:{self.port}/{self.index}'
        # ES基于json数据进行交互的，所以上传数据必须时json格式的数据
        # resp时请求响应对象，通过resp.json()获取相应的json数据
        resp = requests.put(url,json={
            'settings':{
                "number_of_shards":5,
                "number_of_replicas":1
            }
        })
        resp_data = resp.json()
        print(resp_data)
        if resp_data.get('acknowledged'):
            print("create index %s ok!" % self.index)

    def add_doc(self,doc_type,id=None,**values):
        url = f'http://{self.host}:{self.port}/{self.index}/{doc_type}'
        if id:
            url += f'{id}'
        resp = requests.post(url,json=values)
        resp_data = resp.json()


    def query(self,keyword):
        pass