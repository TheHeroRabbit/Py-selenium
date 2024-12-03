import json
from pathlib import Path
from datetime import datetime

from .easydb import MySQLClient
from .easydb import SQLiteClient

LOG_DIR = Path.cwd().joinpath("logs")


def get_time_str():
    """
    获取时间
    """
    time_now = datetime.now()
    time_str = time_now.strftime('%Y-%m-%d %H:%M:%S')

    return time_str


def save_data(name):
    """
    保存数据的装饰器工厂函数。

    该装饰器用于将被装饰函数返回的响应数据保存到数据库和日志文件中。

    参数：
        name (str): 数据库表和日志文件的名称。
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            """
            包装函数，执行被装饰函数并处理响应数据。
            """
            # 创建日志目录（如果不存在）
            LOG_DIR.mkdir(exist_ok=True)
            # 执行被装饰的函数，获取响应
            response = func(*args, **kwargs)
            # 定义日志文件路径
            log_path = LOG_DIR / f'{name}.txt'
            # 创建数据库客户端实例
            sql_client = SQLiteClient()
            try:
                # 打开日志文件，以追加模式写入
                with open(log_path, 'a', encoding='utf-8') as f:
                    # 遍历响应中的每个项目
                    for idx, resp in enumerate(response):
                        # 添加创建时间戳
                        resp['createTime'] = get_time_str()
                        # 在第一次迭代时创建数据库表
                        if idx == 0:
                            field_names = list(resp.keys())
                            sql_client.create_table(name, field_names)
                        # 插入记录到数据库
                        sql_client.insert_item(name, resp)
                        # 将记录转换为JSON字符串
                        row_data = json.dumps(resp, ensure_ascii=False)
                        # 写入日志文件
                        f.write(f'{row_data}\n')
                        # 打印记录到控制台
                        print('[Item]:', resp)
            finally:
                # 确保数据库连接被关闭
                sql_client.connect.close()
            # 返回响应
            return response
        return wrapper
    return decorator
