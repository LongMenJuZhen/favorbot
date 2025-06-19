import os
from pathlib import Path


class KVStore:
    def __init__(self, db_file):
        # 使用相对于项目根目录的路径
        self.data_dir = Path(__file__).parent.parent.parent / 'data'
        self.data_dir.mkdir(exist_ok=True)  # 确保目录存在
        self.db_file_path = self.data_dir / db_file

    def db_set(self, key, value):
        try:
            # 读取现有的键值对
            kv_pairs = {}
            if os.path.exists(self.db_file_path):
                with open(self.db_file_path, 'r', encoding='utf-8') as file:
                    for line in file:
                        k, v = line.strip().split('=', 1)
                        kv_pairs[k] = v

            # 更新或添加键值对
            kv_pairs[key] = value

            # 将更新后的键值对写回文件
            with open(self.db_file_path, 'w', encoding='utf-8') as file:
                for k, v in kv_pairs.items():
                    file.write(f'{k}={v}\n')
            return True
        except Exception as e:
            print(f'设置键值对时出错: {e}')
            return False


    def db_get(self, key):
        try:
            if os.path.exists(self.db_file_path):
                with open(self.db_file_path, 'r', encoding='utf-8') as file:
                    for line in file:
                        k, v = line.strip().split('=', 1)
                        if k == key:
                            return v
            return None
        except Exception as e:
            print(f'获取键值对时出错: {e}')
            return None
