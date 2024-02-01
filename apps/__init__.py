import json
from pathlib import Path
from datetime import datetime
from .sqliteobject import SQLiteObject

LOG_DIR = Path.cwd().joinpath("logs")


def get_time():
    """
    获取时间
    """
    time_now = datetime.now()
    time_str = time_now.strftime('%Y-%m-%d %H:%M:%S')

    return time_str


def save_data(name):
    """
    保存数据
    """
    def decorator(func):
        def process(*args, **kargs):
            SQL_OBJ = SQLiteObject()
            LOG_DIR.mkdir(exist_ok=True)
            response = func(*args, **kargs)
            log_path = LOG_DIR.joinpath(name + '.txt')

            with open(log_path, 'a', encoding='utf-8') as f:
                for resp in response:
                    resp['createTime'] = get_time()
                    SQL_OBJ.create_table(name, list(resp.keys()))
                    SQL_OBJ.insert_data(name, dict(resp))
                    row_data = json.dumps(resp, ensure_ascii=False)
                    f.write('{}\n'.format(row_data))
                    print('[Item]:', resp)

            SQL_OBJ.connect.close()

            return response
        return process
    return decorator
