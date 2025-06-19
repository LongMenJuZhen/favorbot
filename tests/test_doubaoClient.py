import unittest

from src.llmClient.doubaoClient import DoubaoClient

class TestDoubaoClient(unittest.TestCase):
    def setUp(self):
        self.client = DoubaoClient()

    def test_call(self):
        messages = [
            {"role": "user", "content": "你好"}
        ]

        # 测试大模型调用
        resp = self.client.call(messages)
        self.assertIsInstance(resp, str, "返回结果应该是字符串")