import os

DB_FILE = 'data/kvstore.txt'


def db_set(key, value):
    try:
        # 读取现有的键值对
        kv_pairs = {}
        if os.path.exists(DB_FILE):
            with open(DB_FILE, 'r', encoding='utf-8') as file:
                for line in file:
                    k, v = line.strip().split('=', 1)
                    kv_pairs[k] = v

        # 更新或添加键值对
        kv_pairs[key] = value

        # 将更新后的键值对写回文件
        with open(DB_FILE, 'w', encoding='utf-8') as file:
            for k, v in kv_pairs.items():
                file.write(f'{k}={v}\n')
        return True
    except Exception as e:
        print(f'设置键值对时出错: {e}')
        return False


def db_get(key):
    try:
        if os.path.exists(DB_FILE):
            with open(DB_FILE, 'r', encoding='utf-8') as file:
                for line in file:
                    k, v = line.strip().split('=', 1)
                    if k == key:
                        return v
        return None
    except Exception as e:
        print(f'获取键值对时出错: {e}')
        return None
