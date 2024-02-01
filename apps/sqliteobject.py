import sqlite3
from pathlib import Path


class SQLiteObject:

    def __init__(self) -> None:
        # 尝试连接
        try:
            db_path = Path.cwd().joinpath('mydata.db')
            self.connect = sqlite3.connect(db_path)
            self.cursor = self.connect.cursor()
        except sqlite3.Error as e:
            print(e)

    def show_tables(self) -> list:
        """
        获取表名
        """
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [i[0] for i in self.cursor.fetchall()]

        return tables

    def show_columns(self, tablename: str) -> list:
        """
        获取列名
        :param tablename
        """
        self.cursor.execute(f"PRAGMA table_info({tablename});")
        columns = [i[1] for i in self.cursor.fetchall()]

        return columns

    def create_table(self, tablename: str, columns: list) -> bool:
        """
        创建表
        :param tablename
        :param columns
        """
        query = f"CREATE TABLE IF NOT EXISTS {tablename} ({', '.join([f'{col} TEXT' for col in columns])});"
        self.cursor.execute(query)
        self.connect.commit()

        return True

    def drop_table(self, tablename: str) -> bool:
        """
        删除表
        :param tablename
        """
        query = f"DROP TABLE IF EXISTS {tablename};"
        self.cursor.execute(query)
        self.connect.commit()

        return True

    def insert_data(self, tablename: str, data: dict) -> bool:
        """
        插入数据
        :param tablename
        :param data({'column1':'value1','column2':'value2','column3':'value3'})
        """
        columns = ', '.join(data.keys())
        values = ', '.join(['?'] * len(data))
        query = 'INSERT INTO {} ({}) VALUES ({})'.format(tablename, columns, values)

        self.cursor.execute(query, list(data.values()))
        self.connect.commit()

        return True

    def delete_data(self, tablename: str, conditions={}) -> bool:
        """
        删除数据
        :param tablename
        :param condition({'column1':'value1','column2':'value2','column3':'value3'})
        """
        if conditions:
            query = f'DELETE FROM {tablename}'
            query += " WHERE " + " AND ".join([f"{k}='{v}'" for k, v in conditions.items()])
        else:
            query = f'DELETE FROM {tablename}'

        self.cursor.execute(query)
        self.connect.commit()

        return True

    def select_data(self, tablename: str, conditions={}) -> tuple:
        """
        查询数据
        :param tablename
        :param condition({'column1':'value1','column2':'value2','column3':'value3'})
        """
        if conditions:
            query = f'SELECT * FROM {tablename}'
            query += " WHERE " + " AND ".join([f"{k}='{v}'" for k, v in conditions.items()])
        else:
            query = f'SELECT * FROM {tablename}'

        self.cursor.execute(query)
        results = self.cursor.fetchall()

        return results

    def update_data(self, tablename: str, conditions: dict, data: dict) -> bool:
        """
        更新数据
        :param tablename
        :param data({'column':'value'})
        :param condition({'column1':'value1','column2':'value2','column3':'value3'})
        """
        query = f"UPDATE {tablename} SET " + ', '.join([f"{k}='{v}'" for k, v in data.items()])
        query += " WHERE " + " AND ".join([f"{k}='{v}'" for k, v in conditions.items()])

        self.cursor.execute(query)
        self.connect.commit()

        return True
