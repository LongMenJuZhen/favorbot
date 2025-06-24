import unittest
import json

from src.classify.easyClassifier import EasyClassifier
from src.store.kvstore import KVStore

class TestEasyClassifier(unittest.TestCase):
    def setUp(self):
        self.classifier = EasyClassifier()
        self.kv_store = KVStore("kvstore.txt")


    def test_classify(self):
        desc = "文章通过性能对比、功能特性和官方优势的梳理，突出Qdrant作为向量数据库在性能、灵活性、易用性和扩展性上的竞争力，适合需要高效向量检索（如RAG、多模态应用）的场景。"
        classes = json.loads(self.kv_store.db_get("classes"))
        # 分类效果
        resp = self.classifier.single_obj_classify(desc, classes)
        print(resp)
        self.assertIsInstance(resp, list, "返回结果应该是评分列表")