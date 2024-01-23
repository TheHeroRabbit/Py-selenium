import json
from datetime import datetime


def write_log(file):
    """
    写日志
    """
    def decorator(func):
        def process(*args, **kargs):
            response = func(*args, **kargs)
            with open(file, 'a', encoding='utf-8') as f:
                for resp in response:
                    time_now = datetime.now()
                    time_str = time_now.strftime('%H:%M:%S')
                    item = {'time': time_str, 'resp': resp}
                    item = json.dumps(item, ensure_ascii=False)
                    f.write('{}\n'.format(item))
                    print(item)

            return response
        return process
    return decorator
