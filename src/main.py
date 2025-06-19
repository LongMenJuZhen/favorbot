import os
import sys
from store.kvstore import db_set, db_get

if __name__ == '__main__':
    # 示例调用
    db_set("Website1", "https://zhuanlan.zhihu.com/p/637960746")

    print(db_get("Website1"))
