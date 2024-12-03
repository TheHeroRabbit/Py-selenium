import pymysql
import sqlite3

from pathlib import Path
from pymysql.cursors import DictCursor


class SQLiteClient:

    def __init__(self) -> None:
        """
        初始化SQLite数据库连接
        创建一个SQLite数据库连接，并创建一个游标用于执行SQL命令。
        数据库文件将位于当前工作目录下，命名为'db.sqlite3'。
        """
        db_path = Path.cwd().joinpath('db.sqlite3')
        self.connect = sqlite3.connect(db_path)
        self.cursor = self.connect.cursor()

    def show_tables(self) -> list:
        """
        获取数据库中所有表的名称
        :return: 表名列表
        """
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return [row[0] for row in self.cursor.fetchall()]

    def show_columns(self, tablename: str) -> list:
        """
        获取指定表的所有列名
        :param tablename: 表名
        :return: 列名列表
        """
        self.cursor.execute(f"PRAGMA table_info({tablename});")
        return [row[1] for row in self.cursor.fetchall()]

    def create_table(self, tablename: str, columns: list) -> bool:
        """
        创建一个新表，所有列均为TEXT类型
        :param tablename: 表名
        :param columns: 列名列表，格式为 ["列名1", "列名2", ...]
        :return: 创建表成功返回True
        :raises ValueError: 如果列名列表为空
        """
        if not columns:
            raise ValueError("列名列表不能为空。")

        # 将所有列名转换为TEXT类型
        columns_str = ", ".join([f"{column} TEXT" for column in columns])
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {tablename} ({columns_str});")
        self.connect.commit()
        return True

    def truncate_table(self, tablename: str) -> bool:
        """
        清空指定表中的所有数据
        :param tablename: 表名
        :return: 清空成功返回True
        """
        self.cursor.execute(f"DELETE FROM {tablename};")
        self.connect.commit()
        return True

    def drop_table(self, tablename: str) -> bool:
        """
        删除指定表
        :param tablename: 表名
        :return: 删除表成功返回True
        """
        self.cursor.execute(f"DROP TABLE IF EXISTS {tablename};")
        self.connect.commit()
        return True

    def insert_item(self, tablename: str, item: dict) -> bool:
        """
        向指定表中插入一条数据
        :param tablename: 表名
        :param item: 插入数据的字典，格式为 {'column1':'value1','column2':'value2',...}
        :return: 插入成功返回True
        """
        columns = ', '.join(item.keys())
        placeholders = ', '.join(['?'] * len(item))
        values = list(item.values())
        self.cursor.execute(f"INSERT INTO {tablename} ({columns}) VALUES ({placeholders});", values)
        self.connect.commit()
        return True

    def insert_items(self, tablename: str, items: list) -> bool:
        """
        向指定表中插入多条数据
        :param tablename: 表名
        :param items: 插入数据的字典列表，格式为 [{'column1':'value1','column2':'value2',...}, ...]
        :return: 插入成功返回True
        """
        if not items:
            return False
        columns = ', '.join(items[0].keys())
        placeholders = ', '.join(['?'] * len(items[0]))
        values = [list(item.values()) for item in items]
        self.cursor.executemany(f"INSERT INTO {tablename} ({columns}) VALUES ({placeholders});", values)
        self.connect.commit()
        return True

    def delete_item(self, tablename: str, conditions={}) -> bool:
        """
        从指定表中删除数据
        :param tablename: 表名
        :param conditions: 删除条件字典，格式为 {'column1':'value1','column2':'value2',...}
        :return: 删除成功返回True
        """
        if not conditions:
            return False
        condition_str = ' AND '.join([f"{k} = ?" for k in conditions.keys()])
        values = list(conditions.values())
        self.cursor.execute(f"DELETE FROM {tablename} WHERE {condition_str};", values)
        self.connect.commit()
        return True

    def select_item(self, tablename: str, conditions={}) -> list:
        """
        查询指定表中的数据
        :param tablename: 表名
        :param conditions: 查询条件字典，格式为 {'column1':'value1','column2':'value2',...}
        :return: 查询结果列表
        """
        if conditions:
            condition_str = ' AND '.join([f"{k} = ?" for k in conditions.keys()])
            values = list(conditions.values())
            self.cursor.execute(f"SELECT * FROM {tablename} WHERE {condition_str};", values)
        else:
            self.cursor.execute(f"SELECT * FROM {tablename};")
        return self.cursor.fetchall()

    def update_item(self, tablename: str, conditions: dict, item: dict) -> bool:
        """
        更新指定表中的数据
        :param tablename: 表名
        :param item: 更新数据的字典，格式为 {'column':'new_value'}
        :param conditions: 更新条件字典，格式为 {'column1':'value1','column2':'value2',...}
        :return: 更新成功返回True
        """
        if not conditions or not item:
            return False
        item_str = ', '.join([f"{k} = ?" for k in item.keys()])
        condition_str = ' AND '.join([f"{k} = ?" for k in conditions.keys()])
        values = list(item.values()) + list(conditions.values())
        self.cursor.execute(f"UPDATE {tablename} SET {item_str} WHERE {condition_str};", values)
        self.connect.commit()
        return True


