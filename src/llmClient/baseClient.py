from abc import ABC, abstractmethod

class BaseClient(ABC):
    """大模型客户端接口类"""

    # messages = [
    #     {"role": "system", "content": "你是豆包，是由字节跳动开发的 AI 人工智能助手"},
    #     {"role": "user", "content": "常见的十字花科植物有哪些？"},
    # ]
    @abstractmethod
    def call(self, messages):
        pass