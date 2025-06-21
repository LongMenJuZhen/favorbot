from .baseHandler import BaseHandler
from src.store.multiModalStore import MultiModalStore
from src.llmClient.urlResolveClient import UrlResolveClient
from datetime import datetime

class UrlHandler(BaseHandler):

    def __init__(self, db_name):
        self.db = MultiModalStore(db_name)

    def handle(self, url):
        client = UrlResolveClient()
        messages = [
            {"role": "user", "content": f"{url}"}
        ]

        # 测试大模型调用
        resp = client.call(messages)

        dic = {
            'record_id':'',
            'content':url,
            'desc':resp,
            'create_time':datetime.now(),
            'type':'url',
            'class':'',
            'extra':''
        }

        self.db.store.insert(dic)
