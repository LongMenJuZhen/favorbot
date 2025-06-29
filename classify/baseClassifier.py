from abc import ABC, abstractmethod

class BaseClassifier(ABC):
    @abstractmethod
    def single_obj_classify(self, desc: str, classes: list) -> list:
        """根据描述内容对单个对象进行分类

        参数:
            desc: 待分类对象的描述文本
            classes: 候选分类列表，每个分类包含类名和描述
                    示例: [{"class": "book", "desc": "喜欢的书"}, ...]

        返回:
            分类结果列表，按相关性排序，包含类名和匹配分数
            示例: [{"class": "book", "score": 0.9}, ...]

        注意:
            - 实现类应确保返回结果按分数降序排列
            - 分数应在0.0到1.0范围内，1.0表示完全匹配
        """
        pass