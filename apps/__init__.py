import json
from pathlib import Path
from datetime import datetime

LOG_DIR = Path.cwd().joinpath("logs")


def write_log(filename):
    """
    写日志
    """
    def decorator(func):
        def process(*args, **kargs):
            LOG_DIR.mkdir(exist_ok=True)
            response = func(*args, **kargs)
            logPath = LOG_DIR.joinpath(filename)
            with open(logPath, 'a', encoding='utf-8') as f:
                for value in response:
                    time_now = datetime.now()
                    time_str = time_now.strftime('%H:%M:%S')
                    item = {'time': time_str, 'resp': value}
                    item = json.dumps(item, ensure_ascii=False)
                    f.write('{}\n'.format(item))
                    print(item)

            return response
        return process
    return decorator
