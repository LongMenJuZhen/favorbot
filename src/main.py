import os
import sys
from store.kvstore import KVStore
from llmClient.doubaoClient import DoubaoClient

if __name__ == '__main__':
    kvstore = KVStore('kvstore.txt')

    # 示例调用
    kvstore.db_set("Website1", "https://zhuanlan.zhihu.com/p/637960746")

    print(kvstore.db_get("Website1"))

    client = DoubaoClient()
    messages = [
        {"role": "user", "content": "你好"}
    ]

    # 测试大模型调用
    resp = client.call(messages)
    print(resp)


