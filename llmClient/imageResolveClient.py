import base64
import os
from openai import OpenAI
# 使用相对导入
from .baseClient import BaseClient
from pathlib import Path

# 定义方法将指定路径图片转为Base64编码
def encode_image(image_path):
    try:
        with open(Path(image_path), "rb") as image_file:
            print("成功打开文件！")
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"错误详情: {repr(e)}")
        return None


class ImageResolveClient(BaseClient):

    def __init__(self, model='doubao-seed-1.6-250615'):
        self.model = model
        self.client = OpenAI(
            # 从环境变量中读取您的方舟API Key
            api_key=os.environ.get("ARK_API_KEY"),
            base_url="https://ark.cn-beijing.volces.com/api/v3",
        )


    def call(self, messages):
        completion = self.client.chat.completions.create(
            # 将推理接入点 <Model>替换为 Model ID
            model=self.model,
            messages=messages
        )

        return completion.choices[0].message.content