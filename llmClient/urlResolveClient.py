import os
from openai import OpenAI
# 使用相对导入
from .baseClient import BaseClient

class UrlResolveClient(BaseClient):

    def __init__(self, model='bot-20250620105000-q6bk9'):
        self.model = model
        self.client = OpenAI(
            # 从环境变量中读取您的方舟API Key
            api_key=os.environ.get("ARK_API_KEY"),
            base_url="https://ark.cn-beijing.volces.com/api/v3/bots",
        )

    def call(self, messages):
        completion = self.client.chat.completions.create(
            # 将推理接入点 <Model>替换为 Model ID
            model=self.model,
            messages=messages
        )

        return completion.choices[0].message.content