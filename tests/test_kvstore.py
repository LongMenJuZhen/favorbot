import unittest
import os
from store.kvstore import KVStore

class TestKVStore(unittest.TestCase):
    def setUp(self):
        self.kvstore = KVStore('test_kvstore.txt')

    def test_db_set_and_get(self):
        # 测试 db_set 和 db_get 函数
        key = 'Website1'
        value = 'https://zhuanlan.zhihu.com/p/637960746'

        # 设置键值对
        self.kvstore.db_set(key, value)

        # 获取键值对
        result = self.kvstore.db_get(key)

        # 验证结果
        self.assertEqual(result, value)

    def tearDown(self):
        # 清理测试文件
        if os.path.exists(self.kvstore.db_file_path):
            os.remove(self.kvstore.db_file_path)

if __name__ == '__main__':
    unittest.main()