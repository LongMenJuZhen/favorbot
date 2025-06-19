import os
from openai import OpenAI
# 使用相对导入
from .baseClient import BaseClient

class DoubaoClient(BaseClient):

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
            messages=messages,
            extra_body={
                "thinking": {
                    "type": "disabled"  # 不使用深度思考能力
                    # "type": "enabled" # 使用深度思考能力
                    # "type": "auto" # 模型自行判断是否使用深度思考能力
                }
            },
        )

        return completion.choices[0].message.content

# if __name__ == '__main__':
#     client = DoubaoClient()
#     messages = [
#         {"role": "user", "content": "你好"}
#     ]
#     print(client.call(messages))