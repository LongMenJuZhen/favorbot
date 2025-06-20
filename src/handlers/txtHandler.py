from .baseHandler import BaseHandler
from src.store.multiModalStore import MultiModalStore
from datetime import datetime

class TXTHandler(BaseHandler):
    def __init__(self, db_name):
        self.db = MultiModalStore(db_name)

    def handle(self, s):
        dic = {
            'record_id':'',
            'content':s,
            'desc':s,
            'create_time':datetime.now(),
            'type':'text',
            'class':'',
            'extra':''
        }

        self.db.store.insert(dic)