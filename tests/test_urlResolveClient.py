import unittest

from llmClient.urlResolveClient import UrlResolveClient

class TestDoubaoClient(unittest.TestCase):
    def setUp(self):
        self.client = UrlResolveClient()

    def test_call(self):
        messages = [
            {"role": "user", "content": "https://zhuanlan.zhihu.com/p/637960746"}
        ]

        # 测试大模型调用
        resp = self.client.call(messages)
        print(resp)
        self.assertIsInstance(resp, str, "返回结果应该是字符串")