class MySQLClient:

    def __init__(self, host: str, port: int, user: str, password: str, database: str) -> None:
        """
        初始化MySQL数据库连接
        创建一个MySQL数据库连接，并创建一个游标用于执行SQL命令。
        """
        self.connect = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            cursorclass=DictCursor
        )
        self.cursor = self.connect.cursor()

    def show_tables(self) -> list:
        """
        获取数据库中所有表的名称
        :return: 表名列表
        """
        self.cursor.execute("SHOW TABLES;")
        return [row['Tables_in_' + self.connect.db.decode()] for row in self.cursor.fetchall()]

    def show_columns(self, tablename: str) -> list:
        """
        获取指定表的所有列名
        :param tablename: 表名
        :return: 列名列表
        """
        self.cursor.execute(f"SHOW COLUMNS FROM {tablename};")
        return [row['Field'] for row in self.cursor.fetchall()]

    def create_table(self, tablename: str, columns: list) -> bool:
        """
        创建一个新表，所有列均为TEXT类型
        :param tablename: 表名
        :param columns: 列名列表，格式为 ["列名1", "列名2", ...]
        :return: 创建表成功返回True
        :raises ValueError: 如果列名列表为空
        """
        if not columns:
            raise ValueError("列名列表不能为空。")

        # 将所有列名转换为TEXT类型
        columns_str = ", ".join([f"`{column}` TEXT" for column in columns])
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS `{tablename}` ({columns_str});")
        self.connect.commit()
        return True

    def truncate_table(self, tablename: str) -> bool:
        """
        清空指定表中的所有数据
        :param tablename: 表名
        :return: 清空成功返回True
        """
        self.cursor.execute(f"TRUNCATE TABLE `{tablename}`;")
        self.connect.commit()
        return True

    def drop_table(self, tablename: str) -> bool:
        """
        删除指定表
        :param tablename: 表名
        :return: 删除表成功返回True
        """
        self.cursor.execute(f"DROP TABLE IF EXISTS `{tablename}`;")
        self.connect.commit()
        return True

    def insert_item(self, tablename: str, item: dict) -> bool:
        """
        向指定表中插入一条数据
        :param tablename: 表名
        :param item: 插入数据的字典，格式为 {'column1':'value1','column2':'value2',...}
        :return: 插入成功返回True
        """
        columns = ', '.join([f"`{k}`" for k in item.keys()])
        placeholders = ', '.join(['%s'] * len(item))
        values = list(item.values())
        self.cursor.execute(f"INSERT INTO `{tablename}` ({columns}) VALUES ({placeholders});", values)
        self.connect.commit()
        return True

    def insert_items(self, tablename: str, items: list) -> bool:
        """
        向指定表中插入多条数据
        :param tablename: 表名
        :param items: 插入数据的字典列表，格式为 [{'column1':'value1','column2':'value2',...}, ...]
        :return: 插入成功返回True
        """
        if not items:
            return False
        columns = ', '.join([f"`{k}`" for k in items[0].keys()])
        placeholders = ', '.join(['%s'] * len(items[0]))
        values = [list(item.values()) for item in items]
        self.cursor.executemany(f"INSERT INTO `{tablename}` ({columns}) VALUES ({placeholders});", values)
        self.connect.commit()
        return True

    def delete_item(self, tablename: str, conditions={}) -> bool:
        """
        从指定表中删除数据
        :param tablename: 表名
        :param conditions: 删除条件字典，格式为 {'column1':'value1','column2':'value2',...}
        :return: 删除成功返回True
        """
        if not conditions:
            return False
        condition_str = ' AND '.join([f"`{k}` = %s" for k in conditions.keys()])
        values = list(conditions.values())
        self.cursor.execute(f"DELETE FROM `{tablename}` WHERE {condition_str};", values)
        self.connect.commit()
        return True

    def select_item(self, tablename: str, conditions={}) -> list:
        """
        查询指定表中的数据
        :param tablename: 表名
        :param conditions: 查询条件字典，格式为 {'column1':'value1','column2':'value2',...}
        :return: 查询结果列表
        """
        if conditions:
            condition_str = ' AND '.join([f"`{k}` = %s" for k in conditions.keys()])
            values = list(conditions.values())
            self.cursor.execute(f"SELECT * FROM `{tablename}` WHERE {condition_str};", values)
        else:
            self.cursor.execute(f"SELECT * FROM `{tablename}`;")
        return self.cursor.fetchall()

    def update_item(self, tablename: str, conditions: dict, item: dict) -> bool:
        """
        更新指定表中的数据
        :param tablename: 表名
        :param item: 更新数据的字典，格式为 {'column':'new_value'}
        :param conditions: 更新条件字典，格式为 {'column1':'value1','column2':'value2',...}
        :return: 更新成功返回True
        """
        if not conditions or not item:
            return False
        item_str = ', '.join([f"`{k}` = %s" for k in item.keys()])
        condition_str = ' AND '.join([f"`{k}` = %s" for k in conditions.keys()])
        values = list(item.values()) + list(conditions.values())
        self.cursor.execute(f"UPDATE `{tablename}` SET {item_str} WHERE {condition_str};", values)
        self.connect.commit()
        return True
