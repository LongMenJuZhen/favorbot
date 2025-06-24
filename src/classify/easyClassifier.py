import json

from .baseClassifier import BaseClassifier
from src.llmClient.doubaoClient import DoubaoClient

class EasyClassifier(BaseClassifier):
    def __init__(self):
        self.client = DoubaoClient()

    def single_obj_classify(self, desc: str, classes: list) -> list:
        messages = [
            {
                "role": "user",
                "content": f"# 角色定位"
                           f"你是一个文本分类专家，请根据我提供给你的类别列表，返回该文本的分类结果"
                           f"# 工作流程"
                           "1.理解提供给你的分类列表，格式为[{'class': 'book', 'desc': '喜欢的书'}, ...]，class代表类别名，desc代表类别描述"
                           "2.分析提供的文本，在分类列表中找出最相关的分类"
                           "3.严格按照以下json格式输出，分类结果列表，按相关性降序排序，包含类名和匹配分数 示例: [{'class': 'book', 'score': 0.9}, ...]"
                           "- class: 类别列表中的类名"
                           "- score: 文本和分类的相关性评分，分数应在0.0到1.0范围内，1.0表示完全匹配"
                           "# 类别列表"
                           f"{classes}"
                           f"# 待分类文本"
                           f"{desc}"
            }
        ]

        resp = json.loads(self.client.call(messages))

        return resp



