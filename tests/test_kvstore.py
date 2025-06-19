import unittest
import os
import sys

# 执行路径(使用时改成自己的src路径)
sys.path.insert(0, '/Users/rain/Project/favorbot/src')
from store.kvstore import db_set, db_get

class TestKVStore(unittest.TestCase):
    def setUp(self):
        # 初始化测试文件路径
        self.test_file = 'data/test_kvstore.txt'
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_db_set_and_get(self):
        # 测试 db_set 和 db_get 函数
        key = 'Website1'
        value = 'https://zhuanlan.zhihu.com/p/637960746'

        # 设置键值对
        db_set(key, value)

        # 获取键值对
        result = db_get(key)

        # 验证结果
        self.assertEqual(result, value)

    def tearDown(self):
        # 清理测试文件
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

if __name__ == '__main__':
    unittest.main()