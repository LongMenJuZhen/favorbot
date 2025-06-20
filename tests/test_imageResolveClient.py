import unittest

from src.llmClient.imageResolveClient import ImageResolveClient

class TestImageResolveClient(unittest.TestCase):
    def setUp(self):
        self.client = ImageResolveClient()

    def test_call(self):
        messages = [
            {
                # 消息角色为用户
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        # 第一张图片链接及细节设置为 high
                        "image_url": {
                            # 您可以替换图片链接为您的实际图片链接
                            "url": "https://ark-project.tos-cn-beijing.volces.com/doc_image/ark_demo_img_1.png",
                            "detail": "high"
                        }
                    },
                    # 文本类型的消息内容，询问图片里有什么
                    {"type": "text", "text": "图片里有什么？"},
                ],
            }
        ]

        # 测试大模型调用
        resp = self.client.call(messages)
        print(resp)
        self.assertIsInstance(resp, str, "返回结果应该是字符串")