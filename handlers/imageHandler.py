import os

from .baseHandler import BaseHandler
from store.multiModalStore import MultiModalStore
from llmClient.imageResolveClient import ImageResolveClient, encode_image
from datetime import datetime

class ImageHandler(BaseHandler):
    def __init__(self, db_name):
        self.db = MultiModalStore(db_name)


    def handle(self, image_path):
        client = ImageResolveClient()

        # 将图片转为Base64编码
        base64_image = encode_image(image_path)
        # 获取图片格式
        file_ext = os.path.splitext(image_path)[1][1:]

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            # 需要注意：传入Base64编码前需要增加前缀 data:image/{图片格式};base64,{Base64编码}：
                            # PNG图片："url":  f"data:image/png;base64,{base64_image}"
                            # JPEG图片："url":  f"data:image/jpeg;base64,{base64_image}"
                            # WEBP图片："url":  f"data:image/webp;base64,{base64_image}"
                            "url": f"data:image/{file_ext};base64,{base64_image}"
                        },
                    },
                    {
                        "type": "text",
                        "text": "图片里讲了什么?",
                    },
                ],
            }
        ]

        resp = client.call(messages)

        dic = {
            'record_id':'',
            'content':image_path,
            'desc':resp,
            'create_time':datetime.now(),
            'type':'image',
            'class':'',
            'extra':''
        }

        self.db.store.insert(dic)

        return resp
