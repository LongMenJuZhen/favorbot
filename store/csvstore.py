import csv
import os
from typing import List, Dict, Any, Optional, Union
import tempfile
import shutil


class CSVStore:
    """
    CSV 文件存储操作类，支持增删改查等基本操作

    功能特点：
    - 自动处理文件存在性检查
    - 支持自定义分隔符和编码
    - 提供事务支持（通过临时文件）
    - 支持批量操作
    - 提供简单的查询过滤功能
    """

    def __init__(self,
                 filepath: str,
                 fieldnames: Optional[List[str]] = None,
                 delimiter: str = ',',
                 encoding: str = 'utf-8',
                 auto_create: bool = True):
        """
        初始化 CSV 存储

        :param filepath: CSV 文件路径
        :param fieldnames: 字段名列表，如果为None则从文件第一行读取
        :param delimiter: 分隔符，默认为逗号
        :param encoding: 文件编码，默认为utf-8
        :param auto_create: 如果文件不存在是否自动创建
        """
        self.filepath = filepath
        self.delimiter = delimiter
        self.encoding = encoding
        self._fieldnames = fieldnames

        # 如果文件不存在且允许自动创建
        if auto_create and not os.path.exists(filepath):
            self._ensure_directory_exists()
            with open(filepath, 'w', newline='', encoding=encoding) as f:
                if fieldnames:
                    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
                    writer.writeheader()

        # 如果文件已存在或已创建，读取字段名
        if os.path.exists(filepath):
            with open(filepath, 'r', newline='', encoding=encoding) as f:
                reader = csv.DictReader(f, delimiter=delimiter)
                self._fieldnames = reader.fieldnames or fieldnames

    @property
    def fieldnames(self) -> List[str]:
        """返回 CSV 文件的字段名列表"""
        return self._fieldnames

    def _ensure_directory_exists(self):
        """确保文件所在目录存在"""
        dirname = os.path.dirname(self.filepath)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)

    def insert(self, record: Dict[str, Any]) -> None:
        """
        插入单条记录

        :param record: 要插入的记录字典
        :raises ValueError: 如果记录字段与CSV字段不匹配
        """
        self.insert_many([record])

    def insert_many(self, records: List[Dict[str, Any]]) -> None:
        """
        插入多条记录

        :param records: 要插入的记录字典列表
        :raises ValueError: 如果记录字段与CSV字段不匹配
        """
        if not records:
            return

        # 验证字段
        for record in records:
            if set(record.keys()) != set(self.fieldnames):
                raise ValueError(f"记录字段不匹配，期望: {self.fieldnames}, 得到: {list(record.keys())}")

        # 以追加模式写入
        with open(self.filepath, 'a', newline='', encoding=self.encoding) as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames, delimiter=self.delimiter)
            writer.writerows(records)

    def read_all(self) -> List[Dict[str, Any]]:
        """
        读取所有记录

        :return: 记录字典列表
        """
        with open(self.filepath, 'r', newline='', encoding=self.encoding) as f:
            reader = csv.DictReader(f, delimiter=self.delimiter)
            return list(reader)

    def find(self, condition: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        查找符合条件的记录

        :param condition: 查询条件字典，例如 {'name': 'Alice', 'age': '30'}
        :return: 匹配的记录列表
        """
        all_records = self.read_all()

        if not condition:
            return all_records

        def matches(record):
            for key, value in condition.items():
                if str(record.get(key)) != str(value):
                    return False
            return True

        return [record for record in all_records if matches(record)]

    def update(self, condition: Dict[str, Any], new_values: Dict[str, Any]) -> int:
        """
        更新符合条件的记录

        :param condition: 查询条件字典
        :param new_values: 要更新的字段和值
        :return: 更新的记录数
        """
        # 读取所有记录
        all_records = self.read_all()
        updated_count = 0

        # 更新符合条件的记录
        for record in all_records:
            match = True
            for key, value in condition.items():
                if str(record.get(key)) != str(value):
                    match = False
                    break
            if match:
                record.update(new_values)
                updated_count += 1

        # 如果有更新，则重写整个文件
        if updated_count > 0:
            self._write_all_records(all_records)

        return updated_count

    def delete(self, condition: Dict[str, Any]) -> int:
        """
        删除符合条件的记录

        :param condition: 查询条件字典
        :return: 删除的记录数
        """
        # 读取所有记录
        all_records = self.read_all()
        # 过滤出不符合条件的记录
        remaining_records = []
        deleted_count = 0

        for record in all_records:
            match = True
            for key, value in condition.items():
                if str(record.get(key)) != str(value):
                    match = False
                    break
            if match:
                deleted_count += 1
            else:
                remaining_records.append(record)

        # 如果有删除，则重写整个文件
        if deleted_count > 0:
            self._write_all_records(remaining_records)

        return deleted_count

    def _write_all_records(self, records: List[Dict[str, Any]]) -> None:
        """
        内部方法：将所有记录写入文件（使用事务处理）
        """
        # 使用临时文件实现原子写入
        temp_fd, temp_path = tempfile.mkstemp(prefix='csvstore_', dir=os.path.dirname(self.filepath))

        try:
            with os.fdopen(temp_fd, 'w', newline='', encoding=self.encoding) as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames, delimiter=self.delimiter)
                writer.writeheader()
                writer.writerows(records)

            # 替换原文件
            shutil.move(temp_path, self.filepath)
        except Exception as e:
            # 发生错误时删除临时文件
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise e

    def count(self) -> int:
        """
        返回记录总数（不包括标题行）
        """
        with open(self.filepath, 'r', newline='', encoding=self.encoding) as f:
            return sum(1 for _ in f) - 1  # 减去标题行

    def clear(self) -> None:
        """
        清空所有数据（只保留标题行）
        """
        with open(self.filepath, 'w', newline='', encoding=self.encoding) as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames, delimiter=self.delimiter)
            writer.writeheader()

    def __enter__(self):
        """支持上下文管理器"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """支持上下文管理器"""
        pass