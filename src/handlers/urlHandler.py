from .baseHandler import BaseHandler
from src.store.multiModalStore import MultiModalStore
import time

class UrlHandler(BaseHandler):

    def __init__(self, db_name):
        self.db = MultiModalStore(db_name)

    def handle(self, url):
        pass
