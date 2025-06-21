from .csvstore import CSVStore
from pathlib import Path

class MultiModalStore:
    def __init__(self, db_file_name):
        # 使用相对于项目根目录的路径
        self.data_dir = Path(__file__).parent.parent.parent / 'data'
        self.data_dir.mkdir(exist_ok=True)  # 确保目录存在
        self.db_file_path = self.data_dir / db_file_name
        self.db_file_name = db_file_name

        self.store = CSVStore(
            filepath=self.db_file_path,
            fieldnames=[
                'record_id', 'content', 'desc', 'create_time', 'type', 'class', 'extra'
            ],
            auto_create=True
        )
