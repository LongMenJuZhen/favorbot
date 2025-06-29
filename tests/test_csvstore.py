import unittest
import os
from store.csvstore import CSVStore  # 假设CSVStore类在csvstore模块中


class TestCSVStore(unittest.TestCase):
    def setUp(self):
        """每个测试方法前执行，创建测试文件"""
        self.test_file = 'test_csvstore.csv'
        self.fieldnames = ['id', 'name', 'email']
        self.store = CSVStore(
            filepath=self.test_file,
            fieldnames=self.fieldnames,
            auto_create=True
        )

    def test_insert_and_read(self):
        """测试插入和读取功能"""
        # 测试数据
        test_data = {
            'id': '1',
            'name': 'Alice',
            'email': 'alice@example.com'
        }

        # 插入数据
        self.store.insert(test_data)

        # 读取所有数据
        all_data = self.store.read_all()

        # 验证
        self.assertEqual(len(all_data), 1)
        self.assertDictEqual(all_data[0], test_data)

    def test_insert_many(self):
        """测试批量插入功能"""
        # 测试数据
        test_data = [
            {'id': '1', 'name': 'Alice', 'email': 'alice@example.com'},
            {'id': '2', 'name': 'Bob', 'email': 'bob@example.com'},
            {'id': '3', 'name': 'Charlie', 'email': 'charlie@example.com'}
        ]

        # 批量插入
        self.store.insert_many(test_data)

        # 读取验证
        all_data = self.store.read_all()
        self.assertEqual(len(all_data), 3)
        self.assertListEqual(all_data, test_data)

    def test_find(self):
        """测试条件查询功能"""
        # 准备测试数据
        test_data = [
            {'id': '1', 'name': 'Alice', 'email': 'alice@example.com'},
            {'id': '2', 'name': 'Bob', 'email': 'bob@example.com'},
            {'id': '3', 'name': 'Alice', 'email': 'alice2@example.com'}
        ]
        self.store.insert_many(test_data)

        # 查询name为Alice的记录
        results = self.store.find({'name': 'Alice'})

        # 验证
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['id'], '1')
        self.assertEqual(results[1]['id'], '3')

    def test_update(self):
        """测试更新功能"""
        # 准备测试数据
        test_data = [
            {'id': '1', 'name': 'Alice', 'email': 'alice@example.com'},
            {'id': '2', 'name': 'Bob', 'email': 'bob@example.com'}
        ]
        self.store.insert_many(test_data)

        # 更新Alice的邮箱
        updated_count = self.store.update(
            {'name': 'Alice'},
            {'email': 'alice.new@example.com'}
        )

        # 验证更新计数
        self.assertEqual(updated_count, 1)

        # 验证更新结果
        alice = self.store.find({'name': 'Alice'})[0]
        self.assertEqual(alice['email'], 'alice.new@example.com')

    def test_delete(self):
        """测试删除功能"""
        # 准备测试数据
        test_data = [
            {'id': '1', 'name': 'Alice', 'email': 'alice@example.com'},
            {'id': '2', 'name': 'Bob', 'email': 'bob@example.com'},
            {'id': '3', 'name': 'Charlie', 'email': 'charlie@example.com'}
        ]
        self.store.insert_many(test_data)

        # 删除Bob的记录
        deleted_count = self.store.delete({'name': 'Bob'})

        # 验证删除计数
        self.assertEqual(deleted_count, 1)

        # 验证剩余记录
        remaining = self.store.read_all()
        self.assertEqual(len(remaining), 2)
        self.assertEqual(remaining[0]['name'], 'Alice')
        self.assertEqual(remaining[1]['name'], 'Charlie')

    def test_count(self):
        """测试计数功能"""
        # 初始应为空
        self.assertEqual(self.store.count(), 0)

        # 插入3条记录
        test_data = [
            {'id': '1', 'name': 'Alice', 'email': 'alice@example.com'},
            {'id': '2', 'name': 'Bob', 'email': 'bob@example.com'},
            {'id': '3', 'name': 'Charlie', 'email': 'charlie@example.com'}
        ]
        self.store.insert_many(test_data)

        # 验证计数
        self.assertEqual(self.store.count(), 3)

    def test_clear(self):
        """测试清空功能"""
        # 插入一些数据
        test_data = [
            {'id': '1', 'name': 'Alice', 'email': 'alice@example.com'},
            {'id': '2', 'name': 'Bob', 'email': 'bob@example.com'}
        ]
        self.store.insert_many(test_data)

        # 清空
        self.store.clear()

        # 验证
        self.assertEqual(self.store.count(), 0)
        self.assertEqual(len(self.store.read_all()), 0)
        # 验证字段名仍然存在
        self.assertListEqual(self.store.fieldnames, self.fieldnames)

    def tearDown(self):
        """每个测试方法后执行，清理测试文件"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)


if __name__ == '__main__':
    unittest.main